from tau_bench.envs.incident_management_technical.data import load_data
from tau_bench.envs.incident_management_technical.rules import RULES
from tau_bench.envs.incident_management_technical.tools import ALL_TOOLS_INTERFACE_1, ALL_TOOLS_INTERFACE_2, ALL_TOOLS_INTERFACE_3, ALL_TOOLS_INTERFACE_4, ALL_TOOLS_INTERFACE_5
from tau_bench.envs.base import Env
from typing import Optional, Union
from tau_bench.envs.user import UserStrategy
import os


class MockIncidentManagementTechnicalDomainEnv(Env):
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
                from tau_bench.envs.incident_management_technical.tasks_test import TASKS_TEST as tasks
            case "test_interface_1":
                from tau_bench.envs.incident_management_technical.interface_1_tasks import INTERFACE_1_TEST as tasks
            case "test_interface_2":
                from tau_bench.envs.incident_management_technical.interface_2_tasks import INTERFACE_2_TEST as tasks
            case "test_interface_3":
                from tau_bench.envs.incident_management_technical.interface_3_tasks import INTERFACE_3_TEST as tasks
            case "test_interface_4":
                from tau_bench.envs.incident_management_technical.interface_4_tasks import INTERFACE_4_TEST as tasks
            case "test_interface_5":
                from tau_bench.envs.incident_management_technical.interface_5_tasks import INTERFACE_5_TEST as tasks
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
            
        # Load wiki based on interface_num
        folder_path = os.path.dirname(__file__)
        match interface_num:
            case 1:
                wiki_path = os.path.join(folder_path, "tools", "interface_1", "policy.md")
            case 2:
                wiki_path = os.path.join(folder_path, "tools", "interface_2", "policy.md")
            case 3:
                wiki_path = os.path.join(folder_path, "tools", "interface_3", "policy.md")
            case 4:
                wiki_path = os.path.join(folder_path, "tools", "interface_4", "policy.md")
            case 5:
                wiki_path = os.path.join(folder_path, "tools", "interface_5", "policy.md")
            case _:
                raise ValueError(f"Unknown interface_num: {interface_num}")
        
        with open(wiki_path, "r") as f:
            wiki = f.read()
        
        super().__init__(
            data_load_func=load_data,
            tools=tools,
            tasks=tasks,
            wiki=wiki,
            rules=RULES,
            user_strategy=user_strategy,
            user_model=user_model,
            user_provider=user_provider,
            task_index=task_index,
        )
        self.terminate_tools = ["transfer_to_human_agents"]