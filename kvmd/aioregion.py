import types

from typing import Type


# =====
class RegionIsBusyError(Exception):
    def __init__(self) -> None:
        super().__init__("Performing another operation, please try again later")


class AioExclusiveRegion:
    def __init__(self, exc_type: Type[RegionIsBusyError]) -> None:
        self.__exc_type = exc_type
        self.__busy = False

    def is_busy(self) -> bool:
        return self.__busy

    def enter(self) -> None:
        if not self.__busy:
            self.__busy = True
            return
        raise self.__exc_type()

    def exit(self) -> None:
        self.__busy = False

    def __enter__(self) -> None:
        self.enter()

    def __exit__(
        self,
        _exc_type: Type[BaseException],
        _exc: BaseException,
        _tb: types.TracebackType,
    ) -> None:
        self.exit()