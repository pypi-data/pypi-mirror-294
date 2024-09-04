import os
import requests
import logging

# Set up logging for the module
logger = logging.getLogger(__name__)

def get_customers_managed(api_baseurl, api_key):
    """
    Retrieve a list of managed customers from the API.
    
    Parameters:
        api_baseurl (str): The base URL of the API.
        api_key (str): The API key for authentication.
    
    Returns:
        list: A list of managed customers.
    
    Raises:
        ValueError: If the API base URL is not provided.
        HTTPError: If the API request fails.
    """
    if not api_baseurl:
        raise ValueError("API base URL must be provided.")
    if not api_key:
        raise ValueError("API key must be provided.")
    
    
    url = f'{api_baseurl}/customers'
    headers = {
        'Authorization': 'Bearer ' + api_key,
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        all_customers = response.json()

        # Validate response structure
        if not isinstance(all_customers, list):
            logger.error(f"Unexpected response structure: {all_customers}")
            raise ValueError("API did not return a list of customers.")
        
        managed_customers = []
        for customer in all_customers:
            if 'properties' in customer and customer['properties'].get("Managed Status") == 35984:
                managed_customers.append(customer)

        return managed_customers
    
    except requests.exceptions.RequestException as ex:
        logger.error(f"An error occurred while fetching managed customers: {ex}")
        raise  # Re-raise the exception so the caller can handle it

