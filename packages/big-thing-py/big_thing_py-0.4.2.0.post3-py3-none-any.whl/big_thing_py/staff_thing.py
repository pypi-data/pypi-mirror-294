from big_thing_py.core.thing import *


class MXStaffThing(MXThing, metaclass=ABCMeta):

    def __init__(
        self,
        name: str,
        nick_name: str,
        category: DeviceCategory,
        desc: str,
        version: str,
        service_list: List[MXService],
        alive_cycle: float,
        is_parallel: bool,
        is_matter: bool,
    ):
        super().__init__(
            name=name,
            nick_name=nick_name,
            desc=desc,
            category=category,
            version=version,
            service_list=service_list,
            alive_cycle=alive_cycle,
            is_super=False,
            is_parallel=is_parallel,
            is_builtin=False,
            is_manager=False,
            is_matter=is_matter,
        )
        self._is_alive = False

        self._default_tag_list: List[MXTag] = [
            MXTag(tag if check_valid_identifier(tag) == MXErrorCode.NO_ERROR else convert_to_valid_string(tag))
            for tag in [
                self._name,
                # self._nick_name,
            ]
            if tag
        ]

    def __eq__(self, o: 'MXStaffThing') -> bool:
        instance_check = isinstance(o, MXStaffThing)
        staff_thing_name_check = o._name == self._name

        # return super().__eq__(o) and instance_check and staff_thing_id_check
        return instance_check and staff_thing_name_check

    def add_staff_service(self, service_list: List[MXService]) -> None:
        for staff_service in service_list:
            self.add_service(staff_service)

    @abstractmethod
    def staff_dict(self):
        pass

    @abstractmethod
    def setup_service_list(self) -> None:
        pass

    @abstractmethod
    async def setup(self) -> bool:
        pass

    @abstractmethod
    async def wrapup(self) -> bool:
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
    def is_alive(self) -> bool:
        return self._is_alive

    # ==================================
    #             _    _
    #            | |  | |
    #  ___   ___ | |_ | |_   ___  _ __
    # / __| / _ \| __|| __| / _ \| '__|
    # \__ \|  __/| |_ | |_ |  __/| |
    # |___/ \___| \__| \__| \___||_|
    # ==================================

    @is_alive.setter
    def is_alive(self, is_alive: bool) -> None:
        self._is_alive = is_alive
