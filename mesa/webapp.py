from __future__ import annotations

import json
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from .engine import MesaEngine
from .models import UserTask

ROOT = Path(__file__).resolve().parent.parent
WEB_DIR = ROOT / "web"


class MesaRequestHandler(BaseHTTPRequestHandler):
    def _send_json(self, payload: dict, status: int = HTTPStatus.OK) -> None:
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def _serve_file(self, name: str) -> None:
        path = WEB_DIR / name
        if not path.exists() or not path.is_file():
            self.send_error(HTTPStatus.NOT_FOUND, "Archivo no encontrado")
            return

        content = path.read_bytes()
        content_type = "text/plain; charset=utf-8"
        if path.suffix == ".html":
            content_type = "text/html; charset=utf-8"
        elif path.suffix == ".css":
            content_type = "text/css; charset=utf-8"
        elif path.suffix == ".js":
            content_type = "application/javascript; charset=utf-8"

        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def do_GET(self) -> None:
        if self.path in ("/", "/index.html"):
            self._serve_file("index.html")
            return
        if self.path == "/app.js":
            self._serve_file("app.js")
            return
        if self.path == "/styles.css":
            self._serve_file("styles.css")
            return
        self.send_error(HTTPStatus.NOT_FOUND, "Ruta no encontrada")

    def do_POST(self) -> None:
        if self.path != "/api/run":
            self.send_error(HTTPStatus.NOT_FOUND, "Ruta no encontrada")
            return

        try:
            length = int(self.headers.get("Content-Length", "0"))
            if length <= 0:
                self._send_json({"error": "Body vacío"}, HTTPStatus.BAD_REQUEST)
                return

            payload = json.loads(self.rfile.read(length).decode("utf-8"))
            prompt = str(payload.get("prompt", "")).strip()
            if not prompt:
                self._send_json({"error": "prompt es obligatorio"}, HTTPStatus.BAD_REQUEST)
                return

            constraints = [str(x).strip() for x in payload.get("constraints", []) if str(x).strip()]
            preferences = [str(x).strip() for x in payload.get("preferences", []) if str(x).strip()]
            max_generations = int(payload.get("max_generations", 2))
            max_generations = max(1, min(max_generations, 5))

            engine = MesaEngine()
            trace = engine.run(
                UserTask(prompt=prompt, constraints=constraints, preferences=preferences),
                max_generations=max_generations,
            )
            self._send_json(
                {
                    "complexity": int(trace.complexity),
                    "generations": trace.generations,
                    "winner": trace.winner_id,
                    "final_solution": trace.final_solution,
                    "snapshots": trace.snapshots,
                }
            )
        except json.JSONDecodeError:
            self._send_json({"error": "JSON inválido"}, HTTPStatus.BAD_REQUEST)
        except Exception as exc:  # pragma: no cover
            self._send_json({"error": f"Error interno: {exc}"}, HTTPStatus.INTERNAL_SERVER_ERROR)


def run_server(host: str = "127.0.0.1", port: int = 8000) -> None:
    server = ThreadingHTTPServer((host, port), MesaRequestHandler)
    print(f"MESA web en http://{host}:{port}")
    server.serve_forever()


if __name__ == "__main__":
    run_server()
