"""
Replacement for RUSA ACP brevet time calculator
(see https://rusa.org/octime_acp.html)
"""

import os
import flask
from pymongo import MongoClient
from flask import request
import arrow  
import acp_times 
import db 
import config 

import logging

###
# Globals
###
app = flask.Flask(__name__)
CONFIG = config.configuration()

user = db.Mongodb(os.environ['MONGODB_HOSTNAME'])
user.connect()
user.set_data("brevetsdb")

###
# Pages
###

@app.route("/")
@app.route("/index")
def index():
    app.logger.debug("Main page entry")
    return flask.render_template('calc.html')


@app.errorhandler(404)
def page_not_found(error):
    app.logger.debug("Page not found")
    return flask.render_template('404.html'), 404


@app.route("/insert", methods=["POST"])
def submit():
    input = request.form.to_dict()
    # Converting string representation of list to a list
    input['table'] = eval(input['table'])
    table = input['table']
    # Remove the previous submit result
    user.delete_rows("recent_submitt")

    for i in range(len(table)):
        row = table[str(i)]
        user.insert("recent_submitt", row)
    return flask.jsonify(output=str(input))


@app.route("/display")
def display():
    reach_back = user.list_rows("recent_submitt")
    app.logger.debug(reach_back)
    brevet = begin_date = ""
    if len(reach_back) > 0:
        brevet = reach_back[0]['brevet']
        begin_date = reach_back[0]['begin']
    return flask.render_template('display.html', result=reach_back, brevet=brevet, begin=begin_date)

###############
#
# AJAX request handlers
# These return JSON, rather than rendering pages.
#
###############
@app.route("/_calc_times")
def _calc_times():
    """
    Calculates open/close times from miles, using rules
    described at https://rusa.org/octime_alg.html.
    Expects one URL-encoded argument, the number of miles.
    """
    app.logger.debug("Got a JSON request")
    km = request.args.get('km', 999, type=float)
    brevet_dist = request.args.get('brevet_dist', 200, type=int)
    begin_date = request.args.get('begin_date', '2021-01-01T00:00', type=str)

    app.logger.debug("km={}".format(km))
    app.logger.debug("brevet_dist={}".format(brevet_dist))
    app.logger.debug("begin_date={}".format(begin_date))
    app.logger.debug("request.args: {}".format(request.args))

    open_time = acp_times.open_time(km, brevet_dist, arrow.get(begin_date)).format('YYYY-MM-DDTHH:mm')
    close_time = acp_times.close_time(km, brevet_dist, arrow.get(begin_date)).format('YYYY-MM-DDTHH:mm')
    result = {"open": open_time, "close": close_time}

    return flask.jsonify(result=result)


#############

app.debug = CONFIG.DEBUG
if app.debug:
    app.logger.setLevel(logging.DEBUG)

if __name__ == "__main__":
    print("Using the port {} for global access".format(CONFIG.PORT))
    app.run(port=CONFIG.PORT, host="0.0.0.0")