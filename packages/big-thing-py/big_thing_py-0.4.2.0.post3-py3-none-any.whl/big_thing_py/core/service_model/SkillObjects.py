import typing
from enum import Enum
from dataclasses import dataclass, field
from big_thing_py.common import MXType
import sys
from typing import List, Union

INFINITY = sys.maxsize


class MXClassproperty:
    def __init__(self, fget):
        self.fget = fget

    def __get__(self, instance, owner):
        return self.fget(owner)


ALL_SKILLS = {}


@dataclass
class MXValueType:
    type: MXType
    bound: List[int] = field(default_factory=lambda: [-INFINITY - 1, INFINITY])
    format: Union[str, Enum] = None


@dataclass
class Skill:
    id: str = field(init=False)

    @MXClassproperty
    def descriptor(cls) -> str:
        raise NotImplementedError()

    @MXClassproperty
    def values(cls) -> List['SkillValue']:
        value_list = []
        if not hasattr(cls, 'Values'):
            return value_list

        for attr in dir(cls.Values):
            if not attr.startswith('__'):
                attr_instance = getattr(cls.Values, attr)
                value_list.append(attr_instance)

        return value_list

    @MXClassproperty
    def functions(cls) -> List['SkillFunction']:
        function_list = []
        if not hasattr(cls, 'Functions'):
            return function_list

        for attr in dir(cls.Functions):
            if not attr.startswith('__'):
                attr_instance = getattr(cls.Functions, attr)
                function_list.append(attr_instance)

        return function_list

    @MXClassproperty
    def docs_string(cls) -> str:
        description = f'{cls.id}\n'
        description += f'\ndescription: {cls.descriptor}\n'
        if hasattr(cls, 'Values'):
            description += '\nValues:\n'
            for value in cls.values:
                description += f'Value [{value.value_id}]\n'
                description += f'  - {value.docs_string}\n'
        if hasattr(cls, 'Functions'):
            description += '\nFunctions:\n'
            for function in cls.functions:
                description += f'  - {function.docs_string}\n'
        return description

    def __init_subclass__(cls, *args, **kwargs) -> None:
        '''Register a subclass.'''
        super().__init_subclass__(*args, **kwargs)
        cls.id = cls.__name__
        # register this cluster in the ALL_SKILLS dict for quick lookups
        try:
            ALL_SKILLS[cls.id] = cls
        except NotImplementedError:
            # handle case where the Cluster class is not (fully) subclassed
            # and accessing the id property throws a NotImplementedError.
            pass


class SkillValue:
    @MXClassproperty
    def descriptor(cls) -> str:
        raise NotImplementedError()

    @MXClassproperty
    def skill_id(cls) -> str:
        return cls.__qualname__.split('.')[0]

    @MXClassproperty
    def value_id(cls) -> str:
        return cls.__name__

    @MXClassproperty
    def value_type(cls) -> MXValueType:
        raise NotImplementedError()

    @MXClassproperty
    def docs_string(cls) -> str:
        return f'Value: {cls.descriptor} (Type: {str(cls.value_type.type)}, Bound: {cls.value_type.bound}, Format: {cls.value_type.format.__name__})'


class SkillFunctionArgument:
    @MXClassproperty
    def descriptor(cls) -> str:
        raise NotImplementedError()

    @MXClassproperty
    def function_id(cls) -> str:
        return cls.__qualname__.split('.')[2]

    @MXClassproperty
    def argument_id(cls) -> str:
        return cls.__name__

    @MXClassproperty
    def argument_type(cls) -> MXType:
        raise NotImplementedError()

    @MXClassproperty
    def docs_string(cls) -> str:
        return f'Argument: {cls.descriptor} (Type: {str(cls.argument_type.type)}, Format: {cls.format_details()})'


class SkillFunction:
    @MXClassproperty
    def descriptor(cls) -> str:
        raise NotImplementedError()

    @MXClassproperty
    def skill_id(cls) -> str:
        return cls.__qualname__.split('.')[0]

    @MXClassproperty
    def function_id(cls) -> str:
        return cls.__name__

    @MXClassproperty
    def arguments(cls) -> List[SkillFunctionArgument]:
        argument_list = []
        if not hasattr(cls, 'Arguments'):
            return argument_list

        argument_dict: dict = cls.Arguments.__dict__
        for k, attr in argument_dict.items():
            if not k.startswith('__'):
                attr_instance = getattr(cls.Arguments, k)
                argument_list.append(attr_instance)

        return argument_list

    @MXClassproperty
    def return_type(cls) -> MXType:
        raise NotImplementedError()

    @MXClassproperty
    def docs_string(cls) -> str:
        args = ', '.join([arg.docs_string for arg in cls.arguments()])
        return f'Function: {cls.descriptor} - Arguments: ({args}) - Returns: {cls.return_type().name}'
