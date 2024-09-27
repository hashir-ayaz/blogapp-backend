from flask import Flask

app = Flask(__name__)


@app.route("/")
def home():
    return "<strong>Hello, Flask!</strong>"


if __name__ == "__main__":
    app.run(debug=True)
