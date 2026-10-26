from __future__ import annotations

from typing import Any
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.services.connectors.approval_gate import approval_gate
from app.services.connectors.models import (
    ActionResult,
    ConnectorManifest,
    ConnectorStatus,
    PreparedAction,
)
from app.services.connectors.registry import connector_registry

router = APIRouter()


class PrepareActionRequest(BaseModel):
    action_id: str
    case_id: str
    payload: dict[str, Any]
    execution_mode: str = "sandbox"


class HumanApprovalRequest(BaseModel):
    prepared_action: PreparedAction
    user_id: str
    consent_statement: str


class ExecuteActionRequest(BaseModel):
    prepared_action: PreparedAction
    idempotency_key: str
    approval_token: str | None = None


@router.get("", response_model=list[ConnectorManifest])
async def list_connectors() -> list[ConnectorManifest]:
    """Discover all registered RECLAIM Action Fabric connectors and capabilities."""
    return connector_registry.list_manifests()


@router.get("/health", response_model=list[ConnectorStatus])
async def check_all_connectors_health() -> list[ConnectorStatus]:
    """Probe connectivity, latency, and sandbox readiness across all connectors."""
    return connector_registry.healthcheck_all()


@router.get("/{connector_id}", response_model=ConnectorManifest)
async def get_connector_manifest(connector_id: str) -> ConnectorManifest:
    """Introspect specific connector capabilities and parameters."""
    try:
        conn = connector_registry.get(connector_id)
        return conn.describe_capabilities()
    except KeyError:
        raise HTTPException(status_code=404, detail=f"Connector '{connector_id}' not found")


@router.post("/{connector_id}/prepare", response_model=PreparedAction)
async def prepare_connector_action(connector_id: str, req: PrepareActionRequest) -> PreparedAction:
    """Formulate an action, determine if human approval is required, and estimate consequences."""
    try:
        return connector_registry.prepare(
            connector_id=connector_id,
            action_id=req.action_id,
            payload=req.payload,
            case_id=req.case_id,
            execution_mode=req.execution_mode,
        )
    except KeyError:
        raise HTTPException(status_code=404, detail=f"Connector '{connector_id}' not found")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/approve")
async def approve_action_manually(req: HumanApprovalRequest) -> dict[str, Any]:
    """Human approval gate: grant explicit user consent and generate an unforgeable approval token."""
    token = approval_gate.issue_approval(
        prepared_action=req.prepared_action,
        user_id=req.user_id,
        consent_statement=req.consent_statement,
    )
    return {
        "status": "APPROVED",
        "approval_token": token,
        "prepared_action_id": req.prepared_action.prepared_action_id,
        "approved_by": req.user_id,
    }


@router.post("/{connector_id}/execute", response_model=ActionResult)
async def execute_connector_action(connector_id: str, req: ExecuteActionRequest) -> ActionResult:
    """Execute prepared action. Blocks if required human approval token is missing or invalid."""
    try:
        return connector_registry.execute(
            connector_id=connector_id,
            prepared_action=req.prepared_action,
            idempotency_key=req.idempotency_key,
            approval_token=req.approval_token,
        )
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except KeyError:
        raise HTTPException(status_code=404, detail=f"Connector '{connector_id}' not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Connector execution error: {str(e)}")


@router.get("/{connector_id}/operations/{operation_id}", response_model=ActionResult)
async def get_operation_status(connector_id: str, operation_id: str) -> ActionResult:
    """Check live status of an asynchronous connector operation."""
    try:
        return connector_registry.check_status(connector_id, operation_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="Operation record not found")


@router.get("/{connector_id}/operations/{operation_id}/reconcile")
async def reconcile_operation(connector_id: str, operation_id: str) -> dict[str, Any]:
    """Reconcile action result against carrier/provider status."""
    try:
        return connector_registry.reconcile(connector_id, operation_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="Operation record not found")


@router.get("/cases/{case_id}/operations", response_model=list[ActionResult])
async def list_case_operations(case_id: str) -> list[ActionResult]:
    """Retrieve all executed connector operations for a specific case."""
    return connector_registry.list_case_operations(case_id)

