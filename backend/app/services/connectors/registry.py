from __future__ import annotations

from typing import Any

from app.services.connectors.aviation_refund import AviationRefundConnector
from app.services.connectors.base import BaseConnector
from app.services.connectors.email_delivery import EmailComplaintConnector
from app.services.connectors.models import (
    ActionResult,
    ConnectorManifest,
    ConnectorStatus,
    PreparedAction,
)
from app.services.connectors.storage import list_operations_for_case


class ConnectorRegistry:
    """Central registry and lifecycle orchestrator for the RECLAIM Action Fabric."""

    def __init__(self):
        self._connectors: dict[str, BaseConnector] = {}
        # Register default Action Fabric connectors
        self.register(AviationRefundConnector())
        self.register(EmailComplaintConnector())


    def register(self, connector: BaseConnector) -> None:
        manifest = connector.describe_capabilities()
        self._connectors[manifest.connector_id] = connector

    def get(self, connector_id: str) -> BaseConnector:
        connector = self._connectors.get(connector_id)
        if not connector:
            raise KeyError(f"Connector '{connector_id}' is not registered in RECLAIM Action Fabric")
        return connector

    def list_manifests(self) -> list[ConnectorManifest]:
        return [c.describe_capabilities() for c in self._connectors.values()]

    def healthcheck_all(self) -> list[ConnectorStatus]:
        return [c.healthcheck() for c in self._connectors.values()]

    def prepare(
        self,
        connector_id: str,
        action_id: str,
        payload: dict[str, Any],
        case_id: str,
        execution_mode: str = "sandbox",
    ) -> PreparedAction:
        connector = self.get(connector_id)
        return connector.prepare_action(action_id, payload, case_id, execution_mode)

    def execute(
        self,
        connector_id: str,
        prepared_action: PreparedAction,
        idempotency_key: str,
        approval_token: str | None = None,
    ) -> ActionResult:
        connector = self.get(connector_id)
        return connector.execute_action(prepared_action, idempotency_key, approval_token)

    def check_status(self, connector_id: str, operation_id: str) -> ActionResult:
        connector = self.get(connector_id)
        return connector.check_status(operation_id)

    def reconcile(self, connector_id: str, operation_id: str) -> dict[str, Any]:
        connector = self.get(connector_id)
        return connector.reconcile_result(operation_id)

    def list_case_operations(self, case_id: str) -> list[ActionResult]:
        return list_operations_for_case(case_id)


# Global singleton registry instance
connector_registry = ConnectorRegistry()

