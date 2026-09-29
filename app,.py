#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
🧸🥊 Bestie's Fight Club - Python Application Server & Engine
=============================================================================
A complete, robust, zero-dependency Python application for Bestie's Fight Club.
Provides:
  - Full local HTTP web server (Python standard library `http.server`)
  - Multi-threaded request handling for smooth 60fps canvas gaming
  - REST API backend for quiz stats, match history, leaderboard & roasts
  - Persistent JSON database (data/game_data.json)
  - Automatic browser launch & local network IP detection for mobile play
=============================================================================
"""

import sys
import os
import json
import socket
import threading
import webbrowser
import time
from urllib.parse import urlparse, parse_qs
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler

# Reconfigure standard output and error to UTF-8 on Windows
if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

# Optional colorized terminal output using installed colorama
try:
    from colorama import init, Fore, Style
    init(autoreset=True)
    HAS_COLOR = True
except ImportError:
    HAS_COLOR = False

def log_color(text, color="green"):
    if not HAS_COLOR:
        print(text)
        return
    colors = {
        "green": Fore.GREEN,
        "cyan": Fore.CYAN,
        "yellow": Fore.YELLOW,
        "red": Fore.RED,
        "magenta": Fore.MAGENTA,
        "bright": Style.BRIGHT
    }
    print(colors.get(color, Fore.WHITE) + text + Style.RESET_ALL)

# Directory configurations
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
DATA_FILE = os.path.join(DATA_DIR, "game_data.json")
INDEX_HTML = os.path.join(BASE_DIR, "index.html")

# Ensure data directory exists
os.makedirs(DATA_DIR, exist_ok=True)

# Initial database structure
INITIAL_DATA = {
    "quiz_attempts": [],
    "fight_records": [],
    "leaderboard": {
        "Ankita": {"quiz_passes": 0, "fights_won": 0, "total_score": 0},
        "Kanan": {"quiz_passes": 0, "fights_won": 0, "total_score": 0},
        "Kartik": {"quiz_passes": 0, "fights_won": 0, "total_score": 0}
    },
    "custom_roasts": [
        "Even a sleepy teddy bear punches harder than that! 😭",
        "Simmi Ma'am just gave you an F in Combat Studies. Go apologize to Ankita & Kanan right now! 💀",
        "Did you study for this fight like you studied for the exams? Zero preparation! 🤦‍♂️",
        "Your hits had less impact than Kartik saying 'Bas 2 min me aaya'! ⏰",
        "College attendance was higher than your hit accuracy! 🏛️"
    ]
}

import mimetypes
mimetypes.add_type('application/javascript', '.js')
mimetypes.add_type('text/css', '.css')
mimetypes.add_type('text/html', '.html')
mimetypes.add_type('application/json', '.json')

DATA_LOCK = threading.Lock()

def load_game_data():
    with DATA_LOCK:
        if not os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "w", encoding="utf-8") as f:
                    json.dump(INITIAL_DATA, f, indent=2, ensure_ascii=False)
            except Exception:
                pass
            return INITIAL_DATA
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"[Warning] Could not read {DATA_FILE}: {e}")
            return INITIAL_DATA

def save_game_data(data):
    with DATA_LOCK:
        try:
            with open(DATA_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"[Error] Failed to save {DATA_FILE}: {e}")

def get_local_ip():
    """Finds the local LAN IP address so other devices/phones can connect."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

