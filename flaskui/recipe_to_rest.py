import json
from pprint import pprint

mission = "galileo_ssi_edr"

with open( mission + ".json", "r" ) as file:
    generator_recipe = {
        "mission": "",
        "tasks": [],
        "output": "directory"
    }

    recipe = json.load( file )

    tasks_dict = recipe["pow"]["recipe"]
    tasks = []

    # print( tasks_dict )

    for key in tasks_dict.keys():
        task = [key]

        parameters = []
        for parameter_key in tasks_dict[key].keys():
            parameters.append( [parameter_key, tasks_dict[key][parameter_key]] )

        task.append( parameters )
        tasks.append( task )

    # print()
    # print()
    # print( tasks )

    generator_recipe["mission"] = mission
    generator_recipe["tasks"] = tasks

    # pprint( generator_recipe )

# Parses a USGS mission recipe file and returns a generator useable JSON
def parse_recipe( mission ):

    with open( mission + ".json", "r" ) as file:
        generator_recipe = {
            "mission": "",
            "tasks": [],
            "output": ""
        }

        recipe = json.load( file )

        tasks_dict = recipe["pow"]["recipe"]
        tasks = []

        # print( tasks_dict )

        for key in tasks_dict.keys():
            task = [key]

            parameters = []
            for parameter_key in tasks_dict[key].keys():
                parameters.append( [parameter_key, tasks_dict[key][parameter_key]] )

            task.append( parameters )
            tasks.append( task )

        # print()
        # print()
        # print( tasks )

        generator_recipe["mission"] = mission
        generator_recipe["tasks"] = tasks

        # pprint( generator_recipe )

# Returns a JSON object useable by the UI
def recipe_to_ui( mission ):

    filename = mission + ".json"

    ui_dict = {
        "mission": mission,
        "tasks": {},
        "src": ""
    }

    with open( filename, "r" ) as file:
        recipe_json = json.load( file )
        ui_dict["tasks"] = recipe_json["pow"]["recipe"]
        ui_dict["src"] = recipe_json["src"]

    return ui_dict
