
from abc import ABCMeta, abstractmethod
from typing import Dict


class AbstractFilter(metaclass=ABCMeta):
    @abstractmethod
    def execute(self, params: Dict) -> Dict:
        pass
