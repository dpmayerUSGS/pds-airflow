# ------------------------------------------------------------------------------
# Imports ----------------------------------------------------------------------
# ------------------------------------------------------------------------------


import os
import json
import requests

from flask import Flask, request, jsonify
from rest_api import REST_API_PORT



# ------------------------------------------------------------------------------
# Constants --------------------------------------------------------------------
# ------------------------------------------------------------------------------


UI_PORT = 5000



# ------------------------------------------------------------------------------
# Functions --------------------------------------------------------------------
# ------------------------------------------------------------------------------


ui_app = Flask( __name__ + "_ui" )

@ui_app.route( "/" )
def hello_world():

    with open( "ui.html", "r" ) as html:
        return html.read()


@ui_app.route( "/formtest", methods=["POST"] )
def formtest():

    print( request.form )

    for key in request.form.keys():
        print( key, request.form[key] )

    return "Test successful."


@ui_app.route( "/handle_data", methods=["POST"] )
def handle_data():
    print( request.form )
    print( request.form["test"] )
    return "test"


# Sends a simple test
@ui_app.route( "/test" )
def test():

    #os.system( "curl http://localhost:" + str(REST_API_PORT) + "/test -X POST -d \"data=\"" )
    requests.post( "http://localhost:" + str(REST_API_PORT) + "/test", headers={"content-type": "application/json"}, json={} )

    return "test"


# Sends a more complex test, which passes in pre-generated recipe data
# TODO: Make curling nicer
@ui_app.route( "/dagtest" )
def dag_test():

    with open( "REST_json.json", "r" ) as recipe_file:
        recipe_json = json.load( recipe_file )
        #os.system( "curl http://localhost:" + str(REST_API_PORT) + "/dagtest -X POST -d \"data=" + json.dumps(data).replace(" ", "").replace( "\"", "\\\"") + "\"" )
        requests.post( "http://localhost:" + str(REST_API_PORT) + "/dagtest", headers={"content-type": "application/json"}, json=recipe_json )

    return "dag test"



# ------------------------------------------------------------------------------
# Main -------------------------------------------------------------------------
# ------------------------------------------------------------------------------


if( __name__ == "__main__" ):
    ui_app.run( port=UI_PORT, debug=True )
