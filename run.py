import argparse
import subprocess
import sys

COMMANDS: dict[str, list[str]] = {
    "dev": [sys.executable, "-m", "uvicorn", "app.main:app", "--reload"],
    "test": [sys.executable, "-m", "pytest"],
    "lint": [sys.executable, "-m", "ruff", "check", "."],
    "format": [sys.executable, "-m", "ruff", "format", "."],
}


def main() -> int:
    parser = argparse.ArgumentParser(description="Cross-platform project task runner")
    parser.add_argument("command", choices=[*COMMANDS, "help"], nargs="?", default="help")
    args = parser.parse_args()
    if args.command == "help":
        parser.print_help()
        print("\nCommands: dev, test, lint, format")
        return 0
    return subprocess.call(COMMANDS[args.command])


if __name__ == "__main__":
    raise SystemExit(main())
