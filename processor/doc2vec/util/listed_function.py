from typing import List, Callable


class Base:
    def __call__(self, funcs: List[Callable], *args, **kwargs):
        for func in funcs:
            result = func(*args, **kwargs)
            if self._check_result(result):
                return self._get_response(result=result)
            return self._get_response(result=result)

    def _check_result(self, result):
        pass

    def _get_response(self, result):
        pass


class TrueBreak(Base):
    def _check_result(self, result):
        return result == True

    def _get_response(self, result):
        return result


true_break = TrueBreak()


class NotNoneBreak(Base):
    def _check_result(self, result):
        return result is not None

    def _get_response(self, result):
        return result is not None


not_none_break = NotNoneBreak()
