import re

class TwiML:

    def __init__(self, template:str=None):
        self.template = template
        self.placeholder_types = {
            "any": (r".+", str),
            "int": (r"\d+", int),
            "word": (r"\S+", str)
        }

    def update_template(self, template:str):
        self.template = template
    
    def parse(self,
              message:str) -> dict:
        
        pattern = re.escape(self.template)
        placeholders = re.findall(r"<(\w+)(?::(\w+))?>", self.template)
        args = {}
        
        for name, placeholder_type in placeholders:
            type_ = placeholder_type or "any"
            regex, convert = self.placeholder_types.get(type_)
            pattern = pattern.replace(
                re.escape(f"<{name}{':' + type_ if placeholder_type else ''}>"), f"({regex})"
            )
            args[name] = convert

        match = re.match(pattern, message)
        if not match:
            return None
        
        result = {}
        for (name, _), value in zip(placeholders, match.groups()):
            result[name] = args[name](value)
        return result