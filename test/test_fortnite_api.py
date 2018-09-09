from src import fortnite_api as fa
import os
import unittest
import httpretty
import configparser

class FortniteApiTests(unittest.TestCase):
    def setUp(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        self.api = fa.FortniteApi(config)

    @httpretty.activate
    def test_find_players(self):
        httpretty.register_uri(httpretty.GET, self.api.base_url + 'nardiii',
                           status=200, body=self.read_mock_response('nardiii.json'))
        expected = {
            'kd': '2.55',
            'win_percent': '11.92'
        }
        self.assertEqual(expected, self.api.find_player_kda('nardiii'))

    def read_mock_response(self, file):
        with open(os.path.join(os.path.dirname(__file__), 'api', file), 'r') as f:
            return f.read()
