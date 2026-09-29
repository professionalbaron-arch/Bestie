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