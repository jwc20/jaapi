from .utils import *
from .scrape import Scrape
from .login import LogIn


class LinkedIn(Scrape, LogIn):
    def __init__(self, **kwargs):
        Scrape.__init__(self, **kwargs)
        LogIn.__init__(self)


__authors__ = ["jwc20"]
__source__ = "https://github.com/jwc20/jaapi"
