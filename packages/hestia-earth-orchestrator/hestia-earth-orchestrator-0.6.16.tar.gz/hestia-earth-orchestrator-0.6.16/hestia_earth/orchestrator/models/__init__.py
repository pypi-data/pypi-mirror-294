import os
import importlib
from functools import reduce
import concurrent.futures
from pydash.objects import clone_deep
from hestia_earth.utils.tools import non_empty_list

from ..log import logger
from ..version import VERSION
from ..utils import get_required_model_param, _snakecase
from ..strategies.run import should_run
from ..strategies.merge import merge


def _max_workers(type: str):
    try:
        return int(os.getenv(f"MAX_WORKERS_{type.upper()}"))
    except Exception:
        return None


def _list_except_item(list, item):
    idx = list.index(item)
    return list[:idx] + list[idx+1:]


def _import_model(name: str):
    # try to load the model from the default hestia engine, fallback to orchestrator model
    try:
        return {
            'run': importlib.import_module(f"hestia_earth.models.{name}").run,
            'version': importlib.import_module('hestia_earth.models.version').VERSION
        }
    except ModuleNotFoundError:
        # try to load the model from the the models folder, fallback to fully specified name
        try:
            return {
                'run': importlib.import_module(f"hestia_earth.orchestrator.models.{name}").run,
                'version': importlib.import_module('hestia_earth.orchestrator.version').VERSION
            }
        except ModuleNotFoundError:
            return {
                'run': importlib.import_module(f"{name}").run,
                'version': VERSION
            }


def _run_pre_checks(data: dict):
    node_type = _snakecase(data.get('@type', data.get('type')))
    try:
        pre_checks = _import_model('.'.join([node_type, 'pre_checks'])).get('run')
        logger.info('running pre checks for %s', node_type)
        return pre_checks(data)
    except Exception:
        return data


def _run_post_checks(data: dict):
    node_type = _snakecase(data.get('@type', data.get('type')))
    try:
        post_checks = _import_model('.'.join([node_type, 'post_checks'])).get('run')
        logger.info('running post checks for %s', node_type)
        return post_checks(data)
    except Exception:
        return data


def _run_model(data: dict, model: dict, models: list):
    module = _import_model(get_required_model_param(model, 'model'))
    # if no value is provided, use all the models but this one
    model_value = model.get('value') or _list_except_item(models, model)
    result = module.get('run')(model_value, data)
    return {'data': data, 'model': model, 'version': module.get('version'), 'result': result}


def _run(data: dict, model: dict, models: list):
    return _run_model(data, model, models) if should_run(data, model) else None


def _run_serie(data: dict, models: list):
    return reduce(
        lambda prev, m: merge(prev, _run_parallel(prev, m, models) if isinstance(m, list) else [_run(prev, m, models)]),
        models,
        data
    )


def _run_parallel(data: dict, model: list, models: list):
    results = []

    max_workers = _max_workers(data.get('@type', data.get('type')))
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(_run, clone_deep(data), m, models) for m in model]

    for future in concurrent.futures.as_completed(futures):
        results.append(future.result())

    return results


def _filter_models_stage(models: list, stage: int = None):
    return models if stage is None else non_empty_list([
        (_filter_models_stage(m, stage) if isinstance(m, list) else m) for m in models if (
            not isinstance(m, dict) or m.get('stage') == stage
        )
    ])


def run(data: dict, models: list, stage: int = None):
    # run pre-checks if exist
    data = _run_pre_checks(data)
    models = _filter_models_stage(models, stage=stage)
    data = _run_serie(data, models)
    # run post-checks if exist
    return _run_post_checks(data)
