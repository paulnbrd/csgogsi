from flask import Flask, request
import json
import threading
import logging
import csgogsi.state_parser as state_parser
from dataclasses import fields
from werkzeug.exceptions import HTTPException
import traceback

def disable_log():
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)

def enable_log():
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.DEBUG)

disable_log()

ADDR = "127.0.0.1"
PORT = 3000
TOKEN = "CCWJu64ZV3JHDT8hZc"


if __name__ == "__main__":
    """ If you run this script directly, you can see what CS:GO has sent in 'raw' mode """
    
    app = Flask(__name__)

    last_infos = None
    debug = True

    def setup():

        @app.route("/", methods=["POST"])
        def main_route():
            global last_infos
            last_infos = request.json
            return ""

        if debug:
            @app.route("/get_last", methods=["POST", "GET"])
            def get_route():
                return_value = "Valeur : "
                return_value += json.dumps(last_infos, indent=4)
                return_value += "<br /><br />"
                key_list = list(last_infos.keys())
                for key in key_list:
                    return_value += "<a href=\"/get_key?key="+str(key)+"\" target=\"_BLANK\">"+key+"</a><br />"
                return return_value

            @app.route("/get_key")
            def get_key():
                values = request.args
                return json.dumps(last_infos[str(values["key"])], indent=4)
    setup()
    app.run(debug=False, host=ADDR, port=PORT)

class Server:
    def __init__(self, addr: str = ADDR, port: int = PORT, token: str = TOKEN):
        """
        Create a new csgogsi server
        :param addr: Address to listen to (Default to 127.0.0.1)
        :param port: The port to bind the server to (Default to 3000)
        :param token: The auth token of the gamestate_integration_*.cfg file, can be False if auth verification is not needed (Default is like in examples/gamestate_integration_paulinux.cfg)
        """
        self.host: str = addr
        self.port: int = port
        self.running: bool = False
        self.thread: threading.Thread = None
        self.payload: state_parser.Payload = None
        self.old_payload: state_parser.Payload = None
        self.last_values: dict = None
        self.app: Flask = Flask("CSGOGSI_server")
        self.token: str = token

        self.app.route("/", methods=["POST"])(self.post_request)  # When infos received
        self.app.register_error_handler(Exception, self.handle_exception)

        self.callbacks = {}

        self.disable_on_start_event_triggering: bool = False  # Set it to True before receiving data from CS:GO to disable event triggering at the launch
        self.disable_log: bool = False
        self._first_time: bool = True

    def handle_exception(self, e):
        """ Handle exceptions and print them (disable this by setting self.disable_log) """
        if not self.disable_log:
            traceback.print_exc()
        if isinstance(e, HTTPException):
            return e
        return ""

    @staticmethod
    def copy_payload(payload: state_parser.Payload) -> state_parser.Payload:
        """ Util to duplicate a payload (and watch for changes) """
        new_payload = state_parser.Payload(None, None, None, None, None, None)
        for field in fields(state_parser.Payload):
            setattr(new_payload, field.name, getattr(payload, field.name))
        return new_payload

    def post_request(self):
        """ Handle post requests from CS:GO """
        try:
            if request.json["auth"]["token"] != self.token and self.token != False:
                return "auth_error"
            self.last_values = request.json

            if self.payload is not None:
                self.old_payload = self.copy_payload(self.payload)
            
            self.payload = state_parser.parse_payload(self.last_values)

            if self._first_time is True:
                if self.disable_on_start_event_triggering:
                    self.old_payload = self.copy_payload(self.payload)
                self._first_time = False

            for callback_trigger_elem in self.callbacks.keys():  # Iter through events
                event_triggered = False
                old_value = None
                new_value = None
                
                for call in callback_trigger_elem:
                    try:
                        if old_value is None and new_value is None:
                            old_value = getattr(self.old_payload, call)
                            new_value = getattr(self.payload, call)
                        else:
                            old_value = getattr(old_value, call)
                            new_value = getattr(new_value, call)
                    except:
                        event_triggered = True
                        break
                else:
                    if new_value != old_value:
                        event_triggered = True

                if event_triggered:
                    for callback in self.callbacks[callback_trigger_elem]:
                        callback()

            return ""
        except:
            return ""

    def add_observer(self, *args):
        """ Decorator to watch for payload change """
        def wrapper(func):
            if not args in self.callbacks.keys():
                self.callbacks[args] = []
            self.callbacks[args].append(func)
        return wrapper

    def run(self, blocking: bool = True, daemon: bool = True):
        """
        Start the server with this method
        :param blocking: If the server should be started in a new thread or not (True is no (blocking, not in a thread))
        :param daemon: Useful only is blocking=False, define if the thread should be a daemon, if it is the case, the program will stop even if the thread didn't end at the end of the non-daemon threads (see https://docs.python.org/3/library/threading.html#thread-objects)
        """
        if blocking:
            self.serve()  # Launch server not in a thread
        else:
            #  Launch in a thread so it is not blocking the main thread
            self.thread = threading.Thread(target=self.serve, daemon=daemon)
            self.thread.start()
            return self.thread

    def serve(self):
        """ Run the Flask app """
        self.app.run(debug=False, host=self.host, port=self.port)
