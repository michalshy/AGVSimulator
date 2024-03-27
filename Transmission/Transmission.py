import socket
import Config


class Transmission:

    def __init__(self, cfg: Config):
        self._host = cfg.Config.getHost(cfg)
