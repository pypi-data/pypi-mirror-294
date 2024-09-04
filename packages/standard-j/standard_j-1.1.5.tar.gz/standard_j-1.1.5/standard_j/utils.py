from standard_j.error import StandardJError
import typing
from typing import Self as EnumItem


class Initializer(object):
    """
    A class that tracks whether a subclass has been initialized (using inherited initialize())
    Useful for when methods need to act differently post initialization
    Generally best to initialize() at the end of __init__()
    """

    def __new__(cls, *args, **kwargs):
        """
        Used to ensure this class is only inherited, and not directly instantiated
        """
        if cls == Initializer:
            raise NotImplementedError("Initializer class is not implemented and must be inherited")
        return super().__new__(cls, *args, **kwargs)

    def initialize(self):
        """
        The method that initializes the object.
        :return: None
        """
        object.__setattr__(self, f"_{type(self).__name__}__initialized", 1)

    @property
    def is_initialized(self) -> bool:
        """
        Method used to find out if self has been initialized yet
        :return: True if self.__initialized exists, False otherwise
        """
        return f"_{type(self).__name__}__initialized" in object.__getattribute__(self, "__dict__").keys()


# <editor-fold desc="Enum">
class __EnumMeta(type):
    class __EnumDict(dict):
        def __setitem__(self, key, value):
            if hasattr(self, "standard_keys") and key not in getattr(self, "standard_keys"):
                raise StandardJError("Enum attributes must be hinted, not set")
            super().__setitem__(key, value)

        def lock(self):
            if not hasattr(self, "standard_keys"):
                setattr(type(self), "standard_keys", self.keys())

    @classmethod
    def __prepare__(mcs, name, bases):
        return mcs.__EnumDict()

    def __new__(mcs, name, bases, e_dict: __EnumDict):
        enum_cls = super().__new__(mcs, name, bases, e_dict)
        e_dict.lock()

        if name != "Enum":
            if not all(value == EnumItem for value in e_dict["__annotations__"].values()):
                raise TypeError("All attributes of an Enum must be hinted as type 'EnumItem' or 'Self' (from typing)")
            annotations_list = list(e_dict["__annotations__"].keys())
            for index, enum_item in enumerate(annotations_list):
                type.__setattr__(enum_cls, enum_item, enum_cls(enum_item, index))
            type.__setattr__(enum_cls, f"_{enum_cls.__name__}__initialized", 1)
        return enum_cls

    def __iter__(self):
        for key in self.__annotations__.keys():
            yield super().__getattribute__(key)

    def __len__(self):
        return len(self.__annotations__.keys())

    def __setattr__(self, key, value):
        raise AttributeError("Cannot set the value of an Enum attribute")

    def __str__(self):
        return f"{self.__name__}({', '.join(item for item in self.__annotations__.keys())})"

    def __repr__(self):
        out = (f"{enum_item}: {index}" for index, enum_item in enumerate(self.__annotations__.keys()))
        return f"<enum {self.__name__}>({', '.join(out)})"


class Enum(metaclass=__EnumMeta):
    """
    Simple enum class for python that allows for typechecking members as self
    """
    __annotations__ = {}

    def __init__(self, name: str, value: int):
        if hasattr(self, f"_{type(self).__name__}__initialized"):
            raise TypeError(f"{str(self)} cannot be instantiated")
        self.name = name
        self.value = value
        object.__setattr__(self, f"_{type(self).__name__}__initialized", 1)

    def __getattribute__(self, item):
        try:
            super().__getattribute__(f"_{type(self).__name__}__initialized")
        except AttributeError:
            return super().__getattribute__(item)
        if item not in ("name", "value"):
            raise AttributeError("Enum attribute only has access to its 'name' and 'value'")
        return super().__getattribute__(item)

    def __setattr__(self, key, value):
        if hasattr(self, f"_{type(self).__name__}__initialized"):
            raise AttributeError("Enum attribute cannot be modified")
        super().__setattr__(key, value)

    def __int__(self):
        return self.value

    def __str__(self):
        return f"{type(self).__name__}.{self.name}"

    def __repr__(self):
        return f"<{type(self).__name__} object>(name: {self.name}, value: {self.value})"
# </editor-fold>


GenericFunctionType = typing.Callable[[...], typing.Any]
