import math
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional, Dict, Union, List, Type


class Metric(ABC):
    """
    The Metric Abstract Base Class for all Metrics.
    """
    service: Optional[str]
    environment: str
    version: str
    application_id: str
    timestamp_millis: int
    meta: Dict[str, str]

    def __init__(self, application_id: str, version: str, environment: str, service: Optional[str] = None,
                 meta: Optional[Dict[str, str]] = None):

        super().__init__()

        if meta is None:
            meta = dict()

        self.meta = meta
        self.service = service
        self.environment = environment
        self.version = version
        self.application_id = application_id
        self.timestamp_millis = math.floor(datetime.utcnow().microsecond / 1000)

    @abstractmethod
    def index(self) -> str:
        raise NotImplementedError('subclasses must override index()!')

    def id(self):
        return '-'.join(
            filter(
                lambda x: x is not None,
                [self.application_id, self.version, self.service]
            )
        )

    def __iter__(self) -> Dict[str, Union[str, Dict[str, str]]]:
        for key in self.__dict__:
            yield key, getattr(self, key)


class Deployment(Metric, ABC):
    INDEX_NAME: str = 'deployments'

    def index(self) -> str:
        return self.INDEX_NAME


supported_metrics: List[Type[Metric]] = [
  Deployment,
]
