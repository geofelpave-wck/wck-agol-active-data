import os
from http import HTTPStatus

import flask
from flask.typing import ResponseReturnValue
from flask.wrappers import Response

from utils.multiroute_context import internal_context
import utils.wck_bq_data_api as wck_bq
import utils.wck_agol_fs as wck_fs

# This app object allows for multiple endpoints in a functions-framework app.
app = flask.Flask("internal")
# See multiroute_context.py for code on handling custom routing.


# === ROUTES === :
#  - Can put your application logic in functions marked by @app.route
#  - In requests to cloud function, send to corresponding path (e.g. "/healthcheck")


@app.route("/healthcheck", methods=["GET"])
def health_check() -> ResponseReturnValue:
    return flask.jsonify({"status": "OK"}), HTTPStatus.OK


# @app.route("/echo", methods=["POST"])
# def echo() -> ResponseReturnValue:
#     """Echo HTTP endpoint (JSON) to act as toy example"""
#     try:
#         request_json = flask.request.get_json()
#         request_args = flask.request.args

#         return flask.jsonify(
#             {"Received": {"args": request_args, "json": request_json}}
#         ), HTTPStatus.OK

#     except Exception as e:
#         return flask.jsonify(
#             {"error": f"Internal error: {str(e)}"}
#         ), HTTPStatus.INTERNAL_SERVER_ERROR

@app.route("wck_active", methods=["POST"])
def wck_active(request):
    
    agol_user = os.environ.get('agol_user')
    agol_pass = os.environ.get('agol_pass')
    wck_token = os.environ.get('wck_token')
    agol_item = os.environ.get('agol_item')


    # Make the POST request
    api_data = wck_bq.wck_api(wck_token)

    # Working in AGOL
    '''Upload new WCK data to AGOL'''
    agol_update = wck_fs.wfs_agol(agol_user, agol_pass, api_data, agol_item)
    
    return (f"\n --- \n "
            f"\n --- \n")


# === MAIN ENTRY POINT ===
def run(request: flask.Request):
    """
    Main entry point for Cloud Functions.
    Routes requests based on path to the handlers registered with the @app.route decorator.

    NOTE: You shouldn't need to ever change this function, it's just for cloud run.
        * Ask Alex if anything breaks here -- it should be fixed in the template.

    NOTE: The name of this function needs to match
        * `--entry-point` flag when using gcloud functions deploy (makefile or CLI)
        * `--target` flag when running locally with `functions-framework` command

    See multiroute_context.py for code on handling custom routing.
    """

    with internal_context(app, request):
        return_value: Response = app.full_dispatch_request()

    return return_value
