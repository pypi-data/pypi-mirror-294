from abc import abstractmethod
from typing import Any, Dict, List
from almanak.interface.agent_helper import AgentHelperInterface
from almanak.interface.environment_helper import EnvironmentHelperInterface
from almanak.interface.sim_metric import GlobalMetricInterface
from almanak.interface.simulation_state_helper import SimulationStateHelperInterface

class AmazingGlobalMetric(GlobalMetricInterface):
    @staticmethod
    @abstractmethod
    def collect_metric(agents: List[AgentHelperInterface], environments: List[EnvironmentHelperInterface], simulation_state: SimulationStateHelperInterface) -> Dict[str, Any]:
        return {}