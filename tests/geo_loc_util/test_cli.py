import unittest
import json
from click.testing import CliRunner
from src.geo_loc_util import cli


class TestGeoLocationCLI(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()

    def test_command_with_valid_zipcode(self):
        result = json.loads(self.runner.invoke(cli.get_loc_info, ['--zipcode', '18914']).output)
        assert result["name"] == 'Bucks County'

    def test_command_with_non_existing_zipcode(self):
        result = json.loads(self.runner.invoke(cli.get_loc_info, ['--zipcode', '11111']).output)
        assert result["cod"] == '404'
        assert result["message"] == 'not found'

    def test_command_with_zipcode_less_than_five_digits(self):
        result = json.loads(self.runner.invoke(cli.get_loc_info, ['--zipcode', '1111']).output)
        assert result["message"] == 'zipcode value is less than 5 digits, please check your value and try again'

    def test_command_with_zipcode_greater_than_five_digits(self):
        result = json.loads(self.runner.invoke(cli.get_loc_info, ['--zipcode', '111111']).output)
        assert result["message"] == 'zipcode value is less than 5 digits, please check your value and try again'

    def test_command_with_zipcode_with_letters_digits(self):
        result = json.loads(self.runner.invoke(cli.get_loc_info, ['--zipcode', '1111a']).output)
        assert result["message"] == 'zipcode value can only contain numbers, please check your value and try again'

    def test_command_with_valid_city_state(self):
        result = json.loads(self.runner.invoke(cli.get_loc_info, ['--city',  'Chalfont', '--state',' PA']).output)
        assert result[0]["name"] == 'Chalfont'

    def test_command_with_multiple_locations(self):
        result = self.runner.invoke(cli.get_loc_info, ['--multi_location', '18914#Hatboro,PA']).output.split('\n')
        first_result = json.loads(result[0])
        second_result = json.loads(result[1])
        assert first_result["name"] == 'Bucks County'
        assert second_result[0]["name"] == 'Hatboro'

