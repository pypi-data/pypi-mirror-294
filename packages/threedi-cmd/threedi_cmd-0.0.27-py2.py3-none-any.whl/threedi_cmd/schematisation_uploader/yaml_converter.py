import yaml
import threedi_api_client.openapi.models as models

from pathlib import Path
from typing import Dict, List, Union


class Organisation:
    fields = "{{ organisation_uuid }}"


class ThreediModel:
    fields = {
        "schematisation_id": "{{ schematisation_id }}",
        "revision_id": "{{ revision_id }}",
        "auto_update": True,
    }


class Simulation:
    fields = {
        "threedimodel": ThreediModel,
        "organisation": Organisation,
        "name": "{{ simulation_name }}",
        "start_datetime": "{{ datetime_now }}",
        "duration": "{{ duration }}",
    }


scenario_mapping: Dict[str, Union[Organisation, ThreediModel, Simulation]] = {
    "organisation": Organisation,
    "simulation": Simulation,
    "threedimodel": ThreediModel,
}

event_mapping = {
    "breach": models.Breach,
    "constantlateral": models.ConstantLateral,
    "constantrain": models.ConstantRain,
    "filelateral": models.FileLateral,
    "leakagerasterlocal": models.FileRasterLeakage,
    "localrainconstant": models.ConstantLocalRain,
    "localraintimeseries": models.TimeseriesLocalRain,
    "rainrasterlizard": models.LizardRasterRain,
    "raintimeserieslizard": models.LizardTimeseriesRain,
    # rasteredit
    "timeseriesboundary": models.BoundaryCondition,
    # "timeseriesinflow": models.TimeseriesInflow,
    "timeserieslateral": models.TimeseriesLateral,
    "timeseriesleakage": models.TimeseriesLeakage,
    "timeseriesrain": models.TimeseriesRain,
    "timeseriessourcessinks": models.TimeseriesSourcesSinks,
    # saved_state
    # initial saved state
    "timeserieswind": models.TimeseriesWind,
    # "winddragcoefficients": models.WindDragCoefficients,
}


def convert_yaml(yaml_file: Path) -> None:
    with open(yaml_file, "r") as f:
        data = yaml.load(f, Loader=yaml.FullLoader)

    meta = {}
    if "meta" in data:
        meta = data["meta"]

    scenario = {}
    scenario["steps"] = _get_events(data["scenario"]["steps"])
    del data["scenario"]["steps"]

    for key, values in data["scenario"].items():
        if key in scenario_mapping:
            model = scenario_mapping[key]
            params = _extract_scenario(model, values)
            scenario[key] = params

    test_name = yaml_file.stem
    with open(yaml_file.parent / f"{test_name}_converted.yaml", "w") as f:
        yaml.dump({"meta": meta, "scenario": scenario}, f)


def fill_yaml(yaml_file: Path, schematisation_id=None, revision_id=None) -> None:
    with open(yaml_file, "r") as f:
        data = yaml.load(f, Loader=yaml.FullLoader)

    data["scenario"]["simulation"]["threedimodel"]["schematisation_id"] = schematisation_id
    data["scenario"]["simulation"]["threedimodel"]["revision_id"] = revision_id

    with open(yaml_file, "w") as f:
        yaml.dump(data, f)


def _openapi_to_dict(attribute_map: Dict, required_values: List, values: Dict) -> Dict:
    # Create placeholders for all required values and fill values if they are present
    # in the attribute_map
    params = {} 
    for key in required_values:
        if key in values:
            params[key] = values[key]
        else:
            params[key] = "{{ " + key + " }}"

    for key, value in values.items():
        if key in attribute_map:
            params[key] = value

    return params


def _extract_scenario(model: Union[Organisation, ThreediModel, Simulation], values: Dict):
    # Recursivlely extract fields van scenario models
    if isinstance(model.fields, str):
        return model.fields

    params = {}
    for key, v in model.fields.items():
        if key in scenario_mapping:
            params[key] = _extract_scenario(scenario_mapping[key], {})
        elif key in values:
            params[key] = values[key]
        else:
            params[key] = v

    return params

def _get_events(steps: List[Dict]) -> List[Dict]:
    events = []
    for step in steps:
        key = list(step.keys())[0]
        if key in event_mapping:
            model = event_mapping[key]
            params = _openapi_to_dict(model.attribute_map, model.required_fields, step[key])
            events += [{key: params}]

    events += [{"action": {"name": "start", "waitfor_timeout": 1800}}]
    events += [{"waitforstatus": {"name": "finished", "timeout": 1800}}]
    return events
