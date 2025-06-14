from aiohttp import ClientSession, ClientResponse

class Http:

    def __init__(self):
        '''
        This class allows to use HTTP requests asynchronously
        '''
        self.session = None     

    async def request(self, url:str, method:str="GET", data=None, headers=None) -> ClientResponse:
        if self.session is None: self.session = ClientSession()
        async with self.session.request(url=url, method=method, data=data, headers=headers) as response:
            await response.read()
            return response
    
    async def request_text(self, url:str, method:str="GET", data=None, headers=None) -> str:
        response = await self.request(url, method, data, headers)
        return await response.text(encoding="UTF-8")

    async def request_json(self, url:str, method:str="GET", data=None, headers=None) -> dict:
        response = await self.request(url, method, data, headers)
        return await response.json(
            encoding="UTF-8"
        )
    
    async def close(self):
        if self.session is not None and not self.session.closed:
            await self.session.close()  

async def main():
    http = Http()
    print(await http.request('http://127.0.0.1:8000/ping', method="GET"))
    print(await http.request_text('http://127.0.0.1:8000/ping', method="GET"))
    print(await http.request_json('http://127.0.0.1:8000/ping', method="GET"))
    await http.close()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())