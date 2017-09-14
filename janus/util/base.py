from six import with_metaclass

from abc import ABCMeta

class Entity(with_metaclass(ABCMeta)):
    pass


TYPE_ERROR_STRING = 'Expected {expected_type_name}, got {recieved_type_name} instead.'