import pytest

import twilight_vk
from twilight_vk.framework.exceptions.framework import (
    InitializationError
)

@pytest.mark.asyncio
async def test_invalid_initialization():
    with pytest.raises(InitializationError):
        twilight_vk.TwilightVK()