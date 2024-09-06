from almanak.interface.agent import AgentInterface
from almanak.interface.agent_helper import AgentHelperInterface
from almanak.interface.environment_helper import EnvironmentHelperInterface
from almanak.interface.metric_helper import MetricHelperInterface
from almanak.interface.simulation_state_helper import SimulationStateHelperInterface
from almanak.interface.strategy import StrategyInterface


class DeFiAgent(AgentInterface):
    def __init__(self, strategy: StrategyInterface, agent_helper: AgentHelperInterface, metric_helper: MetricHelperInterface):
        self.strategy = strategy
        self.agent_helper = agent_helper
        self.metric_helper = metric_helper

    def agent_initialization(self, simulation_state: SimulationStateHelperInterface):
        self.strategy.strategy_initialization(simulation_state)

    def agent_pre_step(self, simulation_state: SimulationStateHelperInterface):
        self.strategy.strategy_pre_step(simulation_state)

    def agent_step(self, environment_helper: EnvironmentHelperInterface, simulation_state: SimulationStateHelperInterface):
        self.strategy.strategy_step(environment_helper, simulation_state)

    def agent_post_step(self, simulation_state: SimulationStateHelperInterface):
        self.strategy.strategy_post_step(simulation_state)

    def agent_teardown(self, simulation_state: SimulationStateHelperInterface):
        self.strategy.strategy_teardown(simulation_state)
