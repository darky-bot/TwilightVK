import twilight_vk
from twilight_vk.framework.rules import TextRule

bot = twilight_vk.TwilightVK(
    BOT_NAME="SimpleBot",
    ACCESS_TOKEN="123",
    GROUP_ID=123
)

@bot.on_event.message_new(TextRule(value=["привет", "hello"], ignore_case=True))
async def hello(event: dict):
    return "Hello world"

bot.start()