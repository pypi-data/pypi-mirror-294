import requests

class FetchData:
    def __init__(self, client):
        self.client = client

    def fetch(self, gsoName="Equity", limit=5, skipNullFields=True, eql=None, templateName=None, **kwargs):
        """
        Fetch data from the GoldenSource API with optional query parameters.
        
        Args:
            gsoName (str): GSO name (default is "Equity")
            limit (int): Limit on the number of results (default is 5)
            skipNullFields (bool): Whether to skip null fields (default is True)
            eql (str): Entity Query Language condition (optional)
            templateName (str): Template name (optional)
            kwargs: Any additional query parameters
        
        Returns:
            dict: Parsed JSON response from the API.
        """
        # URL endpoint
        endpoint = "gso"

        # Default parameters
        query_params = {
            "gsoName": gsoName,
            "limit": str(limit),
            "skipNullFields": str(skipNullFields).lower(),
        }
        
        # Optional parameters
        if eql:
            query_params["eql"] = eql
        if templateName:
            query_params["templateName"] = templateName
        
        # Add any additional parameters passed in kwargs
        query_params.update(kwargs)

        # Make the GET request
        return self.client.get(endpoint, params=query_params)

