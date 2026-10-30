from flask import Flask, jsonify, request

app = Flask(__name__)


def add(a, b):
    return a + b


def multiply(a, b):
    return a * b


@app.route("/")
def home():
    return jsonify(message="SonarQube + Jenkins demo app")


@app.route("/health")
def health():
    return jsonify(status="UP")


@app.route("/add")
def add_route():
    a = int(request.args.get("a", 0))
    b = int(request.args.get("b", 0))
    return jsonify(result=add(a, b))


@app.route("/multiply")
def multiply_route():
    a = int(request.args.get("a", 1))
    b = int(request.args.get("b", 1))
    return jsonify(result=multiply(a, b))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
