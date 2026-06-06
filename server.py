import http.server
import socketserver
import os
import json
import urllib.parse

PORT = 8000
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=BASE_DIR, **kwargs)

    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Cache-Control", "no-cache")
        super().end_headers()

    def guess_type(self, path):
        if path.endswith(".glb"):
            return "model/gltf-binary"
        if path.endswith(".jpg") or path.endswith(".jpeg"):
            return "image/jpeg"
        return super().guess_type(path)

    def translate_path(self, path):
        path = urllib.parse.unquote(path)
        return super().translate_path(path)

    def do_GET(self):
        if self.path == "/api/models":
            assets_dir = os.path.join(BASE_DIR, "assets")
            try:
                models = sorted([
                    f for f in os.listdir(assets_dir)
                    if f.endswith(".glb")
                ])
                models = [m for m in models if m != "animal_rigged.glb"]
            except FileNotFoundError:
                models = []
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps({"models": models}).encode())
            return
        if self.path == "/api/paintings":
            assets_dir = os.path.join(BASE_DIR, "assets", "images")
            try:
                paintings = sorted([
                    f for f in os.listdir(assets_dir)
                    if f.endswith(".jpg") or f.endswith(".jpeg")
                ])
            except FileNotFoundError:
                paintings = []
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps({"paintings": paintings}).encode())
            return
        if self.path == "/api/name-map":
            name_file = os.path.join(BASE_DIR, "assets", "images", "name.txt")
            images_dir = os.path.join(BASE_DIR, "assets", "images")
            mapping = {}
            try:
                # Build list of actual image files: "01.jpg" -> {num:"01", ext:".jpg"}
                actual_files = {}
                for fn in os.listdir(images_dir):
                    if fn.endswith(".jpg") or fn.endswith(".jpeg"):
                        bn, ext = os.path.splitext(fn)
                        actual_files[bn] = ext
                with open(name_file, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if not line:
                            continue
                        parts = line.split(".", 1)
                        if len(parts) == 2:
                            num = parts[0].strip().zfill(2)
                            rest = parts[1].strip()
                            if rest.endswith(".jpg"):
                                rest = rest[:-4]
                            elif rest.endswith(".jpeg"):
                                rest = rest[:-5]
                            ext = actual_files.get(num, ".jpg")
                            mapping[num + ext] = rest
            except FileNotFoundError:
                pass
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(mapping).encode())
            return
        if self.path == "/api/paintings-layout":
            layout_file = os.path.join(BASE_DIR, "assets", "images", "paintings-layout.json")
            if os.path.exists(layout_file):
                try:
                    with open(layout_file, "r", encoding="utf-8") as f:
                        data = json.load(f)
                except Exception:
                    data = None
            else:
                data = None
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps({"layout": data}).encode())
            return
        if self.path == "/api/painting-sizes":
            assets_dir = os.path.join(BASE_DIR, "assets", "images")
            sizes = {}
            try:
                for f in sorted(os.listdir(assets_dir)):
                    if f.endswith(".jpg") or f.endswith(".jpeg"):
                        try:
                            from PIL import Image
                            img = Image.open(os.path.join(assets_dir, f))
                            sizes[f] = [img.width, img.height]
                        except ImportError:
                            sizes[f] = [1, 1]
            except FileNotFoundError:
                pass
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(sizes).encode())
            return
        super().do_GET()

    def do_POST(self):
        if self.path == "/api/paintings-layout":
            content_len = int(self.headers.get("Content-Length", 0))
            if content_len > 0:
                body = self.rfile.read(content_len)
                try:
                    data = json.loads(body)
                    layout_file = os.path.join(BASE_DIR, "assets", "images", "paintings-layout.json")
                    with open(layout_file, "w", encoding="utf-8") as f:
                        json.dump(data, f, ensure_ascii=False, indent=2)
                    self.send_response(200)
                    self.send_header("Content-Type", "application/json")
                    self.send_header("Access-Control-Allow-Origin", "*")
                    self.end_headers()
                    self.wfile.write(json.dumps({"ok": True}).encode())
                    return
                except Exception as e:
                    self.send_response(400)
                    self.send_header("Content-Type", "application/json")
                    self.send_header("Access-Control-Allow-Origin", "*")
                    self.end_headers()
                    self.wfile.write(json.dumps({"error": str(e)}).encode())
                    return
        self.send_response(404)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps({"error": "Not found"}).encode())

with socketserver.ThreadingTCPServer(("0.0.0.0", PORT), MyHandler) as httpd:
    print(f"Museum server running at http://localhost:{PORT}")
    httpd.serve_forever()
