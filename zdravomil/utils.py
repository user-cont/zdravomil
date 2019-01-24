
from os import getenv

HOME = getenv('HOME')


class ZdravoIgnoredCommit(RuntimeWarning):
    pass


class AuthorMailNotFound(RuntimeWarning):
    pass
