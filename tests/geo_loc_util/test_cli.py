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
        assert result["country"] == 'US'
        assert result["zip"] == '18914'
        assert result["lat"] == 40.2892
        assert result["lon"] == -75.2149

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
        # Using state and city produces more precise latitude and longitude results
        result = json.loads(self.runner.invoke(cli.get_loc_info, ['--city',  'Chalfont', '--state','PA']).output)
        assert result[0]["name"] == 'Chalfont'
        assert result[0]["country"] == 'US'
        assert result[0]["state"] == 'Pennsylvania'
        assert result[0]["lat"] == 40.29066735
        assert result[0]["lon"] == -75.21070232492798

    def test_command_with_valid_city_state_for_major_city(self):
        # Using state and major city produced incorrect results as shown below
        result = json.loads(self.runner.invoke(cli.get_loc_info, ['--city',  'Philadelphia', '--state','PA']).output)
        assert result[0]["name"] == 'Philadelphia'
        assert result[0]["country"] == 'US'
        assert result[0]["state"] == 'Pennsylvania'
        assert result[1]["name"] == 'Philadelphia'
        assert result[1]["country"] == 'US'
        assert result[1]["state"] == 'Pennsylvania'


    def test_command_with_valid_city_and_state_code_less_than_two(self):
        result = json.loads(self.runner.invoke(cli.get_loc_info, ['--city',  'Chalfont', '--state','P']).output)
        assert result["message"] == 'state codes can only be to 2 characters long, please check your value and try again'

    def test_command_with_valid_city_and_state_code_greater_than_two(self):
        result = json.loads(self.runner.invoke(cli.get_loc_info, ['--city',  'Chalfont', '--state','PEN']).output)
        assert result["message"] == 'state codes can only be to 2 characters long, please check your value and try again'

    def test_command_with_valid_city_and_invalid_state_code(self):
        result = json.loads(self.runner.invoke(cli.get_loc_info, ['--city',  'Chalfont', '--state','ZZ']).output)
        assert len(result) == 0

    def test_command_with_multiple_locations(self):
        result = self.runner.invoke(cli.get_loc_info, ['--multi_location', '18914#Hatboro,PA']).output.split('\n')
        first_result = json.loads(result[0])
        second_result = json.loads(result[1])
        assert first_result["name"] == 'Bucks County'
        assert second_result[0]["name"] == 'Hatboro'

