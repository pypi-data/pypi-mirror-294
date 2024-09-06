from uuid import uuid4

def generate_idempotency_key(prefix: str) -> str:
    return f"{prefix}-{str(uuid4())}"
