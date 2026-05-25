import asyncio

from ..api.twilight_api import TwiAPI
from .api import FrameworkRouter
from .polling.bots_longpoll import BotsLongPoll
from ..logger.darky_logger import DarkyLogger
from ..logger.darky_visual import STYLE, FG
from ..components.logo import LogoComponent
from ..utils.config import CONFIG
from ..utils.types.pollings import PollingTypes
from ..utils.types.twi_states import TwiVKStates
from ..utils.event_loop import TwiTaskManager
from .exceptions.framework import (
    InitializationError
)

class TwilightVK:

    def __init__(self,
                 bot_name: str = None,
                 token: str = None, 
                 group_id: int = None, 
                 vk_api: str = CONFIG.VK_API.version,
                 polling_type: str = PollingTypes.BOTSLONGPOLL,
                 api_enabled: bool = True,
                 HOST: str = CONFIG.API.host,
                 PORT: str = CONFIG.API.port,
                 loop_wrapper: TwiTaskManager = None) -> None:
        '''
        Initializes TwilightVK

        :param bot_name: name of your bot
        :type bot_name: str

        :param token: your group's access token, you can find it here(https://dev.vk.com/ru/api/access-token/community-token/in-community-settings)
        :type token: str

        :param group_id: your group's id, you can find it in your group's settings
        :type group_id: int

        :param vk_api: version of VK API, by default its grabbed from the frameworks's default configuration
        :type vk_api: str | None

        :param polling_type: mode of polling (BOTSLONGPOLL/.../...)
        :type polling_type: str

        :param api_enabled: should be bot's api awailable
        :type api_enabled: bool

        :param loop_wrapper: Initialized class TwiTaskManager for async loop wrapping
        :type loop_wrapper: TwiTaskManager
        '''
        self._state = TwiVKStates.INITIALIZING
        self.bot_name = self.__class__.__name__ if bot_name is None else bot_name
        self.logo = LogoComponent()
        self.logger = DarkyLogger(logger_name=f"twilight-vk", configuration=CONFIG.LOGGER)

        self.logger.info(f"Initializing framework...")

        try:
            if not token:
                raise InitializationError(token)
        except InitializationError as ex:
            self.logger.critical(f"Initialization error{ex}")
            exit()

        self._token = token
        self._group_id = group_id
        self._vk_api = vk_api

        self._loop_wrapper = TwiTaskManager() if loop_wrapper is None else loop_wrapper

        polling_typeS = {
            PollingTypes.BOTSLONGPOLL: BotsLongPoll(access_token=token,
                                                    group_id=group_id,
                                                    api_version=vk_api,
                                                    loop_wrapper=self._loop_wrapper)
        }
        self._bot = polling_typeS.get(polling_type, PollingTypes.BOTSLONGPOLL)
        self.methods = self._bot.vk_methods
        self.on_event = self._bot._router.on_event

        self.api_router = FrameworkRouter(self)

        self._api: TwiAPI = None

        if api_enabled:
            self.logger.warning("Twilight API is under development yet")
        if False:
            self._api = TwiAPI(
                BOTS = [self],
                HOST = HOST,
                PORT = PORT,
                loop_wrapper = self._loop_wrapper,
                _need_root_router = False
            )

        self._state = TwiVKStates.DISABLED
        self.logger.info(f"Framework initialized")

    async def run_polling(self):
        '''
        Start polling
        '''
        try:
            self._state = TwiVKStates.STARTING
            self.logger.info(f"Framework is starting...")

            if self._api:
                self._loop_wrapper.add_task(self._api.run_server())

            await self._bot.auth()

            if self._bot.__server__ is not None:
                self._state = TwiVKStates.READY
                self.logger.info(f"{FG.GREEN}Framework is started (bot_name: {self.bot_name}){STYLE.RESET}")
            else:
                self.logger.error(f"Server was not aquired. Exiting...")
                self._state = TwiVKStates.ERROR

            async for event_response in self._bot.listen():
                if self._state == TwiVKStates.READY:
                    self._loop_wrapper.add_task(self._bot._router.handle(event_response))

        except KeyboardInterrupt:
            self.logger.debug(f"TwilightVK was stopped by KeyboardInterrupt")
        except asyncio.CancelledError:
            self.logger.warning(f"Polling was forcibly canceled (it is not recommend to do this)")
        except Exception as exc:
            self.logger.critical(f"Framework was crashed with critical unhandled error", exc_info=True)
            self._state = TwiVKStates.ERROR
        finally:
            #self.__loop__.stop()
            if self._state == TwiVKStates.READY and not self._bot.__stop__:
                self._bot.stop()
            self.logger.info(f"{FG.RED}Framework has been stopped{STYLE.RESET}")
            await asyncio.sleep(0.1)
            if self._api:
                await self._api.stop()
            if self._state == TwiVKStates.ERROR:
                exit(1)
            self._state = TwiVKStates.DISABLED
            exit(0)


    def start(self):
        '''
        Starts the bot and polling until stop() is called
        '''
        try:
            self.logger.note(self.logo.colored)
            self._loop_wrapper.add_task(self.run_polling())
            self._loop_wrapper.run()
        except KeyboardInterrupt:
            self.logger.debug(f"TwilightVK was stopped by KeyboardInterrupt")
        except Exception:
            self.logger.critical("Unhandled error", exc_info=True)

    def stop(self, force: bool = False):
        '''
        Stops the polling and bot

        :param force: *[Optional]* Force stopping with cancelling all current event handlings
        :type force: bool
        '''
        if self._state == TwiVKStates.READY:

            self.logger.info(f"Shutting down...")
            self.should_stop()

            #if force:
            #    self.logger.warning(f"Forced stop. For soft stop - use TwilightVK.should_stop() method")
            #    self._loop_wrapper.cancel_tasks(targets = [self.run_polling()])
    
    def should_stop(self):
        '''
        Tells the bot that it should stop after the next event
        '''
        if self._state == TwiVKStates.READY and not self._bot.__stop__:
            self.logger.info("Framework was asked to stop")
            self._state = TwiVKStates.SHUTTING_DOWN
            self._bot.stop()
        elif self._state == TwiVKStates.SHUTTING_DOWN:
            self.logger.warning("Framework is already stopping")
        else:
            self.logger.error(f"Unable to stop framework for some reason. BOT_STATE={self._state} {self._bot.__stop__}")

    def __getApiRouters__(self):
        return self.api_router.get_router()