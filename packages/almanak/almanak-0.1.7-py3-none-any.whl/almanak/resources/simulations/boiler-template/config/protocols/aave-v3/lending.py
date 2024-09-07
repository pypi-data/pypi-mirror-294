import math
import time
from typing import List

from almanak.interface.contract import ContractInterface
from almanak.interface.lending import LendingInterface, LendingPortfolio
from almanak.interface.metric_helper import MetricHelperInterface
from almanak.interface.token import TokenInterface


class AaveLending(LendingInterface):
    def __init__(self, contracts: List[ContractInterface], tokens: List[TokenInterface], settings: dict, metric_helper: MetricHelperInterface):
        contracts[0].is_dynamic

        self.contracts = contracts
        self.tokens = tokens
        self.settings = settings
        self.metric_helper = metric_helper

        # get contract with name aave_pool
        _pool_contract = next((contract for contract in self.contracts if contract.name == "aave_pool"), None)
        if _pool_contract is None:
            raise ValueError("Aave pool contract not found")
        else:
            self.pool_contract: ContractInterface = _pool_contract

        # Initialize values relevant to AaveV3 on Ethereum
        self.BASE = 10**8
        self.deadline = int(math.floor(time.time()) + 3600) # hardcode

    def initialize(self, agent_addresses: list[str]) -> None:
        """
        Initialize the Aave V3 pool.
        """
        for agent_address in agent_addresses:
            for token in self.tokens:
                if token.symbol == "USDC":
                    continue
                print(f"Approving {token.symbol} for agent {agent_address}")
                token.approve(
                    from_address=agent_address,
                    spender=self.pool_contract.address,
                    amount=int(2**256 - 1)
                )
        return

    def supply(self,
        from_address: str,
        asset: str,
        amount: int,
        **kwargs
    ) -> str:
        """
        A wrapper to the Supply function in Aave V3 pool.
        Remember that since Aave is trustless, it is overcollateralized, and as such,
        you can only borrow into it if you have deposited before, and will only be able to
        borrow an amount B=r*DEPOSIT, with r\in[0,1] the loan to vault ratio
        c.f https://docs.aave.com/developers/core-contracts/pool#supply

        Parameters
        ------------
        from_address: str,
            the address performing the transaction
        asset: str
            the address of the token to be supplied
        amount: int
            the amount of tokenIn to be supplied

        Returns
        ------------
        tx_hash:
            the transaction hash from the transaction
        """
        # self.approve_contract(fromAddress)

        transaction_details = {"from": from_address}

        tx_hash = self.pool_contract.functions.supply(
            asset,
            amount,
            from_address,
            kwargs.get("referralCode", 0)
        ).transact(transaction_details)

        return tx_hash.hex()


    def borrow(
        self,
        from_address: str,
        asset: str,
        amount: int,
        rate: int,
        **kwargs
    ) -> str:
        """
        A wrapper to the borrow function in Aave V3 pool.
        Borrows amount of asset with interestRateMode (Stable: 1, Variable: 2), sending the amount to msg.sender,
        with the debt being incurred by onBehalfOf.
        Remember that since Aave is trustless, it is overcollateralized, and as such,
        you can only borrow into it if you have deposited before, and will only be able to
        borrow an amount B=r*DEPOSIT, with r\in[0,1] the loan to vault ratio
        c.f https://docs.aave.com/developers/core-contracts/pool#borrow

        Parameters
        ------------
        from_address: str,
            the address performing the transaction
        asset: str
            the address of the token to be supplied
        amount: int
            the amount of tokenIn to be supplied
        rate: int
            The type of interest rate on the loan. Stable: 1, Variable: 2

        Returns
        ------------
        tx_hash:
            the transaction hash from the transaction

        """

        # Instantiate the transaction fields
        transaction_details = {"from": from_address}

        tx_hash = self.pool_contract.functions.borrow(
            asset,
            amount,
            rate,
            kwargs.get("referralCode", 0),
            kwargs.get("onBehalfOf", from_address)
        ).transact(transaction_details)

        return tx_hash.hex()

    def repay(
        self,
        from_address: str,
        asset: str,
        amount: int,
        **kwargs
    ) -> str:
        """
        A wrapper to the repay function in Aave V3 pool.
        function repay(address asset, uint256 amount, uint256 rateMode, address onBehalfOf)
        Repays onBehalfOf's debt amount of asset which has a rateMode.
        c.f https://docs.aave.com/developers/core-contracts/pool#repay

        Parameters
        ------------
        fromAddress: s  r,
            the address performing the transaction
        tokenIn: str
            the address of the token to be supplied
        AmountIn: int
            the amount of tokenIn to be supplied
        interestRateMode: int
            The type of interest rate on the loan. Stable: 1, Variable: 2
        onBehalfOf: str
            the address receiving the loan the deposit

        Returns
        ------------
        tx_hash:
            the transaction hash from the transaction
        """

        # Instantiate the transaction fields
        transaction_details = {"from": from_address}

        tx_hash = self.pool_contract.functions.repay(
            asset,
            amount,
            kwargs.get("interestRateMode", 1),
            kwargs.get("onBehalfOf", from_address)
        ).transact(transaction_details)

        return tx_hash.hex()

    def withdraw(
        self,
        from_address: str,
        asset: str,
        amount: int,
        **kwargs
    ) -> str:
        """
        function withdraw(address asset, uint256 amount, address to)
        Withdraws amount of the underlying asset, i.e. redeems the underlying token and burns the aTokens.
        If user has any existing debt backed by the underlying token, then the max amount available to withdraw
        is the amount that will not leave user health factor < 1 after withdrawal.
        c.f https://docs.aave.com/developers/core-contracts/pool#withdraw

        Parameters
        ------------
        from_address: str,
            the address performing the transaction
        asset: str
            the address of the token to be supplied
        amount: int
            the amount of tokenIn to be supplied

        Returns
        ------------
        tx_hash:
            the transaction hash from the transaction



        """

        # Instantiate the transaction fields
        transaction_details = {"from": from_address}

        tx_hash = self.pool_contract.functions.withdraw(
                asset,
                amount,
                kwargs.get("onBehalfOf", from_address)
        ).transact(transaction_details)

        return tx_hash.hex()

    def liquidate(
        self,
        from_address: str,
        user: str,
        debt: str,
        collateral: str,
        amount: int,
        receive_collateral: bool,
        **kwargs
    ) -> str:
        """
        function liquidationCall(address collateral, address debt,
        address user, uint256 debtToCover, bool receiveAToken)
        Liquidate positions with a health factor below 1.
        When the health factor of a position is below 1, liquidators repay part or
        all of the outstanding borrowed amount on behalf of the borrower,
        while receiving a discounted amount of collateral in return
        (also known as a liquidation 'bonus"). Liquidators can decide if they want
        to receive an equivalent amount of collateral aTokens instead of the underlying asset.
        When the liquidation is completed successfully, the health factor of the position is increased,
        bringing the health factor above 1.
        c.f https://docs.aave.com/developers/core-contracts/pool#liquidationCall

        Parameters
        ------------
        fromAddress: str,
            the address performing the transaction
        collateral: str,
            address of the collateral reserve
        debt: str,
            address of the debt reserve
        user: str,
            address of the borrower
        amount: int,
            amount of asset debt that the liquidator will repay.
            -1 means repay all the debt
        receive_collateral: bool =False
            wether user wants to get aTokens equivalent. Default is False.

        Returns
        ------------
        tx_hash:
            the transaction hash from the transaction
        """
        # Instantiate the transaction fields
        transaction_details = {"from": from_address}

        tx_hash = self.pool_contract.functions.liquidationCall(
                collateral,
                debt,
                user,
                amount,
                receive_collateral
            ).transact(transaction_details)

        return tx_hash.hex()

    def fetch_positions(
        self,
        from_address: str
        ) -> LendingPortfolio:
        """
        Returns the user account data across all the reserves

        c.f https://docs.aave.com/developers/core-contracts/pool#getUserAccountData

        Parameters
        ------------
        user: str,
            address of the borrower
        Returns
        ------------
        user_data: dict, with:
            'total collateral base':data[0],
            'total debt base':data[1],
            'available borrow base':data[2],
            'current liq. threshold':data[3],
            'LTV':data[4],
            'health':data[5]

        """


        # data = self.pool_contract.functions.getUserAccountData(from_address).call()
        # user_data={'total collateral base':data[0],
        #     'total debt base':data[1],
        #     'available borrow base':data[2],
        #     'current liq. threshold':data[3],
        #     'LTV':data[4],
        #     'health':data[5]}
        # return user_data
        return LendingPortfolio(
            supplied=[],
            borrowed=[],
        )

    # def get_position_health(
    #     self,
    #     from_address: str
    #     ) -> float:
    #     """
    #     Returns the health factor of the respective account

    #     c.f https://docs.aave.com/developers/core-contracts/pool#getUserAccountData

    #     Parameters
    #     ------------
    #     user: str,
    #         address of the borrower
    #     Returns
    #     ------------
    #     health_factor: float,
    #         health factor of respective account

    #     """


    #     data = self.pool_contract.functions.getUserAccountData(from_address).call()
    #     health_factor = data[5]
    #     return health_factor

    def check_user_collateral(self, w3, pool_address, user_address):
        # ABI for getUserAccountData function
        abi = [{
            "inputs": [{"internalType": "address","name": "user","type": "address"}],
            "name": "getUserAccountData",
            "outputs": [
                {"internalType": "uint256","name": "totalCollateralBase","type": "uint256"},
                {"internalType": "uint256","name": "totalDebtBase","type": "uint256"},
                {"internalType": "uint256","name": "availableBorrowsBase","type": "uint256"},
                {"internalType": "uint256","name": "currentLiquidationThreshold","type": "uint256"},
                {"internalType": "uint256","name": "ltv","type": "uint256"},
                {"internalType": "uint256","name": "healthFactor","type": "uint256"}
            ],
            "stateMutability": "view",
            "type": "function"
        }]

        pool_contract = w3.eth.contract(address=pool_address, abi=abi)
        
        account_data = pool_contract.functions.getUserAccountData(user_address).call()
        
        print(f"Total Collateral (in base currency): {account_data[0]}")
        print(f"Total Debt (in base currency): {account_data[1]}")
        print(f"Available Borrows (in base currency): {account_data[2]}")
        print(f"Current Liquidation Threshold: {account_data[3]}")
        print(f"Loan to Value: {account_data[4]}")
        print(f"Health Factor: {account_data[5]}")

        return account_data

    def validation(self, pool_contract: ContractInterface, from_address: str, asset_address: str, amount: int) -> bool:

        pool_contract_address = pool_contract._w3.to_checksum_address(pool_contract.address)
        is_borrowable = self.check_asset_borrowable(pool_contract._w3, pool_contract_address, asset_address)

        if not is_borrowable:
            print("This asset is not available for borrowing on Aave V3.")

        account_data = self.check_user_collateral(pool_contract._w3, pool_contract_address, from_address)

        if account_data[2] < amount:
            print("Insufficient collateral to cover the new borrow amount.")


    def check_asset_borrowable(self, w3, pool_address, asset_address):
        # ABI for getReserveData function
        abi = [{
            "inputs": [{"internalType": "address","name": "asset","type": "address"}],
            "name": "getReserveData",
            "outputs": [
                {"internalType": "uint256","name": "configuration","type": "uint256"},
                {"internalType": "uint128","name": "liquidityIndex","type": "uint128"},
                {"internalType": "uint128","name": "currentLiquidityRate","type": "uint128"},
                {"internalType": "uint128","name": "variableBorrowIndex","type": "uint128"},
                {"internalType": "uint128","name": "currentVariableBorrowRate","type": "uint128"},
                {"internalType": "uint128","name": "currentStableBorrowRate","type": "uint128"},
                {"internalType": "uint40","name": "lastUpdateTimestamp","type": "uint40"},
                {"internalType": "uint16","name": "id","type": "uint16"},
                {"internalType": "address","name": "aTokenAddress","type": "address"},
                {"internalType": "address","name": "stableDebtTokenAddress","type": "address"},
                {"internalType": "address","name": "variableDebtTokenAddress","type": "address"},
                {"internalType": "address","name": "interestRateStrategyAddress","type": "address"},
                {"internalType": "uint128","name": "accruedToTreasury","type": "uint128"},
                {"internalType": "uint128","name": "unbacked","type": "uint128"},
                {"internalType": "uint128","name": "isolationModeTotalDebt","type": "uint128"}
            ],
            "stateMutability": "view",
            "type": "function"
        }]

        pool_contract = w3.eth.contract(address=pool_address, abi=abi)
        
        reserve_data = pool_contract.functions.getReserveData(asset_address).call()
        
        print(reserve_data)
        # The 'configuration' field contains various flags, including whether the asset is borrowable
        configuration = reserve_data[0]
        
        # Check if the asset is borrowable (bit 58 in the configuration)
        is_borrowable = (configuration >> 58) & 1
        
        print(f"Asset borrowable: {bool(is_borrowable)}")
        return bool(is_borrowable)