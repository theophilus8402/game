
from enum import Enum

Effect = Enum("Effect", [
    # equipment effects?
    "block",
    # spell effects
    ])


class SpecialEffect():

    def __init__(self, spec_type):
        super(SpecialEffect, self).__setattr__("_attributes", {"spec_type":spec_type})

    def __setattr__(self, key, value):
        self._attributes[key] = value

    def __getattr__(self, key):
        try:
            return self._attributes.get(key, None)
        except KeyError:
            raise AttributeError
