# ------------------------------------------------------------------------------
# Imports ----------------------------------------------------------------------
# ------------------------------------------------------------------------------


import generator
import os
import json

from flask import Flask, request
from flask_restful import Resource, Api
from generator import DAG_DIRECTORY



# ------------------------------------------------------------------------------
# Constants --------------------------------------------------------------------
# ------------------------------------------------------------------------------


REST_API_PORT = 5001

api_app = Flask( __name__ )
api = Api( api_app )



# ------------------------------------------------------------------------------
# Classes ----------------------------------------------------------------------
# ------------------------------------------------------------------------------


class PipelineJob( Resource ):
    """A class that represents a POST endpoint for pipeline job submission.
    """

    def post( self, job_id ):
        """A function to handle requests made to the REST API. This function
        also contains a routine for testing the communication of the API to the
        generator library.

        TODO:
            * Rework identifier for generation failure due to parameter error.

        :param job_id: A job identifier in the form of the timestamp of when the job request was first made.
        :returns: A REST response depending on the result of the generation process.
        """

        if( job_id == "test" ):
            try:
                print( generator.test() )
            except:
                return { "Response": "Test failed." }

            return { "Response": generator.test() }

        if( job_id == "submit" ):
            try:
                if( not generator.generate( json.loads( request.data ) ) ):
                    return { "Response": "parameter error" }
            except:
                return { "Response": "Generation failed." }

            return { "Response": "Generation successful." }

        return { "Response": "Unsupported request." }


api.add_resource( PipelineJob, "/<string:job_id>" )



# ------------------------------------------------------------------------------
# Main -------------------------------------------------------------------------
# ------------------------------------------------------------------------------


if( __name__ == "__main__" ):

    directory = os.getcwd()
    if ( "\\" in directory ):
        directory += "\\dags"
    else:
        directory += "/dags"

    if( not os.path.exists( directory ) ):
        os.makedirs( directory )

    api_app.run( port=REST_API_PORT, debug=True )
