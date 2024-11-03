from flask import Flask, jsonify, request
from llm import agent_factory


app = Flask(__name__)
example_agent = agent_factory.create_test_agent()

@app.route('/')
def home():
    return "Welcome to the Panwshop API."

@app.route("/api/chat")
def inference():
    message = request.args.get("message")
    res = example_agent.generate_chat(message)
    return res

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

