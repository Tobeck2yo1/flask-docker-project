from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/")
def home():
    return """
    <h1>Flask Docker Application</h1>
    <p>The application is running successfully inside a Docker container.</p>
    """


@app.route("/health")
def health():
    return jsonify(
        status="healthy",
        message="Flask application is running"
    ), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
