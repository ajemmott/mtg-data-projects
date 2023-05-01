import requests
import pandas as pd

from time import sleep
from loguru import logger

def get_set_data(path_to_data, query):
        
    if path_to_data.exists():
        logger.info(f'\n - previously stored data found. skipping request.\n')
        data = pd.read_json(path_to_data)
        return data
    
    path_to_data.parent.mkdir(parents=True, exist_ok=True)
    
    logger.info(f'\n - requesting api for data...\n')
    data = pd.DataFrame(
        request_card_data(query))
    
    logger.info(f'\n - storing json data for future reference...\n')
    data.to_json(path_to_data)
    
    return data

def request_card_data(query_string):
        """Requests a card _data query to scryfall API and arranges its pagination

        Args:
            query_string (str): the query to be requested. It should follow
            the syntax proposed by scryfall in https://scryfall.com/docs/syntax
        
        Returns:
            list: list of dicts containing the full query card data.
        """
        # Send the query string to the scryfall API. Store the response.    
        response = (requests
                    .get('https://api.scryfall.com/cards/search?q=' + query_string)
                    .json())
        
        data = response['data']
        sleep(0.1)

        # if theres paginated data in the response that, append the data 
        # that follows
        if response['has_more']:
            data += get_next_pages(response['next_page'])

        return data
    
def get_next_pages(next_page):
        """Recursive solution for data pagination

        Args:
            next_page (str): uri of next page of json data

        Returns:
            list: list of dicts containing partial card data.
        """
        # Request the following set of paginated data    
        next_data = requests.get(next_page).json()

        # if there's more paginated data after that, download the data and
        # append the data that follows
        if next_data['has_more']:
            sleep(0.1)
            return next_data['data'] + get_next_pages(next_data['next_page'])

        # if there's no more paginated data, then return the all data found in 
        # pagination
        return next_data['data']
    