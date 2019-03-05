# ------------------------------------------------------------------------------
# Imports ----------------------------------------------------------------------
# ------------------------------------------------------------------------------


import json
import copy

from datetime import datetime

# May be unnecessary
#import sys



# ------------------------------------------------------------------------------
# Constants --------------------------------------------------------------------
# ------------------------------------------------------------------------------


DEBUG = False
TEST = True
TEST_FILE = "REST_json.json"
DAG_DIRECTORY = "./dags/"



# ------------------------------------------------------------------------------
# Classes ----------------------------------------------------------------------
# ------------------------------------------------------------------------------


class CommandObject:

    def __init__( self, name, command, parameters ):
        self.command = command
        self.parameters = parameters
        self.name = name

    def __str__( self ):
        output = self.command

        for parameter in self.parameters:
            if(parameter[1] != "default"):
                output += " " + parameter[0] + "="
                if(parameter[0] == "from" or parameter[0] == "to"):
                    output += "/"
                output += parameter[1]

        return output


class WGETCommandObject:

    def __init__( self, name, parameter ):
        self.command = "cd /img && wget"
        self.parameter = parameter
        self.name = "wget" + name

    def __str__( self ):
        return self.command + " " + self.parameter


class DAGObject:

    # Command is a CommandObject
    def __init__( self, command ):
        self.command = command

    def __str__( self ):
        output = '''%s = BashOperator(
    task_id="%s",
    bash_command= prefix + "%s",
    retries=3,
    dag=dag
)'''

        output = output % (self.command.name, self.command.name, str(self.command))

        return output

    def get_name( self ):
        return self.command.name



# ------------------------------------------------------------------------------
# Functions --------------------------------------------------------------------
# ------------------------------------------------------------------------------


# Generates the string for a DAG file from given list of DAG objects
# TODO: Generate full dag for all included images
# TODO: Move dag string
# TODO: Move start object to object generation
# TODO: Format dag, e.g. put spaces between parentheses
# TODO: Place name of dag in dag
def generate_dag( dag_objects ):

    dag_string = '''from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime.today(),
    "email": ["airflow@example.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 3,
    "retry_delay": timedelta( minutes=5 ),
}

dag = DAG( "image_generation_dag", default_args=default_args, schedule_interval="@once" )

prefix = 'source activate PDS-Pipelines && python /opt/conda/envs/PDS-Pipelines/scripts/isis3VarInit.py && source activate PDS-Pipelines && '

start = BashOperator(
    task_id="start",
    bash_command="echo Starting...",
    retries=3,
    dag=dag
)'''

    for dag_object in dag_objects:
        dag_string += "\n\n" + str( dag_object )

    dag_string += "\n"
    dag_string += "\nstart.set_downstream(" + dag_objects[0].get_name() + ")"

    for index in range( len( dag_objects ) - 1 ):
        dag_string += "\n" + dag_objects[index].get_name() + ".set_downstream(" + dag_objects[index + 1].get_name() + ")"

    return dag_string


# FOR TESTING
# Gets a list of DAG objects from a json file containing UI output, using filename
def get_commands_from_filename( recipe_filename ):

    with open( recipe_filename, "r", ) as file:
        recipe = json.load( file )

        mission = recipe["mission"]
        output = recipe["output"]
        tasks = recipe["tasks"]
        images = recipe["images"]
        sources = recipe["sources"]

        commands = []
        dag_objects = []

        if( images == [] ):
            for source in sources:
                images.append( source.split("/")[-1] )
                commands.append( WGETCommandObject( source.split("/")[-1].split(".")[0], source ) )
                commands.append( WGETCommandObject( source.split("/")[-1].split(".")[0] + "lbl", source.replace( ".img", ".lbl" ) ) )

        for image in images:
            file_index = 0
            for task in tasks:
                parameters = task[1]
                for index in range( len( parameters ) ):
                    if( parameters[index][0] == "from" ):
                        if( "2isis" in task[0] ):
                            if(task[0] == "gllssi2isis"):
                                parameters[index][1] = "img/" + image.split(".")[0] + ".lbl"
                            else:
                                parameters[index][1] = "img/" + image
                        else:
                            parameters[index][1] = "out/" + image.split(".")[0] + str(file_index) + ".cub"
                    elif( parameters[index][0] == "to" ):
                        file_index += 1
                        if( task[0] == "isis2std" ):
                            parameters[index][1] = "out/" + image.split(".")[0] + "." + parameters[-1][1]
                        else:
                            parameters[index][1] = "out/" + image.split(".")[0] + str(file_index) + ".cub"

                commands.append( CommandObject( task[0] + image.split(".")[0], task[0], copy.deepcopy( parameters ) ) )

        for command in commands:
            dag_objects.append( DAGObject( command ) )

        return dag_objects


