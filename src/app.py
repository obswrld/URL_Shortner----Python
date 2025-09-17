from flask import Flask
from src.controllers.url_controller import url

app = Flask(__name__)
app.register_blueprint(url)


if __name__ == '__main__':
    app.run(debug=True)