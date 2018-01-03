from typing import Optional

from popupdict.config import *
from popupdict.util import logger
from .client import *
from .result import QueryResult


# Query client adapter
class QueryAdapter:
    def __init__(self, config: Configuration):
        for client in valid_clients:
            if client.id == config.query_client:
                self.client = client(getattr(config, client.id.replace('-', '_')))
                break

        if not self.client:
            raise Exception("Unknown query client: {}".format(repr(config.query_client)))

    def query(self, text: str) -> Optional[QueryResult]:
        logger.debug('[%s] Query started for query=%s', self.client.id, repr(text))
        try:
            result = self.client.query(text)
            logger.debug('[%s] Query finished for query=%s, result=%s', self.client.id, repr(text), repr(result))
            return result
        except Exception as e:
            logger.exception('[%s] Query failed for query=%s', self.client.id, repr(text))
