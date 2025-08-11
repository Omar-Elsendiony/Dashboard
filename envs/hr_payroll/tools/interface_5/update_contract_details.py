import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class UpdateContractDetails(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        contract_id: str = None,
        worker_id: str = None,
        organization_id: str = None,
        document_id: str = None,
        updates: Dict[str, Any] = {}
    ) -> str:
        contracts = data.get("contracts", {})
        
        def find_contract():
            if contract_id:
                if contract_id not in contracts:
                    raise ValueError("Contract not found with given contract_id")
                return contract_id
            # Try worker_id + org_id
            matches = [
                cid for cid, c in contracts.items()
                if c.get("worker_id") == worker_id and c.get("organization_id") == organization_id
            ] if worker_id and organization_id else []
            
            # If not found, try worker_id + document_id
            if not matches and worker_id and document_id:
                matches = [
                    cid for cid, c in contracts.items()
                    if c.get("worker_id") == worker_id and c.get("document_id") == document_id
                ]

            if len(matches) == 1:
                return matches[0]
            elif not matches:
                raise ValueError("No matching contract found")
            else:
                raise ValueError("Multiple matching contracts found")

        matched_id = find_contract()

        valid_fields = {
            "rate", "rate_type", "start_date", "end_date",
            "status", "currency", "document_id"
        }

        contract = contracts[matched_id]
        for field, value in updates.items():
            if field in valid_fields:
                contract[field] = value

        return json.dumps({"contract_id": matched_id, **contract})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_contract_details",
                "description": (
                    "Updates a contract using contract_id or using a combination of "
                    "worker_id + organization_id or worker_id + document_id. Supports updating "
                    "rate, rate_type, start_date, end_date, status, currency, and document_id."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "contract_id": {
                            "type": "string",
                            "description": "Unique contract ID (primary match method)"
                        },
                        "worker_id": {
                            "type": "string",
                            "description": "Worker ID (used in fallback primary key combinations)"
                        },
                        "organization_id": {
                            "type": "string",
                            "description": "Organization ID (used with worker_id to identify contract)"
                        },
                        "document_id": {
                            "type": "string",
                            "description": "Document ID (used with worker_id to identify contract)"
                        },
                        "updates": {
                            "type": "object",
                            "description": "Fields to update in the contract",
                            "properties": {
                                "rate": {"type": "number"},
                                "rate_type": {"type": "string"},
                                "start_date": {"type": "string"},
                                "end_date": {"type": "string"},
                                "status": {"type": "string"},
                                "currency": {"type": "string"},
                                "document_id": {"type": "string"}
                            }
                        }
                    },
                    "required": ["updates"]
                }
            }
        }
