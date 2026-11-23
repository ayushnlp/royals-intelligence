#!/usr/bin/env python3
"""
Royals Intelligence — Unified Local Development Orchestrator
Starts, health-checks, monitors, and cleanly shuts down both FastAPI backend
and Next.js frontend in a single command.
"""

import os
import sys
import time
import signal
import socket
import argparse
import subprocess
import threading
import urllib.request
import urllib.error

# Root project paths
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BACKEND_DIR = os.path.join(ROOT_DIR, "backend")
FRONTEND_DIR = os.path.join(ROOT_DIR, "frontend")

BACKEND_HOST = "127.0.0.1"
BACKEND_PORT = 8000
FRONTEND_PORT = 3000

# Color formatting for terminal
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
MAGENTA = "\033[95m"
BOLD = "\033[1m"
RESET = "\033[0m"


def log(prefix: str, color: str, msg: str):
    timestamp = time.strftime("%H:%M:%S")
    print(f"{color}[{timestamp}] {prefix}{RESET} {msg}", flush=True)


def is_port_in_use(port: int, host: str = "127.0.0.1") -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.5)
        return s.connect_ex((host, port)) == 0


def check_backend_healthy(timeout_sec: float = 2.0) -> bool:
    url = f"http://{BACKEND_HOST}:{BACKEND_PORT}/api/v1/health"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "RoyalsDevOrchestrator"})
        with urllib.request.urlopen(req, timeout=timeout_sec) as resp:
            data = resp.read().decode("utf-8")
            return resp.status == 200 and ("status" in data or "healthy" in data)
    except Exception:
        return False


def kill_proc_tree(pid: int):
    """
    Cleanly terminates only an owned child process and its immediate subprocess tree.
    Guaranteed never to kill foreign or un-owned system processes.
    """
    if not pid:
        return
    try:
        if os.name == "nt":
            subprocess.run(
                ["taskkill", "/F", "/T", "/PID", str(pid)],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=False,
            )
        else:
            try:
                os.killpg(os.getpgid(pid), signal.SIGTERM)
            except Exception:
                os.kill(pid, signal.SIGTERM)
    except Exception:
        pass


def pipe_output(proc: subprocess.Popen, prefix: str, color: str):
    """Streams child process stdout/stderr with colored prefix."""
    try:
        if proc.stdout:
            for line in iter(proc.stdout.readline, b""):
                if not line:
                    break
                decoded = line.decode("utf-8", errors="replace").rstrip("\r\n")
                if decoded:
                    log(prefix, color, decoded)
    except Exception:
        pass


