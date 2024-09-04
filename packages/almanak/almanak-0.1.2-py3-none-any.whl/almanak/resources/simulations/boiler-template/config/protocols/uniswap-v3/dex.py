import math
import time
from typing import List

from almanak.interface.contract import ContractInterface
from almanak.interface.dex import DexInterface
from almanak.interface.metric_helper import MetricHelperInterface
from almanak.interface.token import TokenInterface


class UniswapDex(DexInterface):
    def __init__(self, contracts: List[ContractInterface], tokens: List[TokenInterface], settings: dict, metric_helper: MetricHelperInterface):
        self._contracts = contracts
        self._tokens = tokens
        self._settings = settings

        # Initialize values relevant to UniswapV3 on Ethereum
        self.UNISWAP_TICK_SPACING = {100: 1, 500: 10, 3_000: 60, 10_000: 200}
        self.MAX_UINT_128 = 2**128 - 1
        self.MAX_UINT_256 = 2**256 - 1
        self.UNISWAP_MIN_TICK = -887272
        self.UNISWAP_MAX_TICK = -self.UNISWAP_MIN_TICK
        self.Q96 = 2**96
        self.Q128 = 2**128
        self.deadline = int(math.floor(time.time()) + 3600)  # hardcode

        self.UNISWAP_V3_FACTORY_ADDRESS = "0x1F98431c8aD98523631AE4a59f267346ea31F984"
        self.UNISWAP_V3_ROUTER_ADDRESS = "0x68b3465833fb72A70ecDF485E0e4C7bD8665Fc45"
        self.UNISWAP_V3_POSITION_MANAGER_ADDRESS = (
            "0xC36442b4a4522E871399CD717aBDD847Ab11FE88"
        )
        self.UNISWAP_V3_QUOTER_ADDRESS = "0xb27308f9F90D607463bb33eA1BeBb41C27CE5AB6"
        self.WETH_ADDRESS = "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"


    def initialize(self):
        # For every token the agent has, approve uniswapv3 as spender.
        token_symbols_held = agent.get_wallet().get_token_names()

        for _token_symbol in token_symbols_held:
            # ETH doesnt get approved
            if _token_symbol == "ETH":
                continue

            # Approve uniswap v3 router address
            _token_class = self.chain.get_token(_token_symbol)
            _token_class.approve(
                wallet=agent.get_address(),
                spender=self.UNISWAP_V3_ROUTER_ADDRESS,
                amount=int(2**256 - 1),
            )
            self.chain.mine()

            # Approve uniswap v3 position manager address
            # Technically only lps need this, but just approve every agent.
            _token_class = self.chain.get_token(_token_symbol)
            _token_class.approve(
                wallet=agent.get_address(),
                spender=self.UNISWAP_V3_POSITION_MANAGER_ADDRESS,
                amount=int(2**256 - 1),
            )
            self.chain.mine()

    def swap(self,
            tokenIn: str,
            tokenOut: str,
            amount: int,
            from_address: str,
            **kwargs):
        """
        A function to execute the exactInputSingle function from the uniswap v3
        swap_router smart contract.
        https://docs.uniswap.org/contracts/v3/guides/swaps/single-swaps#exact-input-swaps

        Performs a single swap from one token to another token on uniswap v3,
        by providing an exact amount of tokenIn inputted

        Parameters
        ------------
        tokenIn: str
            the address of the input token
        tokenOut: str
            the address of the output token
        amountIn: int
            the exact amount of tokenIn tokens to input into the swap
        from_address: str
            the address initiating the swap
        transfer_eth_in: bool
            if True, sends ETH into the swap contract to swap ETH to tokenIn
            then swap tokenIn to tokenOut
            if False, does not send ETH to swap contract, and directly swaps
            tokenIn for tokenOut

        Returns
        ------------
        tx_hash: str
            the transaction hash

        """
        # Instantiate the transaction fields
        transaction_details = {"from": from_address}

        # If the input token is WETH, transfer ETH to smart contract instead of swapping WETH
        # get_token_address('ETH') returns WETH address
        # if (tokenIn == self.get_token_address('ETH')):
        if transfer_eth_in:
            transaction_details["value"] = amountIn

        fee = 3000

        if kwargs['fee']:
            fee = kwargs['fee']

        tx_hash = self.client.univ3_router.exactInputSingle(
            (
                tokenIn,
                tokenOut,
                fee,
                from_address,
                int(amount),
                0,
                0,
            )
        ).transact(transaction_details)

        # If Anvil is set to automine, then a transaction receipt is returned
        # from transact(). Otherwise a transaction hash is returned
        if not isinstance(tx_hash, HexBytes):
            tx_hash = tx_hash["transactionHash"]

        return tx_hash

    def swap_output(self, params):
        raise NotImplementedError

    def quote_input(self, params):
        raise NotImplementedError

    def open_position(self, params):
        raise NotImplementedError

    def add_liquidity(self, params):
        raise NotImplementedError

    def remove_liquidity(self, params):
        raise NotImplementedError