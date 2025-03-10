from jproperties import Properties
import requests
import click

config = Properties()

with open('../../conf/config.properties', 'rb') as config_file:
    config.load(config_file)
base_url = config.get("base_url").data
api_key = config.get("api_key").data
result_limit = "5"
params = {"limit": result_limit, "appid": api_key}

@click.command('geo_loc')
@click.option('--city', help='The city that you want to search')
@click.option('--state', help='The state you want to search based on the city')
@click.option('--zipcode', help='The zip code you want to search ')
@click.option('--multi_location',help='Enter multiple locations using zip or state and zip code')
def get_loc_info(city, state, zipcode, multi_location):
    if zipcode.isdigit():
        zip_length = len(zipcode)
        if zip_length == 5:
            params['zip'] = f'{zipcode},US'
            response = requests.get(f'{base_url}/zip', params=params)
            click.echo(response.content)
        else:
            click.echo('{"message": "zipcode value is less than 5 digits, please check your value and try again"}')
    elif not zipcode.isdigit():
        click.echo('{"message": "zipcode value can only contain numbers, please check your value and try again"}')
    elif city and state:
        params['q']= f'{city},{state},US'
        response = requests.get(f'{base_url}/direct', params=params)
        click.echo(response.content)
    elif multi_location:
        locations = multi_location.split("#")
        for location in locations:
            if "," not in location:
                params['zip'] = f'{location},US'
                response = requests.get(f'{base_url}/zip', params=params)
                click.echo(response.content)
            elif "," in location:
                city_state = location.split(",")
                params['q'] = f'{city_state[0]},{city_state[1]},US'
                response = requests.get(f'{base_url}/direct', params=params)
                click.echo(response.content)


if __name__ == '__main__':
    get_loc_info()
