import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class SetExports(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], action: str, space_id: Optional[str] = None,
               requested_by_user_id: Optional[str] = None, export_format: Optional[str] = None,
               destination: Optional[str] = None, estimated_size_kb: Optional[int] = None,
               priority: Optional[int] = None, job_id: Optional[str] = None,
               status: Optional[str] = None) -> str:
        """
        Create or manage export jobs.
        
        Actions:
        - create: Create new export job (requires space_id, requested_by_user_id, export_format)
        - update: Update export job status (requires job_id, status)
        """
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        if action not in ["create", "update"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid action '{action}'. Must be 'create' or 'update'"
            })
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": "Invalid data format"
            })
        
        export_jobs = data.get("export_jobs", {})
        spaces = data.get("spaces", {})
        users = data.get("users", {})
        
        if action == "create":
            # Validate required fields
            if not space_id:
                return json.dumps({
                    "success": False,
                    "error": "space_id is required for create action"
                })
            
            if not requested_by_user_id:
                return json.dumps({
                    "success": False,
                    "error": "requested_by_user_id is required for create action"
                })
            
            if not export_format:
                return json.dumps({
                    "success": False,
                    "error": "export_format is required for create action"
                })
            
            # Validate space exists
            if space_id not in spaces:
                return json.dumps({
                    "success": False,
                    "error": f"Space {space_id} not found"
                })
            
            # Validate user exists
            if requested_by_user_id not in users:
                return json.dumps({
                    "success": False,
                    "error": f"User {requested_by_user_id} not found"
                })
            
            # Validate export_format enum
            valid_formats = ["PDF", "HTML", "XML"]
            if export_format not in valid_formats:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid export_format. Must be one of: {', '.join(valid_formats)}"
                })
            
            # Generate new job ID
            new_job_id = generate_id(export_jobs)
            timestamp = "2025-10-01T12:00:00"
            
            new_job = {
                "job_id": str(new_job_id),
                "space_id": space_id,
                "requested_by_user_id": requested_by_user_id,
                "requested_at": timestamp,
                "status": "pending",
                "format": export_format,
                "destination": destination,
                "estimated_size_kb": estimated_size_kb,
                "priority": priority if priority is not None else 0
            }
            
            export_jobs[str(new_job_id)] = new_job
            
            return json.dumps({
                "success": True,
                "action": "create",
                "job_id": str(new_job_id),
                "message": f"Export job created for space {space_id} in {export_format} format",
                "job_data": new_job
            })
        
        elif action == "update":
            if not job_id:
                return json.dumps({
                    "success": False,
                    "error": "job_id is required for update action"
                })
            
            if job_id not in export_jobs:
                return json.dumps({
                    "success": False,
                    "error": f"Export job {job_id} not found"
                })
            
            if not status:
                return json.dumps({
                    "success": False,
                    "error": "status is required for update action"
                })
            
            # Validate status enum
            valid_statuses = ["pending", "running", "completed", "failed", "cancelled"]
            if status not in valid_statuses:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
                })
            
            # Update job status
            updated_job = export_jobs[job_id].copy()
            updated_job["status"] = status
            
            export_jobs[job_id] = updated_job
            
            return json.dumps({
                "success": True,
                "action": "update",
                "job_id": job_id,
                "message": f"Export job {job_id} status updated to {status}",
                "job_data": updated_job
            })
    
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "set_exports",
                "description": "Create or manage export jobs in the Confluence system. This tool handles space and page export operations by creating export job requests in various formats (PDF, HTML, XML) or updating existing job statuses. Validates space existence, user authorization, and export format specifications. Supports optional destination paths, size estimates, and priority settings for job queue management. Essential for content backup, data migration, offline access, and content distribution.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "description": "Action to perform: 'create' to queue new export job, 'update' to modify job status",
                            "enum": ["create", "update"]
                        },
                        "space_id": {
                            "type": "string",
                            "description": "Unique identifier of the space to export (required for create action)"
                        },
                        "requested_by_user_id": {
                            "type": "string",
                            "description": "User ID requesting the export (required for create action)"
                        },
                        "export_format": {
                            "type": "string",
                            "description": "Export format (required for create action)",
                            "enum": ["PDF", "HTML", "XML"]
                        },
                        "destination": {
                            "type": "string",
                            "description": "Destination path for exported file (optional)"
                        },
                        "estimated_size_kb": {
                            "type": "integer",
                            "description": "Estimated export size in KB (optional)"
                        },
                        "priority": {
                            "type": "integer",
                            "description": "Job priority for queue management (optional, default 0)"
                        },
                        "job_id": {
                            "type": "string",
                            "description": "ID of export job to update (required for update action)"
                        },
                        "status": {
                            "type": "string",
                            "description": "New job status (required for update action)",
                            "enum": ["pending", "running", "completed", "failed", "cancelled"]
                        }
                    },
                    "required": ["action"]
                }
            }
        }
