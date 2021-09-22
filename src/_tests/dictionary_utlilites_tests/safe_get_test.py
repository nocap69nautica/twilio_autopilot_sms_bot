import unittest
from webapp import webapp, db
from common.utilities.dictionary_utils import DictionaryUtils

class SafeGetTest(unittest.TestCase):

    def test_safe_get_key_is_valid(self):
        with webapp.app_context():
            payload = {
                        "CurrentTask": "cpt_code_provided",
                        "Memory": {
                            "twilio": {
                                "chat": {
                                    "ChannelSid": "",
                                    "AssistantName": "",
                                    "Attributes": {},
                                    "ServiceSid": "",
                                    "Index": 83,
                                    "From": "user",
                                    "MessageSid": ""
                                },
                                "collected_data": {
                                    "collect_comments": {
                                        "answers": {
                                            "isFeedback": {
                                                "confirm_attempts": 0,
                                                "answer": "yes",
                                                "filled": True,
                                                "confirmed": False,
                                                "validate_attempts": 1,
                                                "attempts": 1
                                            }
                                        },
                                        "date_completed": "2021-07-10T01:23:38Z",
                                        "date_started": "2021-07-10T01:23:30Z",
                                        "status": "complete"
                                    }
                                }
                            }
                        },
                        "Channel": "chat",
                        "NextBestTask": "collect_feedback",
                        "CurrentTaskConfidence": "0.82",
                        "AccountSid": "",
                        "CallbackSource": "None",
                        "CurrentInput": "1111",
                        "DialogueSid": "",
                        "DialoguePayloadUrl": "",
                        "QuerySid": "None",
                        "AssistantSid": "",
                        "UserIdentifier": "user"
                    }
            self.assertEqual(DictionaryUtils.safe_get(payload, 'Memory.twilio.collected_data.collect_comments.answers.isFeedback.answer'), 'yes')

    def test_safe_get_key_is_none(self):
        with webapp.app_context():
            payload = {
                        "CurrentTask": "cpt_code_provided",
                        "Memory": {
                            "twilio": {
                                "chat": {
                                    "ChannelSid": "",
                                    "AssistantName": "",
                                    "Attributes": {},
                                    "ServiceSid": "",
                                    "Index": 83,
                                    "From": "user",
                                    "MessageSid": ""
                                }
                            }
                        },
                        "Channel": "chat",
                        "NextBestTask": "collect_feedback",
                        "CurrentTaskConfidence": "0.82",
                        "AccountSid": "",
                        "CallbackSource": "None",
                        "CurrentInput": "1111",
                        "DialogueSid": "",
                        "DialoguePayloadUrl": "",
                        "QuerySid": "None",
                        "AssistantSid": "",
                        "UserIdentifier": "user"
                    }
            self.assertIsNone(DictionaryUtils.safe_get(payload, 'Memory.twilio.collected_data.collect_comments.answers.isFeedback.answer'))

if __name__ == '__main__':
    unittest.main()
