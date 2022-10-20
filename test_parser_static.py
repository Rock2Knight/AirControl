from unittest import TestCase, main
from parser_static import ParserStatic

class TestParserStatic(TestCase):

    def setUp(self):
        self.ParserStatic = ParserStatic()

    def test_day_and_time(self):
        self.assertEqual(self.ParserStatic.day_and_time('2021-05-01 12:06:23'), ('12:06:23', 1))

if __name__ == '__main__':
    main()
