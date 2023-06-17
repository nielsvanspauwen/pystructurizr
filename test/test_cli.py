import os
import unittest

from click.testing import CliRunner

from pystructurizr import cli


class CliTest(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()

    def tearDown(self):
        pass

    def test_dump(self):
        result = self.runner.invoke(cli.dump, ['--view', 'example.systemlandscapeview'])

        gold_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'example.gold')
        with open(gold_file, "r", encoding='utf-8') as gfile:
            gold = gfile.read()

        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.output.strip(), gold)

if __name__ == '__main__':
    unittest.main()
