from typing import List

from almanak.interface.contract import ContractInterface
from almanak.interface.custom_protocol import CustomProtocolInterface
from almanak.interface.metric_helper import MetricHelperInterface
from almanak.interface.token import TokenInterface


class Custom(CustomProtocolInterface):
    def __init__(self, contracts: List[ContractInterface], tokens: List[TokenInterface], settings: dict, metric_helper: MetricHelperInterface):
        self._contracts = contracts
        self._tokens = tokens
        self._settings = settings
        self._metric_helper = metric_helper

    def initialize(self):
        return

    def get_pool_address(self, token_a: str, token_b: str, fee: int):
        """
        Return the pool address to the respective information

        """
        return None