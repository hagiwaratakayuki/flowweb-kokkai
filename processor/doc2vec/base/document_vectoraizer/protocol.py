from abc import ABCMeta


class AbstractDocumentVectoraizer(metaclass=ABCMeta):
    def exec(self, parse_result, dto):
        pass