class BestiesHandler(SimpleHTTPRequestHandler):
    """Custom HTTP Request Handler serving frontend + JSON REST APIs."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=BASE_DIR, **kwargs)

    def end_headers(self):
        # Enable CORS for seamless P2P & local testing
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path

        # 1. API: Server Health Status
        if path == "/api/status":
            self.send_json_response({
                "status": "online",
                "app": "Bestie's Fight Club 🧸🥊",
                "version": "2.0.0",
                "python_version": sys.version.split()[0],
                "local_ip": get_local_ip()
            })
            return

        # 2. API: Fetch Leaderboard & Stats
        if path == "/api/leaderboard":
            data = load_game_data()
            self.send_json_response(data.get("leaderboard", {}))
            return

        # 3. API: Fetch All Characters Meta
        if path == "/api/characters":
            characters_meta = [
                {"name": "Brahmdeep", "hindi": "ब्रह्मदीप", "avatar": "👳‍♂️", "trait": "Red Turban (Pagri)"},
                {"name": "Simmi Ma'am", "hindi": "सिम्मी मैम", "avatar": "👩‍🏫", "trait": "Glasses & Pointer"},
                {"name": "College", "hindi": "कॉलेज", "avatar": "🏛️", "trait": "Clock Crown Mascot"},
                {"name": "Rihan", "hindi": "रिहान", "avatar": "🕶️", "trait": "Cool Street Fighter"},
                {"name": "Saksham", "hindi": "सक्षम", "avatar": "⚡", "trait": "Lightning Speedster"},
                {"name": "Kanan", "hindi": "कनन", "avatar": "🎀", "trait": "Cute Teddy Boxer"},
                {"name": "Kartik", "hindi": "कार्तिक", "avatar": "🧢", "trait": "Cap-Wearing Brawler"},
                {"name": "Ankita", "hindi": "अंकिता", "avatar": "🌸", "trait": "Flower Blossom Champion"}
            ]
            self.send_json_response(characters_meta)
            return

        # 4. API: Dynamic Roast Generator
        if path == "/api/roast":
            params = parse_qs(parsed.query)
            character = params.get("character", ["Bestie"])[0]
            score = params.get("score", ["0"])[0]
            roasts = [
                f"{character}, even a sleepy teddy bear punches harder than that! 😭",
                f"Did {character} study for this fight like Kartik studies 1 night before exams? Zero preparation! 💀",
                f"Simmi Ma'am just deducted 10 internal marks from {character}'s scorecard! 👩‍🏫",
                f"{character}'s punch speed was slower than the group chat deciding where to eat! 🍕",
                f"Go apologize to the Bestie Trio right now! 🧸🥊"
            ]
            import random
            selected_roast = random.choice(roasts)
            self.send_json_response({"character": character, "score": score, "roast": selected_roast})
            return

        # 5. Root Route: Serve index.html
        if path in ("/", "/index.html"):
            if os.path.exists(INDEX_HTML):
                self.serve_file(INDEX_HTML, "text/html; charset=utf-8")
                return

        # Serve static assets through default handler
        super().do_GET()

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path

        # 1. API: Record Quiz Results
        if path == "/api/quiz-stats":
            payload = self.read_json_payload()
            if payload:
                player = payload.get("player", "Unknown")
                score = payload.get("score", 0)
                total = payload.get("total", 6)
                passed = payload.get("passed", False)

                data = load_game_data()
                data["quiz_attempts"].append({
                    "player": player,
                    "score": score,
                    "total": total,
                    "passed": passed,
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
                })
                # Update Leaderboard
                if player in data["leaderboard"]:
                    data["leaderboard"][player]["total_score"] += score
                    if passed:
                        data["leaderboard"][player]["quiz_passes"] += 1
                save_game_data(data)

                self.send_json_response({"success": True, "message": "Quiz attempt recorded by Python backend! 🎯"})
                return
            self.send_error_response("Invalid payload", 400)
            return

        # 2. API: Record Fight Results
        if path == "/api/record-fight":
            payload = self.read_json_payload()
            if payload:
                player = payload.get("player", "Unknown")
                enemy = payload.get("enemy", "Unknown")
                winner = payload.get("winner", "Unknown")
                mode = payload.get("mode", "solo")

                data = load_game_data()
                data["fight_records"].append({
                    "player": player,
                    "enemy": enemy,
                    "winner": winner,
                    "mode": mode,
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
                })
                if winner == "player" and player in data["leaderboard"]:
                    data["leaderboard"][player]["fights_won"] += 1
                save_game_data(data)

                self.send_json_response({"success": True, "message": "Fight match logged by Python backend! 🥊"})
                return
            self.send_error_response("Invalid payload", 400)
            return

        self.send_error_response("Endpoint not found", 404)

    def read_json_payload(self):
        try:
            content_length = int(self.headers.get("Content-Length", 0))
            raw_body = self.rfile.read(content_length).decode("utf-8")
            return json.loads(raw_body)
        except Exception as e:
            print(f"[Error] Failed to read JSON payload: {e}")
            return None

    def send_json_response(self, data, status=200):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def send_error_response(self, message, status=400):
        self.send_json_response({"error": message}, status)

    def serve_file(self, file_path, content_type):
        try:
            with open(file_path, "rb") as f:
                content = f.read()
            self.send_response(200)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(content)))
            self.end_headers()
            self.wfile.write(content)
        except Exception as e:
            print(f"[Error] Failed serving file {file_path}: {e}")
            self.send_error(500, "Internal Server Error")

    def log_message(self, format, *args):
        # Clean terminal logging
        sys.stderr.write(f"[Python Server] {self.address_string()} - {format % args}\n")

def find_available_port(start_port=5000, max_attempts=50):
    """Finds an open port starting from start_port."""
    for port in range(start_port, start_port + max_attempts):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(('127.0.0.1', port)) != 0:
                return port
    return start_port

def print_banner(port, local_ip):
    banner = f"""
========================================================================
   🧸🥊 BESTIE'S FIGHT CLUB - PYTHON APPLICATION SERVER 🥊🧸
========================================================================
   [Edition]   : Friendship vs Hands (Pure Python Web & Game Engine)
   [Status]    : RUNNING ONLINE 🟢
   [Local URL] : http://localhost:{port}
   [Phone URL] : http://{local_ip}:{port} (Play from any Phone/Tablet!)
   [API Path]  : http://localhost:{port}/api/status
========================================================================
   Controls:
   - D-PAD / Arrows  : Move / Jump / Crouch Block (🛡️)
   - A / J           : Punch [🥊]
   - S / K           : Kick [🦶]
   - D / L / Space   : Special Attack [⚡]
   - Press Ctrl + C  : Stop the server gracefully
========================================================================
    """
    log_color(banner, "bright")

def open_browser_delayed(url, delay=1.0):
    time.sleep(delay)
    try:
        webbrowser.open(url)
    except Exception as e:
        print(f"[Notice] Please open {url} in your browser ({e})")

def main():
    port = find_available_port(5000)
    local_ip = get_local_ip()

    server = ThreadingHTTPServer(("0.0.0.0", port), BestiesHandler)

    print_banner(port, local_ip)

    # Automatically launch browser in background thread
    threading.Thread(target=open_browser_delayed, args=(f"http://localhost:{port}",), daemon=True).start()

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        log_color("\n[Bestie's Fight Club] Server stopped gracefully. See you in the ring! 🧸🥊", "yellow")
        server.server_close()
        sys.exit(0)

if __name__ == "__main__":
    main()

