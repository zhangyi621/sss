from flask import Flask

app = Flask(__name__)


@app.route("/", endpoint="首页")
def index():
    return "首页"


if __name__ == '__main__':
    app.run(host="0.0.0.0",port=8000)
