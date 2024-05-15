import json
import requests

class AppMonnify:
    """
    Class AppMonnify
    """
    def __init__(self):
        """
        Constructor method for the AppMonnify class.
        Initializes the Monnify API configuration and sets the authentication header.
        """
        # Define Monnify API configuration settings
        self.mfConfig = {
            'IPN_secret': 'your_IPN_secret_here',
            'addon_currency': 'your_addon_currency_here'
        }

        # Check if configuration is valid
        if 'IPN_secret' not in self.mfConfig or 'addon_currency' not in self.mfConfig:
            raise RuntimeError('Missing or invalid configuration for Monnify API')

        # Set authentication header
        self.authenticationHeader = base64.b64encode(f"{self.mfConfig['public_key']}:{self.mfConfig['secret_key']}".encode()).decode()

        # Define base URL for Monnify API requests
        self.baseURL = 'https://sandbox.monnify.com/api/'

        # Define lengths
        self.accountNumberLength = 10
        self.mobileNumberLength = 11
        self.NINLength = 11
        self.BVNLength = 11

    def init_transaction(self, params=None):
        """
        Initializes a new transaction with the provided data.

        Args:
            params (dict): The data for initializing the transaction.

        Returns:
            dict: The response body of the initialized transaction.

        Raises:
            RuntimeError: If the initialization process fails.
        """
        try:
            if params is None:
                params = {}

            data = {
                'contractCode': self.mfConfig['IPN_secret'],
                'currencyCode': self.mfConfig['addon_currency'],
                'paymentReference': self.generate_random_string(10),
                'paymentMethods': ["CARD", "ACCOUNT_TRANSFER"]
            }
            data.update(params)
            new_data = json.dumps(data)

            headers = {
                'Authorization': f'Basic {self.authenticationHeader}',
                'Content-Type': 'application/json'
            }

            url = self.baseURL + 'v1/merchant/transactions/init-transaction'
            response = requests.post(url, headers=headers, data=new_data)
            
            if response.status_code != 200:
                raise RuntimeError('Unexpected HTTP status code: ' + str(response.status_code))

            res = response.json()
            if 'responseBody' not in res:
                raise RuntimeError('Failed to decode response or responseBody not found')

            return res['responseBody']
        except Exception as e:
            raise RuntimeError('Failed to initialize transaction: ' + str(e))

    def generate_random_string(self, length):
        """
        Generates a random string of specified length.

        Args:
            length (int): Length of the random string.

        Returns:
            str: The generated random string.
        """
        # Implement your random string generation logic here
        pass

if __name__ == "__main__":
    # Instantiate the AppMonnify class
    app_monnify = AppMonnify()
    # Example of initializing a transaction
    transaction_params = {
        'additional_key': 'additional_value'
    }
    transaction_response = app_monnify.init_transaction(transaction_params)
    print("Transaction Response:", transaction_response)
