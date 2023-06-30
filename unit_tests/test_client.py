import unittest

from client import create_presense, process_answ
from common.variables import TIME, ACTION, PRESENCE, USER, ACCOUNT_NAME, GUEST,\
    RESPONSE, BAD_REQUEST, ERROR

TEST_TIME = 77.77
REF_PRESENCE = {
    ACTION: PRESENCE,
    TIME: TEST_TIME,
    USER: {ACCOUNT_NAME: GUEST}
    }


class TestClient(unittest.TestCase):
    def test_create_presence_ok(self):
        # создаем сообщение о присутствии
        test_presence = create_presense()
        # время в сообщении нужно зафиксировать, чтобы тест проходил
        test_presence[TIME] = TEST_TIME

        self.assertEqual(test_presence, REF_PRESENCE)

    def test_proc_answ_ok_resp(self):
        self.assertEqual(process_answ({RESPONSE: 200}), '200: OK')

    def test_proc_answ_err_resp(self):
        ERR_RESP = {
            RESPONSE: 400,
            ERROR: BAD_REQUEST
        }
        self.assertEqual(process_answ(ERR_RESP), '400: BAD REQUEST')

    def test_proc_answ_no_resp(self):
        self.assertRaises(ValueError, process_answ, {ERROR: BAD_REQUEST})

if __name__ == '__main__':
    unittest.main()
