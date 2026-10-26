from __future__ import annotations

import hashlib
import hmac
import json
import secrets
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from app.services.connectors.models import ApprovalState, PreparedAction

SECRET_SALT = "reclaim_action_fabric_secure_gate_salt_2026"
TOKEN_EXPIRY_SECONDS = 86400  # 24 hours


class ActionApprovalGate:
    """Explicit human approval checkpoint for consequential real-world actions.

    Backed by durable JSONL persistence so approval records survive restarts.
    """

    def __init__(self, storage_dir: Path | None = None):
        self.storage_dir = storage_dir or Path("datasets") / "app_store"
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self.tokens_file = self.storage_dir / "action_approvals.jsonl"
        self.audit_file = self.storage_dir / "action_audit_log.jsonl"
        self._approved_tokens: dict[str, dict[str, Any]] = {}
        self._audit_log: list[dict[str, Any]] = []
        self._load_from_disk()

    def _load_from_disk(self) -> None:
        """Hydrate tokens and audit log from disk on startup."""
        if self.tokens_file.exists():
            with self.tokens_file.open("r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        try:
                            record = json.loads(line)
                            token = record.get("token")
                            if token:
                                self._approved_tokens[token] = record
                        except json.JSONDecodeError:
                            continue

        if self.audit_file.exists():
            with self.audit_file.open("r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        try:
                            self._audit_log.append(json.loads(line))
                        except json.JSONDecodeError:
                            continue

    def _save_token(self, token: str, record: dict[str, Any]) -> None:
        """Durable append/update of approval token."""
        self._approved_tokens[token] = record
        # Rewrite tokens file to reflect updated 'used' state safely
        with self.tokens_file.open("w", encoding="utf-8") as f:
            for rec in self._approved_tokens.values():
                f.write(json.dumps(rec, default=str) + "\n")

    def _append_audit(self, event: dict[str, Any]) -> None:
        """Append event to audit log file."""
        self._audit_log.append(event)
        with self.audit_file.open("a", encoding="utf-8") as f:
            f.write(json.dumps(event, default=str) + "\n")

    def request_approval(self, prepared_action: PreparedAction) -> PreparedAction:
        """Mark action as awaiting explicit approval."""
        if not prepared_action.requires_human_approval:
            prepared_action.approval_state = ApprovalState.NOT_REQUIRED
            return prepared_action

        prepared_action.approval_state = ApprovalState.PENDING_APPROVAL
        return prepared_action

    def issue_approval(
        self,
        prepared_action: PreparedAction,
        user_id: str,
        consent_statement: str,
    ) -> str:
        """Record explicit user approval and generate an unforgeable verification token."""
        raw_key = (
            f"{prepared_action.prepared_action_id}:{prepared_action.case_id}:"
            f"{prepared_action.connector_id}:{prepared_action.action_id}:{user_id}:"
            f"{time.time()}:{secrets.token_hex(8)}"
        )
        token = hmac.new(SECRET_SALT.encode(), raw_key.encode(), hashlib.sha256).hexdigest()

        now = datetime.now(timezone.utc).isoformat()
        record = {
            "token": token,
            "prepared_action_id": prepared_action.prepared_action_id,
            "case_id": prepared_action.case_id,
            "connector_id": prepared_action.connector_id,
            "action_id": prepared_action.action_id,
            "user_id": user_id,
            "consent_statement": consent_statement,
            "approved_at": now,
            "timestamp": time.time(),
            "used": False,
        }

        self._save_token(token, record)
        self._append_audit({
            "event": "HUMAN_APPROVAL_GRANTED",
            "token": token[:12] + "...",
            "prepared_action_id": prepared_action.prepared_action_id,
            "case_id": prepared_action.case_id,
            "action_id": prepared_action.action_id,
            "user_id": user_id,
            "timestamp": now,
        })

        prepared_action.approval_state = ApprovalState.APPROVED
        prepared_action.approval_token = token
        return token

    def verify_approval(self, prepared_action: PreparedAction, token: str | None) -> tuple[bool, str | None]:
        """Validate token before execution is permitted."""
        if not prepared_action.requires_human_approval:
            return True, None

        if not token:
            return False, "Action requires explicit human approval token before execution"

        record = self._approved_tokens.get(token)
        if not record:
            return False, "Invalid or unrecognized approval token"

        if record.get("used"):
            return False, "Approval token has already been consumed (idempotency enforcement)"

        # Check expiry
        issued_at = record.get("timestamp", 0)
        if time.time() - issued_at > TOKEN_EXPIRY_SECONDS:
            return False, "Approval token has expired"

        # Cryptographic and context binding checks
        if record.get("prepared_action_id") != prepared_action.prepared_action_id:
            return False, "Approval token mismatch for this prepared action ID"

        if record.get("action_id") != prepared_action.action_id:
            return False, "Approval token mismatch for this action type"

        if record.get("connector_id") != prepared_action.connector_id:
            return False, "Approval token mismatch for this connector"

        return True, None

    def mark_consumed(self, token: str) -> None:
        """Mark token as consumed to prevent replay attacks and persist to disk."""
        if token in self._approved_tokens:
            self._approved_tokens[token]["used"] = True
            self._save_token(token, self._approved_tokens[token])
            self._append_audit({
                "event": "APPROVAL_TOKEN_CONSUMED",
                "token": token[:12] + "...",
                "consumed_at": datetime.now(timezone.utc).isoformat(),
            })

    def get_audit_trail(self, case_id: str | None = None) -> list[dict[str, Any]]:
        if case_id:
            return [e for e in self._audit_log if e.get("case_id") == case_id]
        return list(self._audit_log)


approval_gate = ActionApprovalGate()
