from .model import Model


class KokkaiClusterLink(Model):
    from_cluster: str
    to_cluster: str
