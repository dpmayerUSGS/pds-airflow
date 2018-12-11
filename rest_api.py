# ------------------------------------------------------------------------------
# Imports ----------------------------------------------------------------------
# ------------------------------------------------------------------------------


import generator

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

    def post( self, job_id ):

        if( job_id == "test" ):
            try:
                with open( DAG_DIRECTORY + "test_file.py", "w" ) as test_file:
                    test_file.write( "test" )
            except:
                return { "Response": "Test failed." }

            return { "Response": generator.test() }

        if( job_id == "dagtest" ):
            #try:
            #    generator.generate( request.form["data"] )
            #except:
            #    return { "Response": "Generation failed." }
            generator.generate( request.form["data"] )

            return { "Response": "Generation successful." }

        return { "Response": "Unsupported request." }


api.add_resource( PipelineJob, "/<string:job_id>" )



# ------------------------------------------------------------------------------
# Main -------------------------------------------------------------------------
# ------------------------------------------------------------------------------


if( __name__ == "__main__" ):
    api_app.run( port=REST_API_PORT, debug=True )