def main():
    parser = argparse.ArgumentParser(description="Royals Intelligence Unified Dev Orchestrator")
    parser.add_argument("--backend-only", action="store_true", help="Start only FastAPI backend")
    parser.add_argument("--frontend-only", action="store_true", help="Start only Next.js frontend")
    parser.add_argument("--prod", action="store_true", help="Run frontend in production mode (next start)")
    args = parser.parse_args()

    print(f"\n{BOLD}{MAGENTA}=================================================================={RESET}")
    print(f"{BOLD}{MAGENTA}  ROYALS INTELLIGENCE — UNIFIED LOCAL DEVELOPMENT WORKFLOW        {RESET}")
    print(f"{BOLD}{MAGENTA}=================================================================={RESET}\n")

    backend_proc = None
    frontend_proc = None
    spawned_backend = False

    # Graceful shutdown handler: STRICTLY terminating ONLY owned child PIDs
    def shutdown(signum=None, frame=None):
        log("[SHUTDOWN]", YELLOW, "Received termination signal. Shutting down cleanly...")
        if spawned_backend and backend_proc and backend_proc.poll() is None:
            log("[SHUTDOWN]", YELLOW, f"Stopping owned FastAPI backend (PID {backend_proc.pid})...")
            kill_proc_tree(backend_proc.pid)

        if frontend_proc and frontend_proc.poll() is None:
            log("[SHUTDOWN]", YELLOW, f"Stopping owned Next.js frontend (PID {frontend_proc.pid})...")
            kill_proc_tree(frontend_proc.pid)

        log("[SHUTDOWN]", GREEN, "Owned services stopped cleanly. Local ports released.")
        sys.exit(0)

    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)

    # --------------------------------------------------------------------------
    # 1. START & VERIFY BACKEND
    # --------------------------------------------------------------------------
    if not args.frontend_only:
        backend_already_up = is_port_in_use(BACKEND_PORT)
        if backend_already_up:
            if check_backend_healthy():
                log("[BACKEND]", GREEN, f"✓ Existing healthy Royals Intelligence backend detected on http://{BACKEND_HOST}:{BACKEND_PORT}. Reusing instance.")
            else:
                log("[BACKEND]", RED, f"FATAL: Port {BACKEND_PORT} is in use by an external/unresponsive process.")
                log("[BACKEND]", RED, "For security and process isolation, external processes are NEVER terminated automatically.")
                log("[BACKEND]", RED, f"Please stop the process using port {BACKEND_PORT} and retry.")
                sys.exit(1)

        if not backend_already_up:
            log("[BACKEND]", CYAN, f"Starting FastAPI backend on http://{BACKEND_HOST}:{BACKEND_PORT}...")
            backend_cmd = [
                sys.executable,
                "-m",
                "uvicorn",
                "app.main:app",
                "--host",
                BACKEND_HOST,
                "--port",
                str(BACKEND_PORT),
                "--reload",
            ]
            backend_proc = subprocess.Popen(
                backend_cmd,
                cwd=BACKEND_DIR,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
            )
            spawned_backend = True

            # Start background log streaming for backend
            t_backend = threading.Thread(
                target=pipe_output,
                args=(backend_proc, "[BACKEND] ", CYAN),
                daemon=True,
            )
            t_backend.start()

            # Readiness probe: wait for /api/v1/health to return 200
            log("[BACKEND]", YELLOW, f"Waiting for backend readiness probe on http://{BACKEND_HOST}:{BACKEND_PORT}/api/v1/health...")
            start_time = time.time()
            backend_ready = False
            while time.time() - start_time < 20.0:
                if backend_proc.poll() is not None:
                    log("[BACKEND]", RED, f"FATAL: Backend process exited prematurely with code {backend_proc.returncode}!")
                    shutdown()
                    return

                if check_backend_healthy():
                    backend_ready = True
                    break
                time.sleep(0.4)

            if not backend_ready:
                log("[BACKEND]", RED, f"FATAL: Backend failed to become healthy within 20 seconds!")
                shutdown()
                return

            log("[BACKEND]", GREEN, f"✓ FastAPI backend is READY and operational (HTTP 200).")

    if args.backend_only:
        log("[INFO]", GREEN, "Running in backend-only mode. Press Ctrl+C to stop.")
        while True:
            if backend_proc and backend_proc.poll() is not None:
                log("[BACKEND]", RED, f"Backend exited with code {backend_proc.returncode}")
                break
            time.sleep(1)
        return

    # --------------------------------------------------------------------------
    # 2. START & VERIFY FRONTEND
    # --------------------------------------------------------------------------
    if is_port_in_use(FRONTEND_PORT):
        log("[FRONTEND]", RED, f"FATAL: Port {FRONTEND_PORT} is already in use by another process.")
        log("[FRONTEND]", RED, "For security and process isolation, external processes are NEVER terminated automatically.")
        log("[FRONTEND]", RED, f"Please stop the process using port {FRONTEND_PORT} and retry.")
        shutdown()
        return

    frontend_script = "start" if args.prod else "dev"
    log("[FRONTEND]", MAGENTA, f"Starting Next.js frontend (npm run {frontend_script}) on http://localhost:{FRONTEND_PORT}...")
    
    # Use npm through shell on Windows
    npm_cmd = "npm.cmd" if os.name == "nt" else "npm"
    frontend_proc = subprocess.Popen(
        [npm_cmd, "run", frontend_script],
        cwd=FRONTEND_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )

    t_frontend = threading.Thread(
        target=pipe_output,
        args=(frontend_proc, "[FRONTEND]", MAGENTA),
        daemon=True,
    )
    t_frontend.start()

    log("[ORCHESTRATOR]", GREEN, f"✓ Both services active! Access dashboard at: {BOLD}http://localhost:{FRONTEND_PORT}{RESET}")
    log("[ORCHESTRATOR]", GREEN, "Press Ctrl+C to terminate both services cleanly.\n")

    # --------------------------------------------------------------------------
    # 3. CONTINUOUS PROCESS MONITORING
    # --------------------------------------------------------------------------
    try:
        while True:
            # Check backend health
            if spawned_backend and backend_proc:
                b_code = backend_proc.poll()
                if b_code is not None:
                    log("[FATAL]", RED, f"Backend process crashed or exited unexpectedly with code {b_code}!")
                    break

            # Check frontend health
            if frontend_proc:
                f_code = frontend_proc.poll()
                if f_code is not None:
                    log("[FATAL]", RED, f"Frontend process crashed or exited unexpectedly with code {f_code}!")
                    break

            time.sleep(1.0)
    except KeyboardInterrupt:
        pass
    finally:
        shutdown()


if __name__ == "__main__":
    main()
