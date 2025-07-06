from .groups import Groups
from .messages import Messages

class VkMethods:

    def __init__(self,
                 baseMethods:object):
        self.groups = Groups(baseMethods)
        self.messages = Messages(baseMethods)