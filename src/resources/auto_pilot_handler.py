from flask_restful import Resource, reqparse
from flask import jsonify
from models.current_procedural_terminology import CurrentProceduralTerminologyModel
from models.auto_pilot_handler import AutoPilotHandlerModel
from common.decorators import validate_twilio_request
from datetime import datetime
import logging
import re
import os

logger = logging.getLogger("webapp")

REGEX_PATTERN = r'\b[a-zA-Z0-9]{7}\b|\b[a-zA-Z0-9]{5}\b'

FEEDBACK_URL = os.environ.get('FEEDBACK_URL')

class AutoPilotHandler(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('CurrentTask',
                        type=str,
                        required=False)
    parser.add_argument('Memory',
                        type=str,
                        required=False)
    parser.add_argument('Channel',
                        type=str,
                        required=False)
    parser.add_argument('NextBestTask',
                        type=str,
                        required=False)
    parser.add_argument('CurrentTaskConfidence',
                        type=str,
                        required=False)
    parser.add_argument('AccountSid',
                        type=str,
                        required=False)
    parser.add_argument('CallbackSource',
                        type=str,
                        required=False)
    parser.add_argument('CurrentInput',
                        type=str,
                        required=False)
    parser.add_argument('DialogueSid',
                        type=str,
                        required=False)
    parser.add_argument('DialoguePayloadUrl',
                        type=str,
                        required=False)
    parser.add_argument('QuerySid',
                        type=str,
                        required=False)
    parser.add_argument('AssistantSid',
                        type=str,
                        required=False)
    parser.add_argument('UserIdentifier',
                        type=str,
                        required=False)

    @validate_twilio_request
    def post(self):
        timestamp = datetime.utcnow()
        data = AutoPilotHandler.parser.parse_args()
        logger.info('autopilot_handler_post begin:--------------------------------')
        logger.info(data)
        logger.info('autopilot_handler_post end:--------------------------------')
        message = AutoPilotHandlerModel(timestamp,
                                        data['CurrentTask'],
                                        data['Memory'],
                                        data['Channel'],
                                        data['NextBestTask'],
                                        data['CurrentTaskConfidence'],
                                        data['AccountSid'],
                                        data['CallbackSource'],
                                        data['CurrentInput'],
                                        data['DialogueSid'],
                                        data['DialoguePayloadUrl'],
                                        data['QuerySid'],
                                        data['AssistantSid'],
                                        data['UserIdentifier']
                                        )

        code = CurrentProceduralTerminologyModel.validate_hcpcs_code(message.current_input)
        user_sequence = AutoPilotHandlerModel.get_count_of_phone_number(message.user_identifier) + 1
        message._user_sequence = user_sequence
        json_payload = {}
        if code and user_sequence % 3 == 0:
            response = CurrentProceduralTerminologyModel.formatted_found_code_response(code)
            message._message_response = response
            json_payload = {
                "actions": [
                    {
                        "say": message._message_response,
                    },
                    {
                        "collect": {
                            "name": "collect_feedback",
                            "questions": [
                                {
                                    "question": "Help us make the CPT bot better by telling us what YOU call this procedure.",
                                    "name": "cptFeedback"
                                }
                            ],
                            "on_complete": {
                                "redirect": FEEDBACK_URL
                            }
                        }
                    }
                ]
            }
            message.upsert()
        elif code:
            response = CurrentProceduralTerminologyModel.formatted_found_code_response(code)
            message._message_response = response
            json_payload = {
                "actions": [
                    {
                        "say": message._message_response
                    }
                ]
            }
            message.upsert()
        elif not bool(re.match(REGEX_PATTERN, message.current_input)):
            message._message_response = "Please enter a 5 character CPT Code."
            message._hide = 1
            message._user_sequence = -1
            json_payload = {
                "actions": [
                    {
                        "say": message._message_response
                    }
                ]
            }
            message.upsert()
        elif not code:
            message._message_response = "Please enter a 5 character CPT Code."
            message._hide = 1
            message._user_sequence = -1
            json_payload = {
                "actions": [
                    {
                        "say": message._message_response
                    }
                ]
            }
            message.upsert()
        return jsonify(json_payload)


class FeedbackHandler(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('CurrentTask',
                        type=str,
                        required=False)
    parser.add_argument('Memory',
                        type=str,
                        required=False)
    parser.add_argument('Channel',
                        type=str,
                        required=False)
    parser.add_argument('NextBestTask',
                        type=str,
                        required=False)
    parser.add_argument('CurrentTaskConfidence',
                        type=str,
                        required=False)
    parser.add_argument('AccountSid',
                        type=str,
                        required=False)
    parser.add_argument('CallbackSource',
                        type=str,
                        required=False)
    parser.add_argument('CurrentInput',
                        type=str,
                        required=False)
    parser.add_argument('DialogueSid',
                        type=str,
                        required=False)
    parser.add_argument('DialoguePayloadUrl',
                        type=str,
                        required=False)
    parser.add_argument('QuerySid',
                        type=str,
                        required=False)
    parser.add_argument('AssistantSid',
                        type=str,
                        required=False)
    parser.add_argument('UserIdentifier',
                        type=str,
                        required=False)

    @validate_twilio_request
    def post(self):
        timestamp = datetime.utcnow()
        data = AutoPilotHandler.parser.parse_args()
        logger.info('feedback_handler_post begin:--------------------------------')
        logger.info(data)
        logger.info('feedback_handler_post end:--------------------------------')

        message = AutoPilotHandlerModel(timestamp,
                                        data['CurrentTask'],
                                        data['Memory'],
                                        data['Channel'],
                                        data['NextBestTask'],
                                        data['CurrentTaskConfidence'],
                                        data['AccountSid'],
                                        data['CallbackSource'],
                                        data['CurrentInput'],
                                        data['DialogueSid'],
                                        data['DialoguePayloadUrl'],
                                        data['QuerySid'],
                                        data['AssistantSid'],
                                        data['UserIdentifier'])

        message.current_task = 'collect_feedback'
        message._message_response = 'Thank you for providing feedback!'
        message._user_sequence = -1

        try:
            user_sequence_for_check = AutoPilotHandlerModel.get_count_of_phone_number(message.user_identifier) + 1
            code_data = AutoPilotHandlerModel.get_cpt_code_for_feedback(message.user_identifier, user_sequence_for_check)
            message._feedback_for_code = code_data['current_input']
        except:
            message._feedback_for_code = None

        message.upsert()

        json_payload = {
            "actions": [
                {
                    "say": message._message_response
                },
                {
                    "listen": True
                }
            ]
        }

        return jsonify(json_payload)