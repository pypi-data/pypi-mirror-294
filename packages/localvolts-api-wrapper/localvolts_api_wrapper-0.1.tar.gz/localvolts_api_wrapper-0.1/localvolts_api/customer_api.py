import requests

class CustomerIntervalData:
    def __init__(self, json_data):
        self.data = json_data

    def __getattr__(self, item):
        return self.data.get(item, None)

class CustomerAPI:
    BASE_URL = "https://api.localvolts.com/v1"

    def __init__(self, auth):
        """
        Initialize the CustomerAPI with authentication details.

        :param auth: LocalvoltsAuth - An instance of the LocalvoltsAuth class for API authentication.
        """
        self.auth = auth

    def get_interval_data(self, nmi='*', from_time=None, to_time=None):
        """
        Fetches interval data for a given NMI and time range.

        :param nmi: str - The NMI to query. Use '*' for all NMIs.
        :param from_time: str - The start time in ISO 8601 UTC format.
        :param to_time: str - The end time in ISO 8601 UTC format.
        :return: CustomerIntervalData - Custom object containing the response data.
        """
        params = {'NMI': nmi}
        if from_time:
            params['from'] = from_time
        if to_time:
            params['to'] = to_time

        response = requests.get(f"{self.BASE_URL}/customer/interval", headers=self.auth.get_headers(), params=params)
        response.raise_for_status()

        return CustomerIntervalData(response.json())
