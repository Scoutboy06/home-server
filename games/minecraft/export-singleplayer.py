#!/usr/bin/env python3

import os
import shutil
import zipfile
from pathlib import Path

# -------- CONFIG --------
DATA_DIR = Path("./minecraft-data")
WORLD_NAME = "world"
OUTPUT_ZIP = Path("./world_singleplayer.zip")
TEMP_DIR = Path("./_singleplayer_export")
# ------------------------

def abort(msg):
    print(f"ERROR: {msg}")
    exit(1)

def ensure_exists(path, desc):
    if not path.exists():
        abort(f"{desc} not found: {path}")

def clean_dir(path):
    if path.exists():
        shutil.rmtree(path)

def main():
    print("Starting Paper → Vanilla (Singleplayer) migration")

    world = DATA_DIR / WORLD_NAME
    nether = DATA_DIR / f"{WORLD_NAME}_nether" / "DIM-1"
    end = DATA_DIR / f"{WORLD_NAME}_the_end" / "DIM1"

    ensure_exists(world, "Overworld")
    ensure_exists(nether, "Nether DIM-1")
    ensure_exists(end, "End DIM1")

    clean_dir(TEMP_DIR)
    TEMP_DIR.mkdir(parents=True)

    print("Copying overworld...")
    shutil.copytree(world, TEMP_DIR / WORLD_NAME)

    sp_world = TEMP_DIR / WORLD_NAME

    # Remove vanilla dimensions if present
    for dim in ["DIM-1", "DIM1"]:
        dim_path = sp_world / dim
        if dim_path.exists():
            print(f"Removing existing {dim} folder")
            shutil.rmtree(dim_path)

    print("Migrating Nether...")
    shutil.copytree(nether, sp_world / "DIM-1")

    print("Migrating End...")
    shutil.copytree(end, sp_world / "DIM1")

    print("Creating zip archive...")
    with zipfile.ZipFile(OUTPUT_ZIP, "w", zipfile.ZIP_DEFLATED) as z:
        for file in sp_world.rglob("*"):
            z.write(file, file.relative_to(TEMP_DIR))

    print("Cleaning up temp files...")
    shutil.rmtree(TEMP_DIR)

    print("\nMigration complete!")
    print(f"Output file: {OUTPUT_ZIP.resolve()}")
    print("\nNext steps:")
    print("1. Copy the zip to your local machine")
    print("2. Unzip into ~/.minecraft/saves/")
    print("3. Launch Minecraft (same version as server)")
    print("4. Open world → Open to LAN → Enable cheats → /gamemode creative")

if __name__ == "__main__":
    main()
