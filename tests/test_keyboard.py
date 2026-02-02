import pytest
import pytest_asyncio

from twilight_vk.utils.keyboard import (
    KeyboardMarkup,
    TextActionKeyboardButton,
    LocationKeyboardButton,
    VkPayKeyboardButton
)
from twilight_vk.utils.types.keyboard_colors import KeyboardColor
from tests.fixtures.keyboard import (
    keyboard_markup,
    inline_keyboard_markup
)

@pytest.mark.asyncio
async def test_keyboard(keyboard_markup: dict, inline_keyboard_markup: dict):
    _inline_keyboard = KeyboardMarkup(inline=True,
                                      buttons=[
                                          [
                                              TextActionKeyboardButton(
                                                  label="TestButton",
                                                  color=KeyboardColor.POSITIVE
                                              )
                                          ]
                                      ])
    assert _inline_keyboard.getMarkup() == inline_keyboard_markup

    _keyboard = KeyboardMarkup(one_time=True,
                               inline=False,
                               buttons=[
                                   [
                                       TextActionKeyboardButton(
                                           label="TestButton",
                                           payload="{\"button\": \"1\"}",
                                           color=KeyboardColor.SECONDARY
                                       ),
                                       LocationKeyboardButton(
                                           payload="{\"button\": \"2\"}"
                                       )
                                   ],
                                   [
                                       VkPayKeyboardButton(
                                           hash="action=transfer-to-group&group_id=12345&aid=10"
                                       )
                                   ]
                               ])
    assert _keyboard.getMarkup() == keyboard_markup