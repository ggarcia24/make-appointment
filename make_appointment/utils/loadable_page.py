from typing_extensions import Self


class NotLoadedException(Exception):
    pass


class LoadablePage(object):
    def open(self) -> Self:
        try:
            self._is_loaded()
            return self
        except NotLoadedException:
            self._load()

        self._is_loaded()
        return self

    def _load(self):
        raise NotImplementedError()

    def _is_loaded(self):
        raise NotImplementedError()
