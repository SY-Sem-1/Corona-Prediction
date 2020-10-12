from json import dump, load, loads
from datetime import datetime
import requests

with open("DATABASE And API Configuration/config.json",'r') as file:
    configuration = load(file)

def api_country():
    current_time = datetime.now()
    current_formatted_time = current_time.strftime("%Y-%m-%dT%H:%M:%SZ")
    
    # Querying to get total whole country stats
    # query_whole_india_stats = f'https://api.covid19api.com/country/india?from=2020-03-01T00:00:00Z&to={current_formatted_time}'
    query_whole_country_stats = configuration["CORONA"]["COUNTRY_DATA_URL"] 
    query_whole_country_stats += current_formatted_time
    res = requests.get(query_whole_country_stats)
    country = res.json()
    
    with open('API Data/country.json','w') as file:
        dump(country,file,indent=4)
    
    country = country[len(country) - 1]
    return country

def api_states():
    # Querying to get state-wise all stats
    query_whole_state_stats = configuration["CORONA"]["STATE_DATA_URL"] 
    res = requests.get(query_whole_state_stats)
    states = res.json()

    with open('API Data/states.json','w') as file:
        dump(states,file,indent=4)
    
    return states