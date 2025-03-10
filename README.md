# geo-loc
Code exercise for developing a geolocation utility in python.  The utility will return a longitude and latitude results 
and be called using command line options, examples are list below:
- python cli.py --zipcode=18929
- python cli.py --city=Philadelphia --state=PA
- python cli.py --multi_location 18929#Philadelphia,PA

A help menu is also available using the `--help option` when calling `cli.py` 

### project configuration
The project using pipenv to install the necessary dependencies and set up a virtual env.  There is also a [config.properties](./conf/config.properties) 
file that contains the base_url for the api being called and the api_key or appId
