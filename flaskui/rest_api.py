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

    :returns: A REST response depending on the result of the generation process.
    """

    def post( self, job_id ):

        if( job_id == "test" ):
            try:
                print( generator.test() )
            except:
                print( "Test failed." )
                return { "Response": "Test failed." }

            return { "Response": generator.test() }

        if( job_id == "submit" ):
            try:
                print(request.data)
                generator.generate( json.loads( request.data ) )
            except:
                print( "Generation: failed." )
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
