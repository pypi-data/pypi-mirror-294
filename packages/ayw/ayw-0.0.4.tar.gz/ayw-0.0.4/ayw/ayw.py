import sys
import inspect
import random
import importlib.resources

if sys.argv[0] is not None and len(sys.argv[0]) > 0:
    with open(sys.argv[0]) as f:
        if "import ayw as nb" in f.read():
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

    @staticmethod
    def check_good_import(cls) -> bool:
        if cls.good_import is None:
            cf = inspect.currentframe()
            super_locals = cf.f_back.f_back.f_locals
            if "nb" in super_locals.keys() and super_locals["nb"] is sys.modules[__package__]:
                cls.good_import = True
            else:
                cls.good_import = False
        return cls.good_import


class _NB(__BaseNB, metaclass=__MetaNB):
    def __init__(self):
        res = importlib.resources.files("ayw").joinpath("resources/quotes.txt")
        with res.open() as f:
            self.quotes = f.readlines()

    def __repr__(self):
        if self.check_good_import(self.__class__):
            return random.choice(self.quotes)
        else:
            return "You don't import with respect. You don't offer friendship. You don't even think to call me \"NB\""

    def __call__(self):
        self.check_good_import(self.__class__)
        print(self.__repr__())


nb = _NB()
