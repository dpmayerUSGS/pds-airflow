# ------------------------------------------------------------------------------
# Imports ----------------------------------------------------------------------
# ------------------------------------------------------------------------------


import json
import copy

from datetime import datetime

# May be unnecessary
# import sys



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
    """An object that holds an ISIS command for easy representation in a :term:`DAG`.
    """

    def __init__( self, name, command, parameters ):
        """Makes things.
        """

        self.command = command
        self.parameters = parameters
        self.name = name

    def __str__( self ):
        """Makes the things a string.
        """

        output = self.command

        for parameter in self.parameters:
            if(parameter[1] != "default"):
                output += " " + parameter[0] + "="
                if(parameter[0] == "from" or parameter[0] == "to"):
                    output += "/"
                output += parameter[1]

        return output


class WGETCommandObject:
    """An object that holds a wget command, used for pulling mission imagery
       from the USGS archive.
    """

    def __init__( self, name, parameter ):
        """Makes things.
        """

        self.command = "cd /img && wget"
        self.parameter = parameter
        self.name = "wget" + name

    def __str__( self ):
        """Makes things a string.
        """

        return self.command + " " + self.parameter


class DAGObject:
    """An object that contains a command object with additional behavior for
       representing the command in a :term:`DAG`.
    """

    # Command is a CommandObject
    def __init__( self, command ):
        """Makes things.
        """

        self.command = command

    def __str__( self ):
        """Makes things a string.
        """

        output = '''%s = BashOperator(
    task_id="%s",
    bash_command= prefix + "%s",
    retries=3,
    dag=dag
)'''

        output = output % (self.command.name, self.command.name, str(self.command))

        return output

    def get_name( self ):
        """A helper function that retrieves a command's name.
        """

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
    """A function that converts reformatted user request data into a string
       representation of an executable :term:`DAG`.

    :param dag_objects: Reformatted user request data.

    :returns: A string containing the :term:`DAG` corresponding to the user request.
    """

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

dag = DAG( "%s", default_args=default_args, schedule_interval="@once" )

prefix = 'source activate PDS-Pipelines && python /opt/conda/envs/PDS-Pipelines/scripts/isis3VarInit.py && source activate PDS-Pipelines && '
'''

    for dag_object in dag_objects:
        dag_string += "\n\n" + str( dag_object )

    dag_string += "\n" + dag_objects[0].get_name()

    for index in range( 1, len( dag_objects ) ):
        dag_string += "\n" + dag_objects[index].get_name() + ".set_upstream(" + dag_objects[index - 1].get_name() + ")"

    return dag_string


# FOR TESTING
# Gets a list of DAG objects from a json file containing UI output, using filename
def get_commands_from_filename( recipe_filename ):
    """A function for testing :term:`DAG` generation based on a fixed user request found
       in a local JSON file. Used for testing potential changes to
       :func:`get_commands_from_json` as well as ensuring
       :func:`generate_dag` is operating correctly.

    :param recipe_filename: The name of a JSON file containing a user request.
    :returns: A reformatted user request.
    """

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
    """A function that reformats user request data to make it easier to convert
       this data to a final, executable :term:`DAG`. Before making changes to this
       function, make sure to test your changes using
       :func:`get_commands_frome_filename`.

    :param recipe: A JSON object representation of a user's job request.
    :returns: A reformatted user request.
    """

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

    # Iterates over the supplied images.
    for image in images:
        file_index = 0
        # Iterates over the supplied ISIS commands for the specified image.
        for task in tasks:
            parameters = task[1]
            # Iterates over the parameters of the specified ISIS command.
            for index in range( len( parameters ) ):
                if( "from" in parameters[index][0] ):
                    # Deals with the fact that some recipes have from_
                    # as a parameter, despite it not being valid.
                    if( parameters[index][0] == "from_" ):
                        parameters[index][0] = parameters[index][0].replace( "_", "" )
                    if( "2isis" in task[0] ):
                        # Handles the need of .lbl files for gllssi.
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

            # Performs a deepcopy to retrieve parameters for individual
            # commands, preventing other commands from overwriting them.
            commands.append( CommandObject( task[0] + image.split(".")[0], task[0], copy.deepcopy( parameters ) ) )

    for command in commands:
        dag_objects.append( DAGObject( command ) )

    return dag_objects


# Generates a pipeline job
# TODO: Improve identification of job
# TODO: Change data to recipe
# Parameter is JSON recipe
def generate( data ):
    """A function that drives the generation process.

    :param data: Original user request data.
    :returns: Success or failure status of generation.
    """

    dag_objects = get_commands_from_json( data )
    dag_string = generate_dag( dag_objects )
    timestamp = datetime.now().strftime( "%Y_%m_%d_%H_%M_%S" )
    with open( DAG_DIRECTORY + timestamp + ".py", "w" ) as job_file:
       job_file.write( dag_string % timestamp )
    if( TEST ):
        print( dag_string % timestamp )


# Tests generator library import
def test():
    """A function for testing the ability of the REST API to respond to requests.

    :returns: Successful test response.
    """

    return "Test successful response."



# ------------------------------------------------------------------------------
# Main -------------------------------------------------------------------------
# ------------------------------------------------------------------------------


if( __name__ == "__main__" and TEST ):
    commands = get_commands_from_filename( TEST_FILE )
    dag = generate_dag( commands )
    print( dag )
