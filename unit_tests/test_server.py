import unittest
from time import time

from server import process_client_message
from common.variables import ACTION, TIME, USER, ACCOUNT_NAME, RESPONSE, ERROR,\
    BAD_REQUEST, PRESENCE, GUEST

BAD_RESPONSE = {
        RESPONSE: 400,
        ERROR: BAD_REQUEST
    }


class TestProcessClientMessage(unittest.TestCase):

    def test_ok_response(self):
        test_msg = {
            ACTION: PRESENCE,
            TIME: time(),
            USER: {ACCOUNT_NAME: GUEST}
        }
        self.assertEqual(process_client_message(test_msg), {RESPONSE: 200})

    def test_no_action(self):
        test_msg = {
            TIME: time(),
            USER: {}
        }
        self.assertEqual(process_client_message(test_msg), BAD_RESPONSE)

    def test_wrong_action(self):
        test_msg = {
            ACTION: 'unknown action',
            TIME: time(),
            USER: {}
        }
        self.assertEqual(process_client_message(test_msg), BAD_RESPONSE)

    def test_no_time(self):
        test_msg = {
            ACTION: PRESENCE,
            USER: {}
        }
        self.assertEqual(process_client_message(test_msg), BAD_RESPONSE)

    def test_no_user(self):
        test_msg = {
            ACTION: PRESENCE,
            TIME: time()
        }
        self.assertEqual(process_client_message(test_msg), BAD_RESPONSE)

    def test_no_acc_name(self):
        test_msg = {
            ACTION: PRESENCE,
            TIME: time(),
            USER: {'not account name': ''}
        }
        self.assertEqual(process_client_message(test_msg), BAD_RESPONSE)

    def test_acc_name_not_guest(self):
        test_msg = {
            ACTION: PRESENCE,
            TIME: time(),
            USER: {ACCOUNT_NAME: 'alien'}
        }
        self.assertEqual(process_client_message(test_msg), BAD_RESPONSE)


if __name__ == '__main__':
    unittest.main()
