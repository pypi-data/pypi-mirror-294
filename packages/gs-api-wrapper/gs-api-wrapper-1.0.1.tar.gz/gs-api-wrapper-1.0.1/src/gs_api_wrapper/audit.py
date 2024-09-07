# src/audit.py

class AuditService:
    def __init__(self, client):
        self.client = client

    def get_audit_info(self, eql, field, gso_name="Equity", output_format="JSON"):
        """Fetch audit information."""
        params = {
            "eql": eql,
            "field": field,
            "gsoName": gso_name,
            "format": output_format
        }
        return self.client.get("gso/audit", params=params)


