
from a_sync.a_sync._meta import ASyncSingletonMeta
from a_sync.a_sync.base import ASyncGenericBase

class ASyncGenericSingleton(ASyncGenericBase, metaclass=ASyncSingletonMeta):
    """
    Subclass this class if you want Singleton-esque ASync objects.
    They work kind of like a typical Singleton would, but you will have two instances instead of one:
    - one sync instance
    - one async instance
    """
    pass
