import requests

# Class responsible for handling API communication with Coinbase
class CoinbaseApiClient:
    # Initialization method to properly set the api_url parameter
    def __init__(self, api_url):
        self.api_url = api_url

    # Method to fetch the current Bitcoin Price Index (BPI) 
    def get_current_bpi(self):
        try:
            response = requests.get(self.api_url)
            response.raise_for_status() 
            
            data = response.json()
            
            return float(data['data']['amount'])
        except Exception as e:
            print(f"Error fetching API: {e}")
            return None