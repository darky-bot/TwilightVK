from .api import BaseMethodsGroup

class Messages(BaseMethodsGroup):
    
    #Это образец
    #Примерный запрос к методу: https://api.vk.com/methods/messages.example
    async def example(self, peer_id) -> dict:
        values = {
            "peer_id": peer_id
        }
        response = await self.base_api.base_get_method(api_method=f"{self.method}.example",
                                                       values=values)
        return response
        