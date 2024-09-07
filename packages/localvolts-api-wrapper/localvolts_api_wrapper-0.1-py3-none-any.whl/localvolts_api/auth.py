class LocalvoltsAuth:
    def __init__(self, api_key, partner_id):
        """
        Initialize the LocalvoltsAuth class with the given API key and Partner ID.

        :param api_key: str - The API key for authenticating with the Localvolts API.
        :param partner_id: str - The Partner ID for authenticating with the Localvolts API.
        """
        self.api_key = api_key
        self.partner_id = partner_id

    def get_headers(self):
        """
        Generate headers for API requests.

        :return: dict - A dictionary containing the necessary headers for API authentication.
        """
        return {
            'Authorization': f'ApiKey {self.api_key}',
            'Partner-ID': self.partner_id
        }
