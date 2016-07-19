from datetime import datetime
import json

from lettuce import world
from lettuce.terrain import after, before


def enable(filename=None):
    filename = filename or "lettucetests.json"

    @before.all
    def before_all():
        """
        Set `world._started` to `datetime.now()` to track total duration.
        """
        world._started = datetime.now()

    @after.all
    def generate_json_output(total):
        """
        This callback is called after all the features are
        ran.
        """
        world._stopped = datetime.now()
        total_dict = total_result_to_dict(total)
        with open(filename, "w") as handle:
            json.dump(total_dict, handle)

    @before.each_feature
    @before.each_scenario
    @before.each_step
    def before_each_element(*args):
        """
        Set `step._started`, `scenario._started` or `feature._started` to `datetime.now()`
        to track step/scenario/feature duration.
        """
        element = args[0]
        element._started = datetime.now()

    @after.each_feature
    @after.each_scenario
    @after.each_step
    def after_each_element(*args):
        """
        Set `step._stopped`, `scenario._stopped` or `feature._stopped` to `datetime.now()`
        to track step/scenario/feature duration.
        """
        element = args[0]
        element._stopped = datetime.now()


def total_result_to_dict(total):
    """
    Transform a `TotalResult` to a json-serializable Python dictionary.

    :param total:               a `TotalResult` instance
    :return:                    a Python dictionary
    """
    return {
        "meta": extract_meta(total),
        "duration": _get_duration(world),
        "features": [
            extract_feature_data(feature_result)
            for feature_result in total.feature_results
        ]
    }


def extract_feature_data(feature_result):
    """
    Extract data from a `FeatureResult` instance.

    :param feature_result:                a `FeatureResult` instance
    :return:                              a Python dictionary
    """
    scenarios = []
    meta = {
        "steps": {
            "total": 0,
            "success": 0,
            "failures": 0,
            "skipped": 0,
            "undefined": 0,
        },
        "scenarios": {
            "total": 0,
            "success": 0,
            "failures": 0,
            "skipped": 0,
            "undefined": 0,
        }
    }
    for scenario_result in feature_result.scenario_results:
        scenario_data = extract_scenario_data(scenario_result)
        scenarios.append(scenario_data)
        # scenarios
        success = (
            not scenario_data["meta"]["failures"] and
            not scenario_data["meta"]["skipped"] and
            not scenario_data["meta"]["undefined"]
        )
        meta["scenarios"]["total"] += 1 if scenario_data["meta"]["total"] else 0
        meta["scenarios"]["success"] += 1 if success else 0
        meta["scenarios"]["failures"] += 1 if scenario_data["meta"]["failures"] else 0
        meta["scenarios"]["skipped"] += 1 if scenario_data["meta"]["skipped"] else 0
        meta["scenarios"]["undefined"] += 1 if scenario_data["meta"]["undefined"] else 0
        # steps
        meta["steps"]["total"] += scenario_data["meta"]["total"]
        meta["steps"]["success"] += scenario_data["meta"]["success"]
        meta["steps"]["failures"] += scenario_data["meta"]["failures"]
        meta["steps"]["skipped"] += scenario_data["meta"]["skipped"]
        meta["steps"]["undefined"] += scenario_data["meta"]["undefined"]

    return {
        "name": feature_result.feature.name,
        "duration": _get_duration(feature_result.feature),
        "meta": meta,
        "scenarios": scenarios,
        "background": extract_background_data(feature_result.feature.background)
    }

def extract_background_data(background):
    """
    Extract data from a `Background` instance.

    :param background:                   a `Background` instance, possibly None
    :return:                             a Python dictionary
    """
    if not background:
        return None

    step_data = [extract_step_data(step) for step in background.steps]
    return {
        "meta": {
            "total": len(background.steps),
            "success": sum([s["meta"]["success"] for s in step_data]),
            "failures": sum([s["meta"]["failed"] for s in step_data]),
            "skipped": sum([s["meta"]["skipped"] for s in step_data]),
            "undefined": sum([s["meta"]["undefined"] for s in step_data]),
        },
        "steps": step_data
    }


def extract_scenario_data(scenario_result):
    """
    Extract data from a `ScenarioResult` instance.

    :param scenario_result:              a `ScenarioResult` instance
    :return:                             a Python dictionary
    """
    return {
        "name": scenario_result.scenario.name,
        "duration": _get_duration(scenario_result.scenario),
        "outline": scenario_result.outline,
        "meta": {
            "total": scenario_result.total_steps,
            "success": len(scenario_result.steps_passed),
            "failures": len(scenario_result.steps_failed),
            "skipped": len(scenario_result.steps_skipped),
            "undefined": len(scenario_result.steps_undefined),
        },
        "steps": [extract_step_data(step) for step in scenario_result.all_steps]
    }


def extract_step_data(step):
    """
    Extract data from a `Step` instance.

    :param step:                         a `Step` instance
    :return                              a Python dictionary
    """
    step_data = {
        "name": step.sentence,
        "duration": _get_duration(step),
        "meta": {
            "success": bool(step.passed),
            "failed": bool(step.failed),
            "skipped": not step.passed and not step.failed and step.has_definition,
            "undefined": not step.has_definition,
        },
        "failure": {}
    }
    if step.why:
        step_data["failure"] = {
            "exception": repr(step.why.exception),
            "traceback": step.why.traceback
        }
    return step_data


def extract_meta(total):
    """
    Extract metadata from the `TotalResult`.

    :param total:               a `TotalResult` instance
    :return:                    a Python dictionary
    """
    return {
        "features": {
            "total": total.features_ran,
            "success": total.features_passed,
            "failures": total.features_ran - total.features_passed,
        },
        "scenarios": {
            "total": total.scenarios_ran,
            "success": total.scenarios_passed,
            "failures": total.scenarios_ran - total.scenarios_passed,
        },
        "steps": {
            "total": total.steps,
            "success": total.steps_passed,
            "failures": total.steps_failed,
            "skipped": total.steps_skipped,
            "undefined": total.steps_undefined,
        },
        "is_success": total.is_success,
    }


def _get_duration(element):
    """
    Return the duration of an element.

    :param element:          either a step or a scenario or a feature
    """
    return (element._stopped - element._started).seconds if hasattr(element, '_started') else None
