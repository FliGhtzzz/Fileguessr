import sys
import os
import subprocess
import socket
import httpx
import logging

def check_python():
    print(f"--- Python Environment ---")
    print(f"Executable: {sys.executable}")
    print(f"Version: {sys.version}")
    print(f"CWD: {os.getcwd()}")

def check_dependencies():
    print(f"\n--- Dependencies ---")
    try:
        import fastapi
        print(f"[OK] fastapi {fastapi.__version__}")
    except ImportError:
        print(f"[FAIL] fastapi not found")

    try:
        import elasticsearch
        print(f"[OK] elasticsearch found")
    except ImportError:
        print(f"[FAIL] elasticsearch not found")

    try:
        import httpx
        print(f"[OK] httpx found")
    except ImportError:
        print(f"[FAIL] httpx not found")

def check_ollama():
    print(f"\n--- Ollama Status ---")
    url = "http://127.0.0.1:11434/api/tags"
    try:
        with httpx.Client(timeout=5.0) as client:
            resp = client.get(url)
            if resp.status_code == 200:
                print(f"[OK] Ollama is running")
                models = resp.json().get("models", [])
                model_names = [m["name"] for m in models]
                print(f"Available Models: {', '.join(model_names)}")
                
                # Check for gemma3:4b
                if any("gemma3:4b" in m for m in model_names):
                    print(f"[OK] gemma3:4b is available")
                else:
                    print(f"[WARN] gemma3:4b NOT found. Recommended to run 'ollama pull gemma3:4b'")
            else:
                print(f"[FAIL] Ollama returned status code {resp.status_code}")
    except Exception as e:
        print(f"[FAIL] Cannot connect to Ollama: {e}")

def check_elasticsearch():
    print(f"\n--- Elasticsearch Status ---")
    host = "127.0.0.1"
    port = 9200
    try:
        with socket.create_connection((host, port), timeout=2):
            print(f"[OK] Elasticsearch port {port} is open")
            
            # Check info
            try:
                with httpx.Client(timeout=5.0) as client:
                    resp = client.get(f"http://{host}:{port}")
                    if resp.status_code == 200:
                        info = resp.json()
                        version = info.get("version", {}).get("number", "unknown")
                        print(f"[OK] Elasticsearch version: {version}")
                    else:
                        print(f"[WARN] ES returned status {resp.status_code}")
            except Exception as e:
                print(f"[WARN] Could not get ES info: {e}")
    except Exception as e:
        print(f"[FAIL] Elasticsearch port {port} is CLOSED ({e})")

if __name__ == "__main__":
    print("==================================================")
    print("       File Guessr - Environment Diagnosis")
    print("==================================================")
    check_python()
    check_dependencies()
    check_ollama()
    check_elasticsearch()
    print("\n==================================================")
    input("Press Enter to exit...")
