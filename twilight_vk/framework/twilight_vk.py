import asyncio
import contextlib

from .polling.bots_longpoll import BotsLongPoll
from ..logger.darky_logger import DarkyLogger
from ..logger.darky_visual import STYLE, FG
from ..components.logo import LogoComponent
from ..utils.config_loader import Configuration
from .exceptions.framework import (
    InitializationError
)

CONFIG = Configuration().get_config()

class TwilightVK:

    def __init__(self,
                 BOT_NAME: str = __name__,
                 ACCESS_TOKEN: str = None, 
                 GROUP_ID: int = None, 
                 API_VERSION: str = CONFIG.vk_api.version,
                 API_MODE: str = "BOTSLONGPOLL") -> None:
        '''
        Initializes TwilightVK

        :param BOT_NAME: name of your bot
        :type BOT_NAME: str

        :param ACCESS_TOKEN: your group's access token, you can find it here(https://dev.vk.com/ru/api/access-token/community-token/in-community-settings)
        :type ACCESS_TOKEN: str

        :param GROUP_ID: your group's id, you can find it in your group's settings
        :type GROUP_ID: int

        :param API_VERSION: version of VK API, by default its grabbed from the frameworks's default configuration
        :type API_VERSION: str | None

        :param API_MODE: mode of polling (BOTSLONGPOLL/.../...)
        :type API_MODE: str
        '''
        self.logo = LogoComponent()
        self.logger = DarkyLogger(logger_name=f"twilight-vk", configuration=CONFIG.LOGGER)

        self.logger.info(f"Initializing framework...")

        self.started = False

        if not ACCESS_TOKEN or not GROUP_ID:
            raise InitializationError(ACCESS_TOKEN, GROUP_ID)

        self.__access_token__ = ACCESS_TOKEN
        self.__group_id__ = GROUP_ID
        self.__api_version__ = API_VERSION

        self.__tasks__ = []

        self.__loop__ = asyncio.get_event_loop()

        API_MODES = {
            "BOTSLONGPOLL": BotsLongPoll(access_token=ACCESS_TOKEN,
                                         group_id=GROUP_ID,
                                         api_version=API_VERSION)
        }
        self.__bot__ = API_MODES.get(API_MODE, "BOTSLONGPOLL")
        self.methods = self.__bot__.vk_methods
        self.on_event = self.__bot__.event_handler.on_event

        self.logger.debug(f"Framework is initialized")

    async def run_polling(self):
        '''
        Start polling
        '''
        try:
            self.logger.info(f"Starting the framework...")
            self.started = True
            await self.__bot__.auth()
            self.logger.info(f"{FG.BLUE}Framework is started{STYLE.RESET}")

            #async for event_response in self.__bot__.listen():
            #    for event in event_response["updates"]:
            #        await self.__eventHandler__.handle(event)

            async def process_events(event_response):
                """Вспомогательная функция для обработки набора событий."""
                try:
                    events = []
                    for event in event_response["updates"]:
                        events.append(
                            self.__loop__.create_task(
                                self.__bot__.event_handler.handle(event)
                            )
                        )
                    results = await asyncio.gather(*events, return_exceptions=True)
                    for result, event in zip(results, event_response["updates"]):
                        if isinstance(result, Exception):
                            if not self.__bot__.__stop__:
                                self.logger.error(f"Event handling error {event}: {result}")
                                raise result
                except Exception as ex:
                    self.logger.error(f"{ex.__class__.__name__}: {ex}", exc_info=True)

            async for event_response in self.__bot__.listen():
                if self.started:
                    self.__loop__.create_task(process_events(event_response))

        except asyncio.CancelledError:
            self.logger.warning(f"Polling was forcibly canceled (it is not recommend to do this)")
        except Exception as exc:
            self.logger.critical(f"Framework was crashed with critical unhandled error", exc_info=True)
        finally:
            #self.__loop__.stop()
            if not self.__bot__.__stop__:
                self.__bot__.stop()
            self.logger.info(f"{FG.RED}Framework has been stopped{STYLE.RESET}")
            await asyncio.sleep(0.1)
            self.started = False


    def start(self):
        '''
        Starts the bot and polling until stop() is called
        '''
        self.logger.note(self.logo.colored)

        self.__tasks__.append(self.run_polling())

        if not self.__tasks__:
            self.logger.warning("There is no tasks to run")
            
        while self.__tasks__:
            self.__loop__.create_task(self.__tasks__.pop(0))

        tasks = asyncio.all_tasks(self.__loop__)
        try:
            while tasks:
                tasks_results, _ = self.__loop__.run_until_complete(
                    asyncio.wait(tasks, return_when=asyncio.FIRST_EXCEPTION)
                )
                for task_result in tasks_results:
                    try:
                        task_result.result()
                    except Exception as exc:
                        self.logger.critical(exc)
                tasks = asyncio.all_tasks(self.__loop__)

        except KeyboardInterrupt:
            self.logger.warning(f"KeyboardInterrupt recieved, shutting down...")
            tasks_to_cancel = self.stop(force=True, tasks=tasks)
            with contextlib.suppress(asyncio.CancelledError):
                self.__loop__.run_until_complete(tasks_to_cancel)
        finally:
            self.__loop__.run_until_complete(self.__loop__.shutdown_asyncgens())
            if self.__loop__.is_running():
                self.__loop__.close()

    def stop(self, force: bool = False, tasks: list[asyncio.Task] = None):
        '''
        Stops the polling and bot

        :param force: *[Optional]* Force stopping with cancelling all current event handlings
        :type force: bool

        :param tasks: *[Optional]* List of asynchronous tasks is running now. Used only when *force=True*
        :type tasks: list
        '''
        if self.started:

            self.logger.info(f"Shutting down...")
            self.should_stop()

            if force:

                self.logger.warning(f"Forced stop. For soft stop - use TwilightVK.should_stop() method")

                if not tasks:
                    tasks = asyncio.all_tasks(self.__loop__)
                    
                tasks_to_cancel = asyncio.gather(*tasks)
                tasks_to_cancel.cancel()
                return tasks_to_cancel
    
    def should_stop(self):
        '''
        Tells the bot that it should stop after the next event
        '''
        if not self.__bot__.__stop__:
            self.logger.info("Framework was asked to stop")
            self.__bot__.stop()
        else:
            self.logger.warning("Framework is already stopping")

    def __getApiRouters__(self):
        pass