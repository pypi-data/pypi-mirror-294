from big_thing_py.core.tag import *
from big_thing_py.core.service_model import SkillValue, SkillFunction
from abc import *
from asyncio import iscoroutinefunction


class MXService(metaclass=ABCMeta):

    def __init__(
        self,
        name: str,
        category: Union[SkillValue, SkillFunction],
        func: Union[Callable, Coroutine],
        tag_list: List[MXTag],
        energy: float,
        desc: str,
        thing_name: str,
        middleware_name: str,
    ) -> None:
        self._name = name
        self._category = category
        self._func = func
        self._tag_list = tag_list
        self._energy = energy
        self._desc = desc
        self._thing_name = thing_name
        self._middleware_name = middleware_name

        if not callable(self._func) and not iscoroutinefunction(self._func):
            raise MXValueError(f'func must be callable or coroutine function.')
        if not issubclass(self._category, SkillValue) and not issubclass(self._category, SkillFunction):
            raise MXValueError(f'category must be SkillValue or SkillFunction class.')
        if not self._name:
            self._name = self._category.function_id if issubclass(self._category, SkillFunction) else self._category.value_id
        if check_valid_identifier(self._name) == MXErrorCode.INVALID_DATA:
            raise MXValueError(f'name cannot be empty & can only contain alphanumeric characters and underscores. name: {self._name}')
        elif check_valid_identifier(self._name) == MXErrorCode.TOO_LONG_IDENTIFIER:
            raise MXValueError(f'too long identifier. name: {self._name}, length: {len(self._name)}')

        if any([not isinstance(tag, MXTag) for tag in self._tag_list]):
            raise MXValueError('tag_list must contain MXTag object')
        else:
            self.sort_tag()

        if not isinstance(self._energy, (int, float)):
            raise MXValueError(f'energy must be int or float')
        if not isinstance(self._desc, str):
            raise MXValueError(f'desc must be str')
        if not isinstance(self._thing_name, str):
            raise MXValueError(f'thing_name must be str')
        if not isinstance(self._middleware_name, str):
            raise MXValueError(f'middleware_name must be str')

        # NOTE (thsvkd): test new service model, SkillValue, SkillFunction
        # if self._category == MXFunctionCategory.undefined:
        #     self._category = MXFunctionCategory.get(self._name)

    def __eq__(self, o: 'MXService') -> bool:
        instance_check = isinstance(o, MXService)
        name_check = o._name == self._name
        # thing_name_check = o._thing_name == self._thing_name
        # middleware_name_check = o._middleware_name == self._middleware_name
        tag_list_check = o._tag_list == self._tag_list
        # func_check = o._func == self._func
        energy_check = o._energy == self._energy

        # return instance_check and name_check and thing_name_check and middleware_name_check and tag_list_check and func_check and energy_check
        return instance_check and name_check and tag_list_check and energy_check

    def __getstate__(self):
        state = self.__dict__.copy()

        del state['_func']

        return state

    def __setstate__(self, state):
        self.__dict__.update(state)

        self._func = None

    def add_tag(self, tag: Union[MXTag, List[MXTag]]) -> 'MXService':
        if not isinstance(tag, (MXTag, list)):
            raise Exception('tag must be MXTag object')

        if isinstance(tag, MXTag):
            if not tag in self._tag_list:
                self._tag_list.append(tag)
        elif all(isinstance(t, MXTag) for t in tag):
            for t in tag:
                if not t in self._tag_list:
                    self._tag_list.append(t)
        self._tag_list = sorted(self._tag_list, key=lambda x: x.name)

        return self

    def remove_tag(self, tag: str) -> 'MXService':
        if not isinstance(tag, str):
            raise Exception('tag to remove must be str')

        for t in self._tag_list:
            if t.name == tag:
                self._tag_list.remove(MXTag(tag))

    def sort_tag(self) -> 'MXService':
        self._tag_list = sorted(self._tag_list, key=lambda x: x.name)
        return self

    @abstractmethod
    def dict(self) -> dict:
        pass

    # ====================================
    #               _    _
    #              | |  | |
    #   __ _   ___ | |_ | |_   ___  _ __
    #  / _` | / _ \| __|| __| / _ \| '__|
    # | (_| ||  __/| |_ | |_ |  __/| |
    #  \__, | \___| \__| \__| \___||_|
    #   __/ |
    #  |___/
    # ====================================

    @property
    def name(self) -> str:
        return self._name

    @property
    def category(self) -> Union[SkillValue, SkillFunction]:
        return self._category

    @property
    def thing_name(self) -> str:
        return self._thing_name

    @property
    def middleware_name(self) -> str:
        return self._middleware_name

    @property
    def tag_list(self) -> List[MXTag]:
        return self._tag_list

    @property
    def desc(self) -> str:
        return self._desc

    @property
    def func(self) -> Callable:
        return self._func

    @property
    def energy(self) -> float:
        return self._energy

    # ==================================
    #             _    _
    #            | |  | |
    #  ___   ___ | |_ | |_   ___  _ __
    # / __| / _ \| __|| __| / _ \| '__|
    # \__ \|  __/| |_ | |_ |  __/| |
    # |___/ \___| \__| \__| \___||_|
    # ==================================

    @name.setter
    def name(self, name: str) -> None:
        self._name = name

    @category.setter
    def category(self, category: Union[SkillValue, SkillFunction]) -> None:
        self._category = category

    @thing_name.setter
    def thing_name(self, thing_name: str) -> None:
        self._thing_name = thing_name

    @middleware_name.setter
    def middleware_name(self, middleware_name: str) -> None:
        self._middleware_name = middleware_name

    @tag_list.setter
    def tag_list(self, tag_list: List[MXTag]) -> None:
        self._tag_list = tag_list

    @desc.setter
    def desc(self, desc: str) -> None:
        self._desc = desc

    @func.setter
    def func(self, func: Callable) -> None:
        self._func = func

    @energy.setter
    def energy(self, energy: float) -> None:
        self._energy = energy
