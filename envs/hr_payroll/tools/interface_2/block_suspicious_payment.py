
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class BlockSuspiciousPayment(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], payment_id: str) -> str:
        payments = data.get("payments", {})
        if payment_id not in payments:
            raise ValueError("Payment not found")

        payment = payments[payment_id]
        if payment.get("status") == "failed":
            raise ValueError("Payment already marked as failed and cannot be reprocessed")

        payment["status"] = "blocked"
        return json.dumps({"payment_id": payment_id, "status": "blocked"})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "block_suspicious_payment",
                "description": "Blocks suspicious payment",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "payment_id": {
                            "type": "string",
                            "description": "The ID of the payment to mark as suspicious and block"
                        }
                    },
                    "required": ["payment_id"]
                }
            }
        }
