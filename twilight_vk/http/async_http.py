import logging
import asyncio

from aiohttp import ClientSession, ClientResponse, ClientTimeout, TCPConnector

logger = logging.getLogger("async-http")

class Http:

    def __init__(self,
                 headers: dict | None = None,
                 timeout: int = 30,
                 retries: int = 5):
        '''
        This class allows to use HTTP requests asynchronously
        '''
        self.session = None
        self.headers = headers
        self.timeout = timeout
        self._retry_attempt = 0
        self.retries = retries
    
    async def _get_session(self):
        if self.session is None:
            self.session = ClientSession(headers=self.headers,
                                         timeout=ClientTimeout(self.timeout),
                                         connector=TCPConnector(force_close=True))
        
    @staticmethod
    async def _is_raw(response:ClientResponse, raw:bool=False):
        if raw:
            return response
        return await response.json()

    async def get(self,
                  url:str,
                  params:dict|None=None,
                  headers:dict|None=None,
                  raw:bool=True) -> ClientResponse | dict:
        '''
        HTTP GET method

        :param url: The url to get the response from
        :type url: str

        :param params: Dictionary containing the optional data to be sent in the GET request
        :type params: dict | None

        :param headers: Optional dictionary of HTTP headers to include in the request
        :type headers: dict, optional

        :param raw: Defines the raw/json response
        :type raw: bool
        '''
        await self._get_session()
        try:
            response = await self.session.get(url=url,
                                            params=params,
                                            headers=headers)
        except asyncio.TimeoutError:
            self._retry_attempt += 1
            logger.error(f"TimeoutError occured in HTTP-GET request")

            if self._retry_attempt <= self.retries:
                logger.info(f"Retrying (Attempt ({self._retry_attempt}/{self.retries}))...")
                return await self.get(url = url, params = params, headers = headers, raw = raw)
            
            logger.error(f"No more retry attempts, raising exception...")
            raise asyncio.TimeoutError

        return await self._is_raw(response, raw=raw)
    
    async def post(self,
                   url:str,
                   data:dict,
                   params:dict={},
                   headers:dict=None,
                   raw:bool=True) -> ClientResponse | dict:
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
        await self._get_session()
        try:
            response = await self.session.post(url=url,
                                            params=params,
                                            json=data,
                                            headers=headers)
        except asyncio.TimeoutError:
            self._retry_attempt += 1
            logger.error(f"TimeoutError occured in HTTP-GET request")

            if self._retry_attempt <= self.retries:
                logger.info(f"Retrying (Attempt ({self._retry_attempt}/{self.retries}))...")
                return await self.get(url = url, params = params, headers = headers, raw = raw)
            
            logger.error(f"No more retry attempts, raising exception...")
            raise asyncio.TimeoutError

        return await self._is_raw(response, raw=raw)
    
    async def close(self):
        if self.session is not None and not self.session.closed:
            await self.session.close()
            self.session = None