# DEPRECATED
# Gets a list of DAG objects from a json file containing UI output, using file
def get_commands_from_file( recipe_file ):

    recipe = json.load( file )

    mission = recipe["mission"]
    output = recipe["output"]
    tasks = recipe["tasks"]
    images = recipe["images"]
    sources = recipe["sources"]

    commands = []
    dag_objects = []

    if( images == [] ):
        for source in sources:
            images.append( source.split("/")[-1] )
            commands.append( WGETCommandObject( source ) )

    for image in images:
        for task in tasks:
            print( task )
            parameters = task[1]
            for index in range( len( parameters ) ):
                if( parameters[index][0] == "from" ):
                    if( "2isis" in task[0] ):
                        parameters[index][1] = "img/" + image
                    else:
                        parameters[index][1] = "out/" + image.split(".")[0] + ".cub"
                elif( parameters[index][0] == "to" ):
                    parameters[index][1] = "out/" + image.split(".")[0] + ".cub"

            commands.append( CommandObject( task[0], task[1] ) )

    for command in commands:
        dag_objects.append( DAGObject( command ) )
    return dag_objects


# Gets a list of DAG objects from a json file containing UI output, using json object
def get_commands_from_json( recipe ):

    # with open( recipe_filename, "r", ) as file:
    #     recipe = json.load( file )

        mission = recipe["mission"]
        output = recipe["output"]
        tasks = recipe["tasks"]
        images = recipe["images"]
        sources = recipe["sources"]

        commands = []
        dag_objects = []

        if( images == [] ):
            for source in sources:
                images.append( source.split("/")[-1] )
                commands.append( WGETCommandObject( source.split("/")[-1].split(".")[0], source ) )
                if(mission == "galileo_ssi_edr"):
                    commands.append( WGETCommandObject( source.split("/")[-1].split(".")[0] + "lbl", source.replace( ".img", ".lbl" ) ) )

        for image in images:
            file_index = 0
            for task in tasks:
                parameters = task[1]
                for index in range( len( parameters ) ):
                    if( parameters[index][0] == "from" ):
                        if( "2isis" in task[0] ):
                            if(task[0] == "gllssi2isis"):
                                parameters[index][1] = "img/" + image.split(".")[0] + ".lbl"
                            else:
                                parameters[index][1] = "img/" + image
                        else:
                            parameters[index][1] = "out/" + image.split(".")[0] + str(file_index) + ".cub"
                    elif( parameters[index][0] == "to" ):
                        file_index += 1
                        if( task[0] == "isis2std" ):
                            parameters[index][1] = "out/" + image.split(".")[0] + "." + parameters[-1][1]
                        else:
                            parameters[index][1] = "out/" + image.split(".")[0] + str(file_index) + ".cub"

                commands.append( CommandObject( task[0] + image.split(".")[0], task[0], copy.deepcopy( parameters ) ) )

        for command in commands:
            dag_objects.append( DAGObject( command ) )

        return dag_objects


# Generates a pipeline job
# TODO: Improve identification of job
# TODO: Change data to recipe
# Parameter is JSON recipe
def generate( data ):

    dag_objects = get_commands_from_json( data )
    dag_string = generate_dag( dag_objects )
    timestamp = datetime.now().strftime( "%Y_%m_%d_%H_%M_%S" )
    with open( DAG_DIRECTORY + timestamp + ".py", "w" ) as job_file:
        job_file.write( dag_string )


# Tests generator library import
def test():

    return "Test successful response."



# ------------------------------------------------------------------------------
# Main -------------------------------------------------------------------------
# ------------------------------------------------------------------------------


if( __name__ == "__main__" and TEST ):
    commands = get_commands_from_filename( TEST_FILE )
    dag = generate_dag( commands )
    print( dag )
