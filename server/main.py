from flask import Flask, jsonify, request
from llm import agent_factory
from llm import tool_store


app = Flask(__name__)
example_agent = agent_factory.create_test_agent()


@app.route('/')
def home():
    return "Welcome to the Panwshop API."


@app.route("/api/chat", methods=["POST"])
def inference():
    payload = request.get_json(force=True)
    message = payload.get("message")
    
    # Single-session assumption; no session management required.
    res = example_agent.generate_chat(message)

    # If the agent returned a tool_call notification dict, forward as JSON.
    if isinstance(res, dict) and res.get("status") == "tool_call":
        return jsonify(res), 202

    # Otherwise return finished reply
    return jsonify({"status": "finished", "reply": res})


@app.route("/api/tool_result", methods=["POST"])
def tool_result():
    payload = request.get_json(force=True)
    tool_call_id = payload.get("tool_call_id")
    result = payload.get("result")

    if not tool_call_id:
        return jsonify({"error": "missing tool_call_id"}), 400

    pending = tool_store.get_pending_call(tool_call_id)
    if not pending:
        return jsonify({"error": "unknown or expired tool_call_id"}), 404

    # store the result and resume the agent loop
    tool_store.set_pending_result(tool_call_id, result)

    reply = example_agent.resume_with_tool_result(tool_call_id=tool_call_id, result=result)

    return jsonify({"status": "finished", "reply": reply})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

