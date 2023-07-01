import unittest
from os import remove
from os.path import exists
from socket import socket, AF_INET, SOCK_STREAM

from common.utils import detect_encode

FILE_UTF_8 = 'test_file_utf-8.tst'
FILE_CP1251 = 'test_file_cp1251.tst'
ENC_UTF_8 = 'utf-8'
ENC_CP1251 = 'windows-1251'
TEST_STR = 'Тестовый файл в кодировке '


class TestUtils(unittest.TestCase):

    def setUp(self) -> None:
        with open(FILE_UTF_8, 'w', encoding=ENC_UTF_8) as f:
            f.write(TEST_STR + ENC_UTF_8)

        with open(FILE_CP1251, 'w', encoding=ENC_CP1251) as f:
            f.write(TEST_STR + ENC_CP1251)

    def tearDown(self) -> None:
        if exists(FILE_UTF_8):
            remove(FILE_UTF_8)
        if exists(FILE_CP1251):
            remove(FILE_CP1251)

    # ================ detect_encode ================
    def test_encode_utf_8(self):
        self.assertEqual(detect_encode(FILE_UTF_8), ENC_UTF_8)

    def test_encode_cp1251(self):
        self.assertEqual(detect_encode(FILE_CP1251), ENC_CP1251)

    def test_encode_no_file(self):
        self.assertRaises(SystemExit, detect_encode, '')

    def test_encode_wo_param(self):
        self.assertRaises(TypeError, detect_encode, )


if __name__ == '__main__':
    unittest.main()
