from .model import Model


class NodeBody(Model):
    body: str = ''

    def __init__(self, *args, **kwargs) -> None:

        super(NodeBody, self).__init__(entity_options={
            "exclude_from_indexes": ("data", "title", )}, *args, **kwargs)
