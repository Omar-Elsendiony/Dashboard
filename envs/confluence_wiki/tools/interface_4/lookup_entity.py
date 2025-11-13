import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool


class LookupEntity(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        entity_type: str,
        entity_id: Optional[str] = None,
        filters: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Get entities by type with optional filters.
        - entity_type is required.
        - entity_id is optional; when provided, it is ANDed with filters.
        - When entity_id is omitted, returns all entries that match filters.

        Supported entity_type and ID fields:
        - label: page_label_id
        - attachment: attachment_id
        - database: database_id
        - smart_link: smart_link_id
        - whiteboard: whiteboard_id
        """
        entity_type = str(entity_type)
        entity_id = None if entity_id is None else str(entity_id)

        pages = data.get("pages", {})
        users = data.get("users", {})
        spaces = data.get("spaces", {})
        attachments = data.get("attachments", {})
        databases = data.get("databases", {})
        smart_links = data.get("smart_links", {})
        page_labels = data.get("page_labels", {})
        whiteboards = data.get("whiteboards", {})

        allowed_types = {"label", "attachment",
                         "database", "smart_link", "whiteboard"}
        if entity_type not in allowed_types:
            return json.dumps(
                {
                    "success": False,
                    "error": f"Invalid entity_type: '{entity_type}'. Must be one of {sorted(list(allowed_types))}",
                }
            )

        # Normalize filters
        filters = filters or {}
        filters = {k: v for k, v in filters.items() if v is not None}

        def finish(
            collection: Dict[str, Any],
            id_field: str,
            allowed: set[str],
            validate_cb=None,
        ):
            # entity_id existence check, if provided
            if entity_id is not None and entity_id not in collection:
                return json.dumps(
                    {
                        "success": False,
                        "error": f"{entity_type.replace('_', ' ').title()} not found: '{entity_id}'",
                    }
                )

            # unsupported filter keys
            unexpected = [k for k in filters if k not in allowed]
            if unexpected:
                return json.dumps(
                    {
                        "success": False,
                        "error": f"Unsupported filter(s) for {entity_type}: {', '.join(unexpected)}",
                    }
                )

            # custom validations (enums, referential)
            if validate_cb:
                err = validate_cb(filters)
                if err is not None:
                    return json.dumps({"success": False, "error": err})

            # Build criteria and filter
            criteria = dict(filters)
            if entity_id is not None:
                criteria[id_field] = entity_id
            entities = [
                e
                for e in collection.values()
                if all(str(e.get(k)) == str(v) for k, v in criteria.items())
            ]

            return json.dumps(
                {
                    "success": True,
                    "entity_type": entity_type,
                    "entity_id": entity_id,
                    "count": len(entities),
                    "entities": entities,
                }
            )

        if entity_type == "label":

            def _validate(f: Dict[str, Any]) -> Optional[str]:
                if "page_id" in f and str(f["page_id"]) not in pages:
                    return f"Invalid page_id: '{f['page_id']}'"
                if "added_by" in f and str(f["added_by"]) not in users:
                    return f"Invalid added_by user_id: '{f['added_by']}'"
                return None

            return finish(
                page_labels,
                id_field="page_label_id",
                allowed={"label_name", "page_id", "added_by"},
                validate_cb=_validate,
            )

        if entity_type == "attachment":

            def _validate(f: Dict[str, Any]) -> Optional[str]:
                if "content_type" in f and str(f["content_type"]) not in {
                    "page",
                    "database",
                    "whiteboard",
                    "smart_link",
                }:
                    return f"Invalid content_type: '{f['content_type']}'"
                if "status" in f and str(f["status"]) not in {
                    "current",
                    "archived",
                    "deleted",
                }:
                    return f"Invalid status: '{f['status']}'"
                if "uploaded_by" in f and str(f["uploaded_by"]) not in users:
                    return f"Invalid uploaded_by user_id: '{f['uploaded_by']}'"
                if "content_id" in f:
                    cid = str(f["content_id"])
                    ctype = str(f.get("content_type")
                                ) if "content_type" in f else None
                    if ctype == "page" and cid not in pages:
                        return f"content_id '{cid}' not a valid page"
                    if ctype == "database" and cid not in databases:
                        return f"content_id '{cid}' not a valid database"
                    if ctype == "whiteboard" and cid not in whiteboards:
                        return f"content_id '{cid}' not a valid whiteboard"
                    if ctype == "smart_link" and cid not in smart_links:
                        return f"content_id '{cid}' not a valid smart_link"
                    if ctype is None and (
                        cid not in pages
                        and cid not in databases
                        and cid not in whiteboards
                        and cid not in smart_links
                    ):
                        return f"content_id '{cid}' does not exist in any content set"
                if "host_page_id" in f and str(f["host_page_id"]) not in pages:
                    return f"Invalid host_page_id: '{f['host_page_id']}'"
                return None

            return finish(
                attachments,
                id_field="attachment_id",
                allowed={
                    "content_type",
                    "content_id",
                    "host_page_id",
                    "file_name",
                    "status",
                    "uploaded_by",
                },
                validate_cb=_validate,
            )

        if entity_type == "database":

            def _validate(f: Dict[str, Any]) -> Optional[str]:
                if "status" in f and str(f["status"]) not in {
                    "current",
                    "archived",
                    "deleted",
                }:
                    return f"Invalid status: '{f['status']}'"
                if "host_space_id" in f and str(f["host_space_id"]) not in spaces:
                    return f"Invalid host_space_id: '{f['host_space_id']}'"
                if "host_page_id" in f and str(f["host_page_id"]) not in pages:
                    return f"Invalid host_page_id: '{f['host_page_id']}'"
                return None

            return finish(
                databases,
                id_field="database_id",
                allowed={"title", "status", "host_space_id", "host_page_id"},
                validate_cb=_validate,
            )

        if entity_type == "smart_link":

            def _validate(f: Dict[str, Any]) -> Optional[str]:
                if "target_type" in f and str(f["target_type"]) not in {
                    "page",
                    "database",
                    "whiteboard",
                    "external",
                }:
                    return f"Invalid target_type: '{f['target_type']}'"
                # Validate host_page_id refers to an existing page
                if "host_page_id" in f and str(f["host_page_id"]) not in pages:
                    return f"Invalid host_page_id: '{f['host_page_id']}'"
                if "target_id" in f:
                    tid = str(f["target_id"])
                    ttype = str(f.get("target_type")
                                ) if "target_type" in f else None
                    if ttype == "page" and tid not in pages:
                        return f"target_id '{tid}' not a valid page"
                    if ttype == "database" and tid not in databases:
                        return f"target_id '{tid}' not a valid database"
                    if ttype == "whiteboard" and tid not in whiteboards:
                        return f"target_id '{tid}' not a valid whiteboard"
                return None

            return finish(
                smart_links,
                id_field="smart_link_id",
                allowed={
                    "title",
                    "url",
                    "target_id",
                    "target_type",
                    "host_page_id",
                },
                validate_cb=_validate,
            )

        if entity_type == "whiteboard":

            def _validate(f: Dict[str, Any]) -> Optional[str]:
                if "status" in f and str(f["status"]) not in {
                    "current",
                    "archived",
                    "deleted",
                }:
                    return f"Invalid status: '{f['status']}'"
                if "host_space_id" in f and str(f["host_space_id"]) not in spaces:
                    return f"Invalid host_space_id: '{f['host_space_id']}'"
                if "host_page_id" in f and str(f["host_page_id"]) not in pages:
                    return f"Invalid host_page_id: '{f['host_page_id']}'"
                return None

            return finish(
                whiteboards,
                id_field="whiteboard_id",
                allowed={"title", "status", "host_space_id", "host_page_id"},
                validate_cb=_validate,
            )

        # Fallback empty (shouldn't hit)
        return json.dumps(
            {
                "success": True,
                "entity_type": entity_type,
                "entity_id": entity_id,
                "count": 0,
                "entities": [],
            }
        )

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "lookup_entity",
                "description": (
                    "Get entities by type with optional filters. If entity_id is provided, it is ANDed with filters; "
                    "otherwise returns all matching entries. Supported types: label, attachment, database, smart_link, whiteboard."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "entity_type": {
                            "type": "string",
                            "description": "One of: label, attachment, database, smart_link, whiteboard",
                        },
                        "entity_id": {
                            "type": ["string", "null"],
                            "description": "Optional primary identifier for the entity type",
                        },
                        "filters": {
                            "type": "object",
                            "description": "Optional type-specific filters applied with AND",
                            "additionalProperties": True,
                        },
                    },
                    "required": ["entity_type"],
                },
            },
        }
