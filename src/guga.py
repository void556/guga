#!/usr/bin/env python3
import sys
import os
import subprocess
import shutil
import urllib.request
import json
from pathlib import Path

BUILD_DIR = Path("/tmp/guga_builds")
AUR_RPC_URL = "https://aur.archlinux.org/rpc/v5/search/"

def print_status(msg, color="32"): # Green status text
    print(f"\033[1;{color}m[guga]\033[0m {msg}")

def check_dependencies():
    for tool in ["git", "makepkg", "pacman"]:
        if not shutil.which(tool):
            print_status(f"Error: Missing required tool '{tool}'", "31")
            sys.exit(1)

def search_aur(query):
    print_status(f"Searching AUR for '{query}'...")
    url = f"{AUR_RPC_URL}{urllib.parse.quote(query)}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "guga-aur-helper"})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode("utf-8"))
            results = data.get("results", [])
            
            if not results:
                print_status("No packages found.", "33")
                return

            print("\n  \033[1mName\033[0m \t\t \033[1mVersion\033[0m \t\t \033[1mDescription\033[0m")
            print("-" * 60)
            for pkg in results[:15]: # Limit output to top 15 matches
                name = pkg.get("Name")
                ver = pkg.get("Version")
                desc = pkg.get("Description") or "No description"
                print(f"  \033[1;34m{name}\033[0m \t {ver} \t {desc[:40]}...")
            print()
    except Exception as e:
        print_status(f"Failed to fetch search results: {e}", "31")

def install_package(pkg_name):
    check_dependencies()
    BUILD_DIR.mkdir(parents=True, exist_ok=True)
    pkg_dir = BUILD_DIR / pkg_name

    if pkg_dir.exists():
        shutil.rmtree(pkg_dir)

    print_status(f"Cloning AUR repository for '{pkg_name}'...")
    clone_url = f"https://aur.archlinux.org/{pkg_name}.git"
    git_res = subprocess.run(["git", "clone", clone_url, str(pkg_dir)])

    if git_res.returncode != 0:
        print_status(f"Failed to clone package '{pkg_name}'", "31")
        return

    print_status(f"Building and installing '{pkg_name}' via makepkg...")
    os.chdir(pkg_dir)
    makepkg_res = subprocess.run(["makepkg", "-si"])

    if makepkg_res.returncode == 0:
        print_status(f"Successfully installed '{pkg_name}'!", "32")
    else:
        print_status(f"Build/installation failed for '{pkg_name}'", "31")

def show_help():
    print("""\033[1mguga\033[0m - Lightweight Python AUR Helper

Usage:
  guga -S <pkgname>     Install an AUR package
  guga -Ss <query>     Search for an AUR package
  guga -h              Show this help menu
""")

def main():
    if len(sys.argv) < 2:
        show_help()
        sys.exit(0)

    flag = sys.argv[1]

    if flag == "-S" and len(sys.argv) >= 3:
        for pkg in sys.argv[2:]:
            install_package(pkg)
    elif flag == "-Ss" and len(sys.argv) >= 3:
        search_aur(sys.argv[2])
    elif flag in ["-h", "--help"]:
        show_help()
    else:
        print_status("Invalid usage.", "31")
        show_help()

if __name__ == "__main__":
    main()
