from flask import Flask, jsonify, request
from llm.inference import LLM


app = Flask(__name__)
llm = LLM()

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route("/api/infer")
def inference():
    prompt = request.args.get("prompt")
    print(f"Prompt submitted: {prompt}")
    res = llm.infer(prompt)
    return res

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
