from typing import Any, Dict

from almanak.interface.agent_helper import AgentHelperInterface
from almanak.interface.agent_metric import AgentMetricInterface
from almanak.interface.simulation_state_helper import SimulationStateHelperInterface


class AmazingAgentMetric(AgentMetricInterface):
    @staticmethod
    def collect_metric(agent_helper: AgentHelperInterface, simulation_state: SimulationStateHelperInterface) -> Dict[str, Any]:
        pnl = 0

        stables = ["usdc", "usdt", "dai"]
        for environment_helper in agent_helper.get_environments():
            agent_address = agent_helper.get_address(environment_helper.get_alias())
            if agent_address is None:
                raise Exception(f"Agent address not found for {environment_helper.get_alias()}")

            # for asset in ['weth', 'usdc']:
            for asset in simulation_state.price_feeds:
                token1 = environment_helper.get_token(asset[0])
                token2 = environment_helper.get_token(asset[1])
                if token1 is not None:
                    count1 = token1.get_balance(agent_address)
                    if token1.symbol.lower() in stables:
                        price = 1
                    else:
                        price = simulation_state.price_feeds[asset].get_price(simulation_state.current_step - 1)

                    pnl += count1 * price

                if token2 is not None:
                    count2 = token2.get_balance(agent_address)

                    if token2.symbol.lower() in stables:
                        price = 1
                    else:
                        price = simulation_state.price_feeds[asset].get_price(simulation_state.current_step - 1)

                    pnl += count2 * price

        return {"pnl": pnl}
