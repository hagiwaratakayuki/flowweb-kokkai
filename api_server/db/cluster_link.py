from .model import Model


class ClusterLink(Model):
    link_start: str
    link_target: str
    link_count: int

    def __init__(self, id=None) -> None:
        super().__init__(id, entity_options={
            "exclude_from_indexes": ("link_target",)})
