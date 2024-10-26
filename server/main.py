from flask import Flask, jsonify, request
from llm.agent import LLMAgent


app = Flask(__name__)
llm = LLMAgent()


@app.route('/')
def hello_world():
    return "Hello World!"


@app.route("/chat")
def inference():
    message = request.args.get("message")
    res = llm.generate_chat(message)
    return res


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
