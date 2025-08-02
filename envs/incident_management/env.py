# Copyright Sierra

from tau_bench.envs.incident_management.data import load_data
from tau_bench.envs.incident_management.rules import RULES
from tau_bench.envs.incident_management.tools import (
    ALL_TOOLS_INTERFACE_1,
    ALL_TOOLS_INTERFACE_2,
    ALL_TOOLS_INTERFACE_3,
    ALL_TOOLS_INTERFACE_4,
    ALL_TOOLS_INTERFACE_5,
)
from tau_bench.envs.incident_management.wiki import WIKI
from tau_bench.envs.base import Env
from typing import Optional, Union
from tau_bench.envs.user import UserStrategy


class MockIncidentManagementDomainEnv(Env):
    def __init__(
        self,
        user_strategy: Union[str, UserStrategy] = UserStrategy.LLM,
        user_model: str = "gpt-4o",
        user_provider: Optional[str] = None,
        task_split: str = "test",
        task_index: Optional[int] = None,
        interface_num: Optional[int] = None,
    ):
        match task_split:
            case "test":
                from tau_bench.envs.incident_management.tasks import tasks
            case "test_interface_1":
                from tau_bench.envs.incident_management.interface_1_tasks import INTERFACE_1_TEST as tasks
            case "test_interface_2":
                from tau_bench.envs.incident_management.interface_2_tasks import INTERFACE_2_TEST as tasks
            case "test_interface_3":
                from tau_bench.envs.incident_management.interface_3_tasks import INTERFACE_3_TEST as tasks
            case "test_interface_4":
                from tau_bench.envs.incident_management.interface_4_tasks import INTERFACE_4_TEST as tasks
            case "test_interface_5":
                from tau_bench.envs.incident_management.interface_5_tasks import INTERFACE_5_TEST as tasks
            case _:
                raise ValueError(f"Unknown task split: {task_split}")
        
        # Select tools based on interface_num
        match interface_num:
            case 1:
                tools = ALL_TOOLS_INTERFACE_1
            case 2:
                tools = ALL_TOOLS_INTERFACE_2
            case 3:
                tools = ALL_TOOLS_INTERFACE_3
            case 4:
                tools = ALL_TOOLS_INTERFACE_4
            case 5:
                tools = ALL_TOOLS_INTERFACE_5
            case _:
                raise ValueError(f"Unknown interface_num: {interface_num}")
        
        super().__init__(
            data_load_func=load_data,
            tools=tools,
            tasks=tasks,
            wiki=WIKI,
            rules=RULES,
            user_strategy=user_strategy,
            user_model=user_model,
            user_provider=user_provider,
            task_index=task_index,
        )
        self.terminate_tools = ["transfer_to_human_agents"]
