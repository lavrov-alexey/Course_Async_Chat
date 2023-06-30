import unittest

from server import process_client_message
from common.variables import ACTION, TIME, USER, ACCOUNT_NAME, RESPONSE, ERROR,\
    BAD_REQUEST, PRESENCE, GUEST

TEST_TIME = 77.77
BAD_RESPONSE = {
        RESPONSE: 400,
        ERROR: BAD_REQUEST
    }


class TestProcessClientMessage(unittest.TestCase):

    def test_proc_client_msg_ok(self):
        test_msg = {
            ACTION: PRESENCE,
            TIME: TEST_TIME,
            USER: {ACCOUNT_NAME: GUEST}
        }
        self.assertEqual(process_client_message(test_msg), {RESPONSE: 200})

    def test_proc_client_msg_no_action(self):
        test_msg = {
            TIME: TEST_TIME,
            USER: {}
        }
        self.assertEqual(process_client_message(test_msg), BAD_RESPONSE)

    def test_proc_client_msg_wrong_action(self):
        test_msg = {
            ACTION: 'unknown action',
            TIME: TEST_TIME,
            USER: {}
        }
        self.assertEqual(process_client_message(test_msg), BAD_RESPONSE)

    def test_proc_client_msg_no_time(self):
        test_msg = {
            ACTION: PRESENCE,
            USER: {}
        }
        self.assertEqual(process_client_message(test_msg), BAD_RESPONSE)

    def test_proc_client_msg_no_user(self):
        test_msg = {
            ACTION: PRESENCE,
            TIME: TEST_TIME,
        }
        self.assertEqual(process_client_message(test_msg), BAD_RESPONSE)

    def test_proc_client_msg_no_acc_name(self):
        test_msg = {
            ACTION: PRESENCE,
            TIME: TEST_TIME,
            USER: {'not account name': ''}
        }
        self.assertEqual(process_client_message(test_msg), BAD_RESPONSE)

        test_msg = {
            ACTION: PRESENCE,
            TIME: TEST_TIME,
            USER: {ACCOUNT_NAME: 'alien'}
        }
        self.assertEqual(process_client_message(test_msg), BAD_RESPONSE)


if __name__ == '__main__':
    unittest.main()
