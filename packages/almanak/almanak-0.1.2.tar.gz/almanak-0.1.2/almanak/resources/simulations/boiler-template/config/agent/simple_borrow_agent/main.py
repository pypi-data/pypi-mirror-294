from almanak.interface.agent_base import BaseAgent
from almanak.interface.agent_helper import AgentHelperInterface
from almanak.interface.environment_helper import EnvironmentHelperInterface
from almanak.interface.metric_helper import MetricHelperInterface
from almanak.interface.simulation_state_helper import SimulationStateHelperInterface
from almanak.interface.strategy import StrategyInterface


class SimpleBorrower(BaseAgent):
    def __init__(self, strategy: StrategyInterface, agent_helper: AgentHelperInterface, metric_helper: MetricHelperInterface):
        super().__init__(strategy, agent_helper, metric_helper)
        self.strategy = strategy
        self.agent_helper = agent_helper

    def agent_initialization(self, simulation_state: SimulationStateHelperInterface):
        super().agent_initialization(simulation_state)

    def agent_pre_step(self, simulation_state: SimulationStateHelperInterface):
        '''
        This is a simple borrow agent. This is what they should do:

        1. Approves tx and supplies a token to Aave.
        2. Borrows some token agains the supplied collateral.
        3. Reapys their debt at a later time.
        4. Withdraws funds from Aave at the end of the simulation.
        '''

        # get the settings from the agent
        settings = self.agent_helper.get_settings()

        initial_collateral_token: str = settings.get("initial_collateral_token")
        initial_collateral_amount: int = settings.get("initial_collateral_amount")
        initial_borrow_amount: int = settings.get("initial_borrow_amount")
        initial_borrow_token: str = settings.get("initial_borrow_token")
        protocol: str = settings.get("protocol")

        for environment in self.agent_helper.get_environments():

            lending_protocol = environment.get_protocol(protocol)
            if lending_protocol is None:
                raise Exception(f"{protocol} protocol not found")

            agent_address = self.agent_helper.get_address(environment.get_alias())
            if agent_address is None:
                raise Exception(f'Agent address not found for {environment.get_alias()}')

            print(f"Agent {agent_address} is initializing")
            # as a first step, this agent deposits and borrows some amount of tokens specified in the config file/
            # deposits

            
            usdc_balance = environment.get_token("WBTC").get_balance(agent_address)
            print(f'Agent {agent_address} has {usdc_balance} tokens of {initial_collateral_token}')
            usdc_allowance = environment.get_token("WBTC").get_allowance(agent_address, lending_protocol.lending.pool_contract.address)
            print(f'Agent {agent_address} has {usdc_allowance} allowance for {initial_collateral_token}')
            eth_balance = environment.get_token('ETH').get_balance(agent_address)
            print(f'Agent {agent_address} has {eth_balance} tokens of ETH')

            match simulation_state.current_step:
                case 2:
                    print('Supplying...')
                    lending_protocol.lending.supply(
                        from_address=agent_address,
                        asset=initial_collateral_token,
                        amount=initial_collateral_amount
                    )
                    print(f'Agent will supply {initial_collateral_amount} tokens of {initial_collateral_token}')
                case 3:
                    print('Initial Borrow...')
                    lending_protocol.lending.borrow(
                        from_address=agent_address,
                        asset=initial_borrow_token,
                        amount=initial_borrow_amount,
                        rate=2,
                        onBehalfOf=agent_address,
                    )
                    print('Borrowed!')
        super().agent_pre_step(simulation_state)

    def agent_step(self, environment_helper: EnvironmentHelperInterface, simulation_state: SimulationStateHelperInterface):
        super().agent_step(environment_helper, simulation_state)

        lending_protocol = environment_helper.get_protocol(self.agent_helper.get_settings().get("protocol"))
        if lending_protocol is None:
            raise Exception("AaveV3 protocol not found")

        agent_address = self.agent_helper.get_address(environment_helper.get_alias())
        if agent_address is None:
            raise Exception(f'Agent address not found for {environment_helper.get_alias()}')

        settings = self.agent_helper.get_settings()

        repay_step: int = settings.get("repay_step")
        initial_borrow_amount: int = settings.get("initial_borrow_amount")
        initial_borrow_token: str = settings.get("initial_borrow_token")

        print(repay_step)

        if simulation_state.current_step != repay_step:
            print(f' step {simulation_state.current_step}, not time to repay yet')
        else:
            print(f' step {simulation_state.current_step}, time to repay!')
            lending_protocol.lending.repay(
                from_address=agent_address,
                asset=initial_borrow_token,
                amount=initial_borrow_amount,
                interestRateMode=1,
                onBehalfOf=agent_address
            )
            print('repayed loan')


        if simulation_state.current_step==simulation_state.steps:
            print('Withdraws funds')

            # gets the data related to the loan.
            data = lending_protocol.lending.fetch_positions(
                agent_address
            )

            # withdraws the funds
            lending_protocol.lending.withdraw(
                from_address=agent_address,
                asset=initial_borrow_token,
                amount=initial_borrow_amount,
                onBehalfOf=agent_address
            )

    def agent_post_step(self, simulation_state: SimulationStateHelperInterface):
        super().agent_post_step(simulation_state)

    def agent_teardown(self, simulation_state: SimulationStateHelperInterface):
        super().agent_teardown(simulation_state)

    def current_net_worth(self):
        # For an LP agent you would need to retreive this in a different location from
        # a trader agent.
        pass
