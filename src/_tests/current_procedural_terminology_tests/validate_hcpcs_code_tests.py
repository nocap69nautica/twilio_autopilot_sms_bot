import unittest
import os
from webapp import webapp, db
from models.current_procedural_terminology import CurrentProceduralTerminologyModel

class ValidateHcpcsCodeTest(unittest.TestCase):

    def test_only_code_validation_is_true(self):
        with webapp.app_context():
            webapp.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI')
            db.init_app(webapp)
            self.assertTrue(CurrentProceduralTerminologyModel.validate_hcpcs_code('0211T'))

    def test_only_code_validation_is_false(self):
        with webapp.app_context():
            webapp.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI')
            db.init_app(webapp)
            self.assertFalse(CurrentProceduralTerminologyModel.validate_hcpcs_code('XXXXX'))

    def test_embedded_code_validation_is_true(self):
        with webapp.app_context():
            webapp.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI')
            db.init_app(webapp)
            self.assertTrue(CurrentProceduralTerminologyModel.validate_hcpcs_code('Can you run code 0211t please!!!'))

    def test_embedded_code_validation_is_false(self):
        with webapp.app_context():
            webapp.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI')
            db.init_app(webapp)
            self.assertFalse(CurrentProceduralTerminologyModel.validate_hcpcs_code('Can you run code XXXXX please!'))

if __name__ == '__main__':
    unittest.main()
