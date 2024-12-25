"""
Simple in-memory thread-safe store for pending tool calls.

Assumes a single active session; entries are keyed only by tool_call_id.
"""
import threading
import time

_pending = {}
_lock = threading.Lock()

PENDING_TTL_SECONDS = 300


def create_pending_call(tool_call_id, name, args):
    # Use the provided tool_call_id directly; assume uniqueness from the LLM.
    call_id = str(tool_call_id)
    now = time.time()
    entry = {
        "id": call_id,
        "name": name,
        "args": args,
        "created_at": now,
        "result": None,
    }
    with _lock:
        _pending[call_id] = entry
    return entry

def get_pending_call(call_id):
    with _lock:
        entry = _pending.get(call_id)
        if not entry:
            return None
        # check TTL
        if time.time() - entry["created_at"] > PENDING_TTL_SECONDS:
            # expire
            del _pending[call_id]
            return None
        return entry

def set_pending_result(call_id, result):
    with _lock:
        entry = _pending.get(call_id)
        if not entry:
            return False
        entry["result"] = result
        # keep entry for a short while; caller will remove if needed
        return True

def pop_pending_call(call_id):
    with _lock:
        return _pending.pop(call_id, None)
