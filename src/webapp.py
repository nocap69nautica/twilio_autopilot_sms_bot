from flask import Flask, render_template
from flask_restful import Api
from flask_moment import Moment
from common.database import db
from models.auto_pilot_handler import AutoPilotHandlerModel
from resources.auto_pilot_handler import AutoPilotHandler, FeedbackHandler
from socket import gethostname
import logging
import os

webapp = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)
webapp.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI')
webapp.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
webapp.config['SQLALCHEMY_POOL_RECYCLE'] = 299
webapp.config['SQLALCHEMY_POOL_TIMEOUT'] = 20
webapp.secret_key = os.environ.get('APP_SECRET_KEY')
moment = Moment(webapp)
api = Api(webapp)
with webapp.app_context():
    db.init_app(webapp)

@webapp.before_first_request
def create_tables():
    db.create_all()

api.add_resource(AutoPilotHandler, '/autopilot_handler')
api.add_resource(FeedbackHandler, '/feedback_handler')

@webapp.route('/')
def index():
    last_100_initial_query = AutoPilotHandlerModel.get_last_100_messages_by_current_task("cpt_code_provided")
    initial_messages = []
    for result in last_100_initial_query:
        initial_messages.append(result)
    last_100_feedback_query = AutoPilotHandlerModel.get_last_100_messages_by_current_task("collect_feedback")
    feedback_messages = []
    for result in last_100_feedback_query:
        if result._feedback_for_code:
            feedback_messages.append(result)
    return render_template("base.html", initial_messages=initial_messages, feedback_messages=feedback_messages)

if __name__ == '__main__':
    if 'liveconsole' not in gethostname():
        webapp.run(host='0.0.0.0', port=8088, debug=True)