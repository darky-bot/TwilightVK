import logging

from .groups import Groups
from .messages import Messages
from .users import Users
from ...logger.darky_logger import DarkyLogger
from ...utils.config_loader import Configuration

CONFIG = Configuration().get_config()

class VkMethods:

    def __init__(self,
                 baseMethods:object):
        self.logger = DarkyLogger("vk-methods", CONFIG.LOGGER)
        self.groups = Groups(baseMethods, self.logger)
        self.messages = Messages(baseMethods, self.logger)
        self.users = Users(baseMethods, self.logger)