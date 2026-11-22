"""Open this machine's phishing-detector interface in a local web browser.

Requires Python 3.10+. This does not publish the app to the internet.
"""
import argparse
import sys
import threading
import webbrowser

from ui_server import HOST, PORT, create_server


def main() -> int:
    if sys.version_info < (3, 10):
        print("Python 3.10+ is required.", file=sys.stderr)
        return 2

    parser = argparse.ArgumentParser(description="Start phishing detector locally")
    parser.add_argument("--no-browser", action="store_true", help="Do not automatically open browser")
    parser.add_argument("--port", type=int, default=PORT, help="Local listen port")
    args = parser.parse_args()
    if args.port < 0 or args.port > 65535:
        parser.error("Port must be from 0 to 65535")

    try:
        server = create_server(HOST, args.port)
    except OSError as exc:
        print(f"Cannot start local server: {exc}", file=sys.stderr)
        print("Another copy may already be using port 8765. Close it and retry.", file=sys.stderr)
        return 1

    url = f"http://{HOST}:{server.server_port}"
    print(f"Phishing Detector: {url}", flush=True)
    print("This app runs on your own computer. Press Ctrl+C to stop.", flush=True)
    if not args.no_browser:
        # Open only after the socket has been bound. No external websites are visited.
        threading.Timer(0.5, lambda: webbrowser.open_new_tab(url)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping server.")
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
