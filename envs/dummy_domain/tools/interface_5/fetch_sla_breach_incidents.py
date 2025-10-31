import json
from typing import Any, Dict, List, Optional, Set
from datetime import datetime, timezone
from tau_bench.envs.tool import Tool

class FetchSlaBreachIncidents(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any], 
        client_id: Optional[str] = None, 
        start_date: Optional[str] = None, 
        end_date: Optional[str] = None, 
        status: Optional[str] = None
    ) -> str:
        """
        Retrieves incidents that have breached their Service Level Agreements (SLAs).
        Checks both response SLA (detection_time to acknowledged_at) and 
        resolution SLA (detection_time to resolved_at/closed_at) breaches.
        
        Incidents are linked to clients through Configuration Items:
        incidents → incident_configuration_items → configuration_items → ci_client_assignments → clients
        """
        
        # SLA Matrix: (business_hours_minutes, 24x7_minutes) for each tier and severity
        # Using max value (24x7) as the SLA target
        SLA_MATRIX = {
            'premium': {
                'P1': {'response': (15, 30), 'resolution': (120, 240)},
                'P2': {'response': (60, 120), 'resolution': (480, 1440)},
                'P3': {'response': (240, 480), 'resolution': (2880, 4320)},
                'P4': {'response': (1440, 2880), 'resolution': (7680, 7680)}
            },
            'standard': {
                'P1': {'response': (60, 120), 'resolution': (480, 1440)},
                'P2': {'response': (240, 480), 'resolution': (1440, 2880)},
                'P3': {'response': (1440, 1440), 'resolution': (4320, 7200)},
                'P4': {'response': (2880, 4320), 'resolution': (10080, 10080)}
            },
            'basic': {
                'P1': {'response': (240, 480), 'resolution': (1440, 2880)},
                'P2': {'response': (1440, 1440), 'resolution': (4320, 7200)},
                'P3': {'response': (2880, 4320), 'resolution': (7200, 14400)},
                'P4': {'response': (7200, 10080), 'resolution': (20160, 20160)}
            }
        }
        
        # Validate data structure
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": "Invalid data format: expected dictionary"
            })
        
        # Validate required tables exist
        required_tables = [
            "incidents", 
            "sla_agreements", 
            "users",
            "incident_configuration_items",
            "ci_client_assignments"
        ]
        missing_tables = [table for table in required_tables if table not in data]
        if missing_tables:
            return json.dumps({
                "success": False,
                "error": f"Missing required data tables: {', '.join(missing_tables)}"
            })
        
        # Validate input parameters
        if status and status not in ['open', 'in_progress', 'monitoring', 'resolved', 'closed']:
            return json.dumps({
                "success": False,
                "error": f"Invalid status '{status}'. Must be one of: open, in_progress, monitoring, resolved, closed"
            })
        
        # Validate and parse date filters
        filter_start_dt = None
        filter_end_dt = None
        
        if start_date:
            try:
                filter_start_dt = datetime.strptime(start_date, '%Y-%m-%d').replace(tzinfo=timezone.utc)
            except ValueError:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid start_date format '{start_date}'. Expected YYYY-MM-DD"
                })
        
        if end_date:
            try:
                # Set to end of day for inclusive range
                filter_end_dt = datetime.strptime(end_date, '%Y-%m-%d').replace(
                    hour=23, minute=59, second=59, microsecond=999999, tzinfo=timezone.utc
                )
            except ValueError:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid end_date format '{end_date}'. Expected YYYY-MM-DD"
                })
        
        # Validate date range logic
        if filter_start_dt and filter_end_dt and filter_start_dt > filter_end_dt:
            return json.dumps({
                "success": False,
                "error": "start_date must be less than or equal to end_date"
            })
        
        # Load data tables
        incidents_data = data.get("incidents", {})
        sla_agreements_data = data.get("sla_agreements", {})
        users_data = data.get("users", {})
        incident_cis_data = data.get("incident_configuration_items", {})
        ci_assignments_data = data.get("ci_client_assignments", {})
        
        # Build client_id to active SLA mapping for efficient lookup
        client_sla_map = {}
        for sla_id, sla_agreement in sla_agreements_data.items():
            if sla_agreement.get("status") == "active":
                sla_client_id = sla_agreement.get("client_id")
                if sla_client_id:
                    if sla_client_id in client_sla_map:
                        # Data integrity issue: multiple active SLAs for same client
                        # Per policy (SOP 1.3), this shouldn't happen
                        # Keep the first one found
                        pass
                    else:
                        client_sla_map[sla_client_id] = sla_agreement
        
        breach_incidents = []
        
        # Helper function to parse ISO datetime with timezone handling
        def parse_datetime(dt_str: Optional[str]) -> Optional[datetime]:
            if not dt_str:
                return None
            try:
                # Handle 'Z' UTC indicator
                if dt_str.endswith('Z'):
                    dt_str = dt_str[:-1] + '+00:00'
                dt = datetime.fromisoformat(dt_str)
                # Ensure timezone aware
                if dt.tzinfo is None:
                    dt = dt.replace(tzinfo=timezone.utc)
                return dt
            except (ValueError, AttributeError):
                return None
        
        # Helper function to get all client IDs affected by an incident
        # Uses the proper relationship chain: incident → incident_cis → ci_assignments → clients
        def get_incident_client_ids(incident_id: str) -> Set[str]:
            """
            Get all client IDs affected by this incident through CI assignments.
            Relationship: incidents → incident_configuration_items → ci_client_assignments → clients
            """
            client_ids = set()
            
            # Find all CIs linked to this incident
            incident_ci_ids = set()
            for ici_id, ici in incident_cis_data.items():
                if ici.get("incident_id") == incident_id:
                    ci_id = ici.get("ci_id")
                    if ci_id:
                        incident_ci_ids.add(ci_id)
            
            # Find all clients assigned to these CIs
            for assignment_id, assignment in ci_assignments_data.items():
                if assignment.get("ci_id") in incident_ci_ids:
                    client_id_value = assignment.get("client_id")
                    if client_id_value:
                        client_ids.add(client_id_value)
            
            return client_ids
        
        # Process each incident
        for incident_id, incident in incidents_data.items():
            # Apply status filter first (most selective)
            if status and incident.get("status") != status:
                continue
            
            # Get detection time (required field in DB schema)
            detection_time_str = incident.get("detection_time")
            if not detection_time_str:
                continue  # Skip incidents without detection_time
            
            incident_detection_dt = parse_datetime(detection_time_str)
            if not incident_detection_dt:
                continue  # Skip invalid datetime format
            
            # Apply time range filter based on detection_time
            if filter_start_dt and incident_detection_dt < filter_start_dt:
                continue
            if filter_end_dt and incident_detection_dt > filter_end_dt:
                continue
            
            # Get all client IDs affected by this incident through CI assignments
            incident_client_ids = get_incident_client_ids(incident_id)
            if not incident_client_ids:
                continue  # Skip incidents with no client assignments
            
            # Apply client_id filter if provided
            if client_id:
                if client_id not in incident_client_ids:
                    continue  # This incident doesn't affect the requested client
            
            # Get incident severity
            incident_severity = incident.get("severity")
            if not incident_severity:
                continue
            
            # Process SLA breach for each affected client
            for incident_client_id in incident_client_ids:
                # Find the SLA agreement for this client
                client_sla = client_sla_map.get(incident_client_id)
                if not client_sla:
                    continue  # No active SLA for this client
                
                client_tier = client_sla.get("tier")
                if not client_tier or client_tier not in SLA_MATRIX:
                    continue
                
                sla_config = SLA_MATRIX[client_tier].get(incident_severity)
                if not sla_config:
                    continue
                
                # Get SLA targets (using max value from range - assumes 24x7 coverage)
                expected_response_minutes = sla_config['response'][1]
                expected_resolution_minutes = sla_config['resolution'][1]
                
                # Check for Response SLA breach (detection_time to acknowledged_at)
                response_breach = False
                actual_response_minutes = None
                acknowledged_at_str = incident.get("acknowledged_at")
                
                if acknowledged_at_str:
                    acknowledged_at_dt = parse_datetime(acknowledged_at_str)
                    if acknowledged_at_dt:
                        actual_response_minutes = (acknowledged_at_dt - incident_detection_dt).total_seconds() / 60
                        if actual_response_minutes > expected_response_minutes:
                            response_breach = True
                
                # Check for Resolution SLA breach (detection_time to resolved_at/closed_at)
                resolution_breach = False
                actual_resolution_minutes = None
                resolved_at_str = incident.get("resolved_at") or incident.get("closed_at")
                
                if resolved_at_str:
                    resolved_at_dt = parse_datetime(resolved_at_str)
                    if resolved_at_dt:
                        actual_resolution_minutes = (resolved_at_dt - incident_detection_dt).total_seconds() / 60
                        if actual_resolution_minutes > expected_resolution_minutes:
                            resolution_breach = True
                
                # If either SLA is breached, add to results
                if response_breach or resolution_breach:
                    incident_copy = incident.copy()
                    incident_copy["incident_id"] = incident_id
                    incident_copy["client_id"] = incident_client_id
                    incident_copy["sla_tier"] = client_tier
                    incident_copy["sla_id"] = client_sla.get("sla_id") if isinstance(client_sla, dict) else None
                    
                    # Response SLA metrics
                    if response_breach:
                        incident_copy["response_sla_breach"] = True
                        incident_copy["expected_response_minutes"] = expected_response_minutes
                        incident_copy["actual_response_minutes"] = round(actual_response_minutes, 2)
                        incident_copy["response_breach_by_minutes"] = round(actual_response_minutes - expected_response_minutes, 2)
                    else:
                        incident_copy["response_sla_breach"] = False
                    
                    # Resolution SLA metrics
                    if resolution_breach:
                        incident_copy["resolution_sla_breach"] = True
                        incident_copy["expected_resolution_minutes"] = expected_resolution_minutes
                        incident_copy["actual_resolution_minutes"] = round(actual_resolution_minutes, 2)
                        incident_copy["resolution_breach_by_minutes"] = round(actual_resolution_minutes - expected_resolution_minutes, 2)
                    else:
                        incident_copy["resolution_sla_breach"] = False
                    
                    breach_incidents.append(incident_copy)
        
        return json.dumps({
            "success": True,
            "count": len(breach_incidents),
            "breach_incidents": breach_incidents
        }, indent=2)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "fetch_sla_breach_incidents",
                "description": "Retrieves incidents that have breached their Service Level Agreements (SLAs). Checks both response SLA (acknowledgment time) and resolution SLA (resolution time) breaches. Incidents are linked to clients through Configuration Items: incidents are associated with CIs via incident_configuration_items, and CIs are assigned to clients via ci_client_assignments.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "client_id": {
                            "type": "string",
                            "description": "Optional: Filter incidents by a specific client ID. Only incidents affecting this client (through CI assignments) will be included."
                        },
                        "start_date": {
                            "type": "string",
                            "description": "Optional: Start date for the time range filter based on incident detection_time (YYYY-MM-DD format). Inclusive."
                        },
                        "end_date": {
                            "type": "string",
                            "description": "Optional: End date for the time range filter based on incident detection_time (YYYY-MM-DD format). Inclusive, includes full day until 23:59:59."
                        },
                        "status": {
                            "type": "string",
                            "description": "Optional: Filter incidents by current status. Must be one of: open, in_progress, monitoring, resolved, closed."
                        }
                    },
                    "required": []
                }
            }
        }