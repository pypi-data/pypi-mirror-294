from almanak.interface.agent import AgentInterface
from almanak.interface.agent_helper import AgentHelperInterface
from almanak.interface.environment_helper import EnvironmentHelperInterface
from almanak.interface.metric_helper import MetricHelperInterface
from almanak.interface.simulation_state_helper import SimulationStateHelperInterface
from almanak.interface.strategy import StrategyInterface


class Liquidator(AgentInterface):
    def __init__(self, strategy: StrategyInterface, agent_helper: AgentHelperInterface, metric_helper: MetricHelperInterface):
        super().__init__(strategy, agent_helper, metric_helper)
        self.strategy = strategy
        self.agent_helper = agent_helper
        self.liquidate = False

        # get the settings from the agent
        settings = self.agent_helper.get_settings()

        self.address = settings.get("address")

        self.protocol_lending: str = settings.get("protocol_money_market")
        self.protocol_amm: str = settings.get("protocol_amm")
        self.account_to_monitor: str = settings.get("account_to_monitor")
        self.collateral: str = settings.get("collateral")
        self.debt: str = settings.get("debt")
        self.amm_pool: str = settings.get("pool")

    def agent_initialization(self, simulation_state: SimulationStateHelperInterface):
        super().agent_initialization(simulation_state)

        """
        This class represents a potential liquidator to act on top of Aave & liquidate one account once the price
        of the collateral falls below account health.
        """

        # self.model = self.modelHelper.load(settings.get("models")["trading_prediction"])

    def agent_pre_step(self, simulation_state: SimulationStateHelperInterface):
        super().agent_pre_step(simulation_state)
        # Loop through all environments the agent is part of
        for environment in self.agent_helper.get_environments():
            protocol_lending = environment.get_protocol(self.protocol_lending)

            print(f"self.agent_helper.get_address(environment.get_alias()): {self.agent_helper.get_address(environment.get_alias())}")
            usdc_token = environment.get_token("USDC")
            weth_token = environment.get_token("WETH")
            print(f"usdc_token: {usdc_token}")
            print(
                f"usdc_token.get_balance(self.agent_helper.get_address(environment.get_alias())): {usdc_token.get_balance(self.agent_helper.get_address(environment.get_alias()))}"
            )
            print(f"weth_token: {weth_token}")
            print(
                f"weth_token.get_balance(self.agent_helper.get_address(environment.get_alias())): {weth_token.get_balance(self.agent_helper.get_address(environment.get_alias()))}"
            )

            check_liquidation_possibility = protocol_lending.lending.fetch_positions(self.account_to_monitor)

            # if check_liquidation_possibility < 0.9:
            # self.liquidate = True

    def agent_step(self, environment_helper: EnvironmentHelperInterface, simulation_state: SimulationStateHelperInterface):
        super().agent_step(environment_helper, simulation_state)
        print("liquidator step")

        environment = next(
            environment for environment in self.agent_helper.get_environments() if environment.get_alias() == environment_helper.get_alias()
        )
        protocol_lending = environment.get_protocol(self.protocol_lending)
        protocol_amm = environment.get_protocol(self.protocol_amm)
        collateral_token = environment.get_token_by_address(self.collateral)
        if collateral_token is None:
            raise ValueError(f"Collateral token {self.collateral} not found")

        txs = environment_helper.get_tx_pool()
        for tx in txs:
            print(tx)

        if self.liquidate:
            self.liquidate = False

            protocol_lending.lending.liquidate(
                self.address, collateral=self.collateral, debt=self.debt, user=self.account_to_monitor, amount=-1, receive_collateral=True
            )

            feature_vector = self.feature_vector(simulation_state)

            to_buy = self.model.predict(feature_vector)[0]

            if to_buy > 0.5:
                protocol_lending.lending.withdraw(self.address, asset=self.collateral, amount=type(int).max, to=self.address)

                amount = collateral_token.get_balance(self.address)

                protocol_amm.dex.swap(self.address, self.collateral, self.debt, amount, kwargs={"fee": 5000})

    def agent_post_step(self, simulation_state: SimulationStateHelperInterface):
        super().agent_post_step(simulation_state)

    def agent_teardown(self, simulation_state: SimulationStateHelperInterface):
        super().agent_teardown(simulation_state)

    def current_net_worth(self):
        # For an LP agent you would need to retreive this in a different location from
        # a trader agent.
        pass

    def feature_vector(self, simulation_state: SimulationStateHelperInterface):
        """
        This is querying the respective information needed for the model to predict the share to take
        Parameters
        ------------
        simulation_state: SimulationStateHelperInterface
            general state interaction

        Returns
        ------------
        feature_vector: list
            feature vector needed to get prediction for model
        """

        protocol_amm = self.agent_helper.get_environments()[0].get_protocol(self.protocol_amm)

        fee = 3000
        price_step_10 = simulation_state.get_price_feed(("ETH", "USDT")).get_price(simulation_state.current_step - 10)
        price_step = simulation_state.get_price_feed(("ETH", "USDT")).get_price(simulation_state.current_step)

        slope = (price_step - price_step_10) / price_step_10

        token_from = 0
        token_to = 1

        feature_vector = [fee, slope, token_to, token_from]

        return feature_vector
