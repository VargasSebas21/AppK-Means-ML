from flask import Flask
from flask_cors import CORS

import os


class FlaskInstance:
    __instance = None
    __app = Flask(__name__, template_folder='static')
    __port = int(float(os.environ.get("PORT", 5000)))
    __prefix = ""

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = object.__new__(cls)
        return cls.__instance

    @property
    def __get_instance__(self):
        if self.__instance is None:
            self.__instance = object.__new__(self)
        return self.__instance

    @property
    def get_app(self) -> Flask:
        """
        Return the flask app instance
        """
        return self.__app

    def set_prefix(self, prefix=""):
        self.__prefix = prefix
        if self.__prefix != "" and self.__prefix[len(self.__prefix) - 1] != "/":
            self.__prefix += "/"

    def run(self):
        """
        Starts the flask server. Use the environment variable HOST and PORT to bind an specific host and port.
        Default is 127.0.0.1:5000
        @environment HOST: Host to bind the server
        @environment PORT: Port to bind the server
        """
        CORS(app=self.__app)
        if os.environ.get("HOST") is None:
            self.__app.run("0.0.0.0", self.__port)
        else:
            self.__app.run(os.environ.get("HOST"), self.__port)

    def add_endpoint(self, endpoint=None, endpoint_name=None, handler=None, methods=[]):
        """
        Create a new http endpoint for the services
        @param endpoint: Url to match with the request
        @type endpoint: str
        @param endpoint_name: Internal name to recognize the endpoint in the system
        @type endpoint_name: str
        @param handler: Execution method
        @param methods: HTTP methods can be: "GET", "POST", "PUT", "DELETE" lowercase is allowed
        @type methods: list
        """

        if endpoint[0] == "/":
            endpoint = endpoint[1:]

        methods = [x.upper() for x in methods]
        self.__app.add_url_rule(self.__prefix+endpoint, endpoint_name, handler, None, methods=methods)