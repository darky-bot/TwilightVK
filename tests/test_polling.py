import pytest
import twilight_vk

@pytest.mark.skip("Not ready")
@pytest.mark.asyncio
async def test_botlongpoll_check_event_func():
    bot: twilight_vk.TwilightVK = None
    response = await bot.__bot__.check_event()
    assert response.keys() == {"ts": 0, "updates": []}.keys()