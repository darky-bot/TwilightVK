from aiohttp import ClientSession, ClientResponse

class Http:

    def __init__(self):
        '''
        This class allows to use HTTP requests asynchronously
        '''
        self.session = None

    async def get(self, url:str, params:dict=None, raw:bool=True) -> ClientResponse | dict:
        '''
        HTTP GET method

        :param url: The url to get the response from
        :type url: str

        :param params: Dictionary containing the optional data to be sent in the GET request
        :type params: dict | None

        :param raw: Defines the raw/json response
        :type raw: bool
        '''
        if self.session is None: self.session = ClientSession()
        response = await self.session.get(url=url, params=params)
        if raw:
            return response
        return await response.json()
    
    async def post(self, url:str, data:dict, params:dict, headers:dict=None, raw:bool=True) -> ClientResponse | dict:
        '''
        HTTP POST method

        :param url: The URL to send the POST request to
        :type url: str

        :param data: Dictionary containing the data to be sent in the POST request body
        :type data: dict

        :param headers: Optional dictionary of HTTP headers to include in the request
        :type headers: dict, optional

        :param raw: Defines the raw/json response
        :type raw: bool
        '''
        if self.session is None: self.session = ClientSession()
        response = await self.session.post(url=url,
                                           params=params,
                                           json=data,
                                           headers=headers)
        response.raise_for_status()
        if raw:
            return response
        return await response.json()
    
    async def close(self):
        if self.session is not None and not self.session.closed:
            await self.session.close()

async def main():
    httpClient = Http()
    print(await httpClient.get('http://httpbin.org/get', raw=False))
    print(await httpClient.post('http://httpbin.org/post', {"user": "123", "pass": "123"}, {"header": "TestHeader"}))
    await httpClient.close()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())