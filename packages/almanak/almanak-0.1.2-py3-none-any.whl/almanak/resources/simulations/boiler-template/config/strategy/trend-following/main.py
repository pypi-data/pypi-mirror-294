from typing import List

from almanak.interface.agent_helper import AgentHelperInterface
from almanak.interface.environment_helper import EnvironmentHelperInterface
from almanak.interface.metric_helper import MetricHelperInterface
from almanak.interface.model_helper import ModelHelperInterface
from almanak.interface.simulation_state_helper import SimulationStateHelperInterface
from almanak.interface.strategy import StrategyInterface


class StrategyTrendFollowing(StrategyInterface):
    def __init__(
        self,
        agent_helper: AgentHelperInterface,
        environment_helper: EnvironmentHelperInterface,
        models: List[ModelHelperInterface],
        metric_helper: MetricHelperInterface,
    ):
        super().__init__(agent_helper, environment_helper, models, metric_helper)
        self.agent_helper = agent_helper
        self.environment_helper = environment_helper
        self.models = models
        self.metric_helper = metric_helper

    def strategy_initialization(self, simulation_state: SimulationStateHelperInterface):
        pass

    def strategy_pre_step(self, simulation_state: SimulationStateHelperInterface):
        pass

    def strategy_step(self, environment_helper: EnvironmentHelperInterface, simulation_state: SimulationStateHelperInterface):
        print("Strategy step")
        print(f"Models[0]: {self.models[0]}")
        print(f"Models[0].predict([1, 2, 3, 4]): {self.models[0].predict([1, 2, 3, 4])}")

    def strategy_post_step(self, simulation_state: SimulationStateHelperInterface):
        pass

    def strategy_teardown(self, simulation_state: SimulationStateHelperInterface):
        pass

    def predict_trend(self):
        return -2.5
