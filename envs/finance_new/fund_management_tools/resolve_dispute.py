import json
from typing import Any, Dict, List
from tau_bench.envs.tool import Tool

class ResolveDispute(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], involved_ids: List[str], description: str, 
               evidence: Dict[str, Any]) -> str:
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        users = data.get("users", {})
        investors = data.get("investors", {})
        audit_trails = data.get("audit_trails", {})
        
        # Validate that involved parties exist (check both users and investors)
        valid_parties = []
        for party_id in involved_ids:
            if str(party_id) in users or str(party_id) in investors:
                valid_parties.append(party_id)
            else:
                return json.dumps({"success": False, "message": f"Party {party_id} not found", "halt": True})
        
        # Validate evidence is provided
        if not evidence or not isinstance(evidence, dict):
            return json.dumps({"success": False, "message": "Valid evidence dictionary required", "halt": True})
        
        # Validate description
        if not description or len(description.strip()) == 0:
            return json.dumps({"success": False, "message": "Description is required", "halt": True})
        
        # Find an admin user to log the resolution
        admin_user = None
        for user_id, user in users.items():
            if user.get("role") == "admin":
                admin_user = user_id
                break
        
        if not admin_user:
            return json.dumps({"success": False, "message": "No admin user available to process dispute", "halt": True})
        
        # Create audit trail entry for dispute resolution
        audit_id = generate_id(audit_trails)
        timestamp = "2025-10-01T00:00:00"
        
        audit_entry = {
            "audit_trail_id": audit_id,
            "reference_id": involved_ids[0],  # Use first party as reference
            "reference_type": "user",
            "action": "process",
            "user_id": admin_user,
            "field_name": "dispute_resolution",
            "old_value": "disputed",
            "new_value": f"resolved: {description}",
            "created_at": timestamp
        }
        
        audit_trails[str(audit_id)] = audit_entry
        
        return json.dumps({"success": True, "message": "Dispute resolved"})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "resolve_dispute",
                "description": "Resolve a dispute between parties with evidence",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "involved_ids": {"type": "array", "items": {"type": "string"}, "description": "IDs of involved parties"},
                        "description": {"type": "string", "description": "Description of the dispute"},
                        "evidence": {"type": "object", "description": "Evidence related to the dispute"}
                    },
                    "required": ["involved_ids", "description", "evidence"]
                }
            }
        }
