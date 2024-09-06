from big_thing_py.core.service_model import SkillObjects
from big_thing_py.core.service_model.SkillObjects import MXClassproperty
from typing import Set, Dict, List, Union, Any

# ALL_DEVICE_TYPES: dict[int, type["MXDeviceCategory"]] = {}


class MXDeviceCategory:
    """Base class for MX device types."""

    # device_type: int
    skills: Set[SkillObjects.Skill]

    # def __init_subclass__(cls, *, device_type: int, **kwargs: Any) -> None:
    #     """Register a subclass."""
    #     super().__init_subclass__(**kwargs)
    #     cls.device_type = device_type
    #     ALL_DEVICE_TYPES[device_type] = cls

    def __init_subclass__(cls, **kwargs: Any) -> None:
        """Register a subclass."""
        super().__init_subclass__(**kwargs)

    # def __hash__(self) -> int:
    #     """Return unique hash for this object."""
    #     return self.device_type

    @MXClassproperty
    def name(cls) -> str:
        """Return the class name as a string."""
        return cls.__name__
