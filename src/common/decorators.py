from flask import request, abort
from functools import wraps
from twilio.request_validator import RequestValidator
import os


def validate_twilio_request(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        validator = RequestValidator(os.environ.get('TWILIO_KEY'))

        request_valid = validator.validate(
            request.url,
            request.form,
            request.headers.get('X-TWILIO-SIGNATURE', ''))

        if request_valid:
            return f(*args, **kwargs)
        else:
            return abort(403)
    return decorated_function
