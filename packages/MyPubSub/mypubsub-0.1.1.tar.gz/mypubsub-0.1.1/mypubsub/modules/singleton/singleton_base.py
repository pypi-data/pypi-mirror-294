"""
This module provides the Singleton Base class for Singleton pattern implementation.
"""

class SingletonMeta(type):
    """
    A metaclass for creating singleton classes.
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonMeta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class SingletonBase(metaclass=SingletonMeta):
    """
    A base class that implements the singleton pattern.
    """
    def __init__(self):
        # Initialize singleton instance
        pass

    @classmethod
    def get_instance(cls):
        """
        Get the singleton instance of the class.
        """
        return cls()

    @classmethod
    def reset_instance(cls):
        """
        Reset the singleton instance. Useful for testing or reinitialization.
        """
        if cls in cls._instances:
            del cls._instances[cls]

    @classmethod
    def reset_all_instances(cls):
        """
        Reset all the singleton instance. Useful for testing or reinitialization.
        """
        cls._instances = {}

    @classmethod
    def get_instance_count(cls):
        """
        Get the count of instances created (should be 1 for singletons).
        """
        return len(cls._instances)

    def __str__(self):
        """
        Return a string representation of the singleton instance.
        """
        return f"{self.__class__.__name__} singleton instance"
