from webapp import db
from sqlalchemy.sql.expression import and_

class AutoPilotHandlerModel(db.Model):

    __tablename__ = 'auto_pilot_messages'

    id = db.Column(db.BigInteger, primary_key=True)
    timestamp = db.Column(db.DateTime)
    current_task = db.Column(db.String(100))
    memory = db.Column(db.String(4000))
    channel = db.Column(db.String(100))
    next_best_task = db.Column(db.String(100))
    current_task_confidence = db.Column(db.String(10))
    account_sid = db.Column(db.String(35))
    callback_source = db.Column(db.String(35))
    current_input = db.Column(db.String(512))
    dialogue_sid = db.Column(db.String(35))
    dialogue_payload_url = db.Column(db.String(255))
    query_sid = db.Column(db.String(35))
    assistant_sid = db.Column(db.String(35))
    user_identifier = db.Column(db.String(15))
    _message_response = db.Column(db.String(512))
    _user_sequence = db.Column(db.BigInteger)
    _feedback_for_code = db.Column(db.String(5))
    _hide = db.Column(db.Integer)

    def __init__(self,
                 timestamp=None,
                 current_task=None,
                 memory=None,
                 channel=None,
                 next_best_task=None,
                 current_task_confidence=None,
                 account_sid=None,
                 callback_source=None,
                 current_input=None,
                 dialogue_sid=None,
                 dialogue_payload_url=None,
                 query_sid=None,
                 assistant_sid=None,
                 user_identifier=None,
                 _message_response=None,
                 _user_sequence=None,
                 _feedback_for_code=None,
                 _hide=0):
        self.timestamp = timestamp
        self.current_task = current_task
        self.memory = memory
        self.channel = channel
        self.next_best_task = next_best_task
        self.current_task_confidence = current_task_confidence
        self.account_sid = account_sid
        self.callback_source = callback_source
        self.current_input = current_input
        self.dialogue_sid = dialogue_sid
        self.dialogue_payload_url = dialogue_payload_url
        self.query_sid = query_sid
        self.assistant_sid = assistant_sid
        self.user_identifier = user_identifier
        self._message_response = _message_response
        self._user_sequence = _user_sequence
        self._feedback_for_code = _feedback_for_code
        self._hide = _hide


    @classmethod
    def find_by_from_phone_number(cls, user_identifier):
        return cls.query.filter_by(user_identifier=user_identifier).first()

    @classmethod
    def get_count_of_phone_number(cls, user_identifier):
        return cls.query.filter(and_(cls.user_identifier == user_identifier, cls._user_sequence != "-1")).count()

    @classmethod
    def get_last_100_messages_by_current_task(cls, current_task):
        return db.session.query(cls).filter_by(current_task=current_task, _hide=0).order_by(
            cls.timestamp.desc()).limit(100)

    @classmethod
    def get_cpt_code_for_feedback(cls, user_identifier, feedback_user_sequence):
        cpt_code_sequence = feedback_user_sequence - 1
        return db.session.query(cls.current_input).filter_by(current_task='cpt_code_provided', user_identifier=user_identifier, _user_sequence=cpt_code_sequence).first()

    def upsert(self):
        db.session.add(self)
        db.session.commit()

    def json(self):
        return {
            'timestamp': self.timestamp,
            'current_task': self.current_task,
            'memory': self.memory,
            'channel': self.channel,
            'next_best_task': self.next_best_task,
            'current_task_confidence': self.current_task_confidence,
            'account_sid': self.account_sid,
            'callback_source': self.callback_source,
            'current_input': self.current_input,
            'dialogue_sid': self.dialogue_sid,
            'dialogue_payload_url': self.dialogue_payload_url,
            'query_sid': self.query_sid,
            'assistant_sid': self.assistant_sid,
            'user_identifier': self.user_identifier,
            '_message_response': self._message_response,
            '_user_sequence': self._user_sequence,
            '_feedback_for_code': self._feedback_for_code,
            '_hide': self._hide
        }