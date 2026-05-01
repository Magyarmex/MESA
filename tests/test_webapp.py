import json
from io import BytesIO

from mesa.webapp import MesaRequestHandler


class DummyHandler(MesaRequestHandler):
    def __init__(self):
        pass


def test_prompt_required_validation():
    handler = DummyHandler()
    handler.path = "/api/run"
    payload = json.dumps({"prompt": "   "}).encode("utf-8")
    handler.headers = {"Content-Length": str(len(payload))}
    handler.rfile = BytesIO(payload)
    handler.wfile = BytesIO()

    statuses = {}

    def send_response(code):
        statuses["code"] = code

    handler.send_response = send_response
    handler.send_header = lambda *_: None
    handler.end_headers = lambda: None
    handler.send_error = lambda *_: None

    handler.do_POST()

    assert statuses["code"] == 400
