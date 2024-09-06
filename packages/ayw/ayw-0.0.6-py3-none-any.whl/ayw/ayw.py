import sys
import inspect
import random
import importlib.resources
from types import FrameType

# importer_file_ = inspect.stack()[12].filename
importer_file_ = sys.argv[0]
if importer_file_ is not None and len(importer_file_) > 0:
    with open(importer_file_) as _f:
        cf = inspect.currentframe()
        _content = _f.read()
        if "import ayw as sb" in _content or "import ayw as SB" in _content:
            print("sb")
        elif "import ayw as nb" in _content or "import ayw as NB" in _content:
            print("ayw NB")
        else:
            print("nb")
else:
    print("ayw NB!!!")


class __MetaNB(type):
    def __repr__(self):
        return "贼NB"


class __BaseNB(metaclass=__MetaNB):
    good_import: bool = None

    @classmethod
    def check_good_import(cls, caller_frame: FrameType) -> bool:
        caller_locals = cls.get_caller_locals(caller_frame)
        return cls.module_name_equals(caller_locals, "nb") or cls.module_name_equals(caller_locals, "NB")

    @classmethod
    def check_bad_import(cls, caller_frame: FrameType) -> bool:
        caller_locals = cls.get_caller_locals(caller_frame)
        return cls.module_name_equals(caller_locals, "sb") or cls.module_name_equals(caller_locals, "SB")

    @classmethod
    def get_caller_locals(cls, caller_frame):
        if caller_frame is None:
            caller_frame = inspect.currentframe().f_back.f_back.f_back
        caller_locals = caller_frame.f_locals
        return caller_locals

    @classmethod
    def module_name_equals(cls, caller_locals, name):
        return name in caller_locals.keys() and caller_locals[name] is sys.modules[__package__]


class _NB(__BaseNB, metaclass=__MetaNB):
    def __init__(self):
        res = importlib.resources.files("ayw").joinpath("resources/quotes.txt")
        with res.open(encoding="utf-8") as f:
            self.quotes = f.readlines()

    def __repr__(self):
        return self.get_message(caller_frame=inspect.currentframe().f_back)

    def __call__(self, *args, **kwargs):
        print(self.get_message(caller_frame=inspect.currentframe().f_back))

    def get_message(self, **kwargs):
        if "caller_frame" in kwargs.keys() and kwargs["caller_frame"] is not None:
            caller_frame = kwargs["caller_frame"]
        else:
            caller_frame = inspect.currentframe().f_back
        if self.check_bad_import(caller_frame):
            return "sbyx"
        elif self.check_good_import(caller_frame):
            return random.choice(self.quotes).strip()
        else:
            return "You don't import with respect. You don't offer friendship. You don't even think to call me \"NB\""


nb = _NB()
