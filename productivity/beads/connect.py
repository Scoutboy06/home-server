#!/usr/bin/env python3
"""Connect the current eden checkout to the home-server Beads database."""

import configparser
import json
import os
from pathlib import Path
import subprocess

HOST = "home-server.hydra-adelie.ts.net"
PORT = 3307
PROJECT_ID = "517735e0-52fa-432a-82f1-6b59f1ef4fde"

version = subprocess.check_output(["bd", "version"], text=True).strip()
if not version.startswith("bd version 1.3.1 ") and version != "bd version 1.3.1":
    raise SystemExit(f"Install Beads 1.3.1 before connecting; found: {version}")

subprocess.run(["git", "rev-parse", "--show-toplevel"], check=True, capture_output=True)
if not Path(".git").exists():
    raise SystemExit("Run this script from the root of your eden checkout.")

beads = Path(".beads")
metadata_path = beads / "metadata.json"
metadata = json.loads(metadata_path.read_text()) if metadata_path.exists() else {}
if metadata.get("project_id") not in (None, "", PROJECT_ID):
    raise SystemExit("This checkout belongs to another Beads project; refusing to change it.")

result = subprocess.run(
    ["ssh", "home-server", "cat ~/home-server/productivity/beads/.env"],
    check=True, capture_output=True, text=True,
)
settings = dict(line.split("=", 1) for line in result.stdout.splitlines() if "=" in line)
password = settings["DOLT_PASSWORD"]

credentials_path = Path(os.environ.get(
    "BEADS_CREDENTIALS_FILE", str(Path.home() / ".config/beads/credentials")
)).expanduser()
credentials_path.parent.mkdir(parents=True, exist_ok=True)
credentials = configparser.ConfigParser(interpolation=None)
if credentials_path.exists():
    credentials.read(credentials_path)
section = f"{HOST}:{PORT}"
if credentials.has_section(section):
    if credentials.get(section, "password", fallback="") != password:
        raise SystemExit("A different password is already stored for this server; resolve it first.")
else:
    # Append rather than rewriting other credentials or their comments.
    fd = os.open(credentials_path, os.O_WRONLY | os.O_CREAT | os.O_APPEND, 0o600)
    with os.fdopen(fd, "a") as handle:
        handle.write(f"\n[{section}]\npassword = {password}\n")
credentials_path.chmod(0o600)

beads.mkdir(mode=0o700, exist_ok=True)
backup_path = beads / "metadata.pre-home-server.json"
if metadata_path.exists() and not backup_path.exists():
    backup_path.write_text(metadata_path.read_text())
metadata.update({
    "database": "dolt",
    "backend": "dolt",
    "dolt_mode": "server",
    "dolt_database": "eden",
    "dolt_server_host": HOST,
    "dolt_server_user": "beads",
    "project_id": PROJECT_ID,
})
metadata.pop("dolt_server_port", None)
port_path = beads / "dolt-server.port"
port_backup = beads / "dolt-server.port.pre-home-server"
if port_path.exists() and not port_backup.exists():
    port_backup.write_text(port_path.read_text())
port_path.write_text(f"{PORT}\n")
metadata_path.write_text(json.dumps(metadata, indent=2) + "\n")
print(f"Configured eden → {HOST}:{PORT}; credentials saved with mode 600.")
print("Existing local databases were preserved, not merged. The server is the source of truth.")
print("Use Beads 1.3.1 on all clients. Conflicting BEADS_DOLT_* environment variables override this setup.")
subprocess.run(["bd", "dolt", "test"], check=True)
