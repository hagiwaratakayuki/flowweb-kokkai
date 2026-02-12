from abc import ABCMeta, abstractmethod


class AbstractDocumentVectoraizer(metaclass=ABCMeta):
    @abstractmethod
    def exec(self. parse_result, data):
        pass
