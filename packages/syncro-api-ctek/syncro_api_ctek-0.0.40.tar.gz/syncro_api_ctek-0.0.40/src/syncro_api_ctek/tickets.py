import os
import requests

def get_customers_managed(api_baseurl, api_key):
    url = f'{api_baseurl}/customers'
    headers = {
        'Authorization': 'Bearer ' + api_key,
        'Content-Type': 'application/json'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        all_customers = response.json()
        managed_customers = []
        for customer in all_customers:
            if 'properties' in customer and customer['properties'].get("Managed Status") == 35984:
                managed_customers.append(customer)
        return managed_customers
    except Exception as ex:
        return f"Unexpected error: {ex}"