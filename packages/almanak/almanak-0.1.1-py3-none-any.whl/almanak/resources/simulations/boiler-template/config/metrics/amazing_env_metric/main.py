from typing import Any, Dict
from almanak.interface.environment_helper import EnvironmentHelperInterface
from almanak.interface.env_metric import EnvironmentMetricInterface
from almanak.interface.simulation_state_helper import SimulationStateHelperInterface

class AmazingEnvMetric(EnvironmentMetricInterface):
    @staticmethod
    def collect_metric(environment_helper: EnvironmentHelperInterface, simulation_state: SimulationStateHelperInterface) -> Dict[str, Any]:
        return {}