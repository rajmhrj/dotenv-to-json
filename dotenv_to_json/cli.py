from __future__ import annotations
from typing import Any, Dict, cast
import json
import sys
from typing import Optional

from .parser import parse_env_lines, load_from_file


def _read_input(path: Optional[str]):
    if path is None or path == '-':
        return sys.stdin
    return open(path, 'r', encoding='utf-8')


def main(argv: Optional[list[str]] = None) -> int:
    import argparse

    parser = argparse.ArgumentParser(prog="env2json", description="Convert a .env file to JSON")
    parser.add_argument("-i", "--input", help="Input .env file path (default: stdin)", default=None)
    parser.add_argument("-o", "--output", help="Output JSON file path (default: stdout)", default=None)
    parser.add_argument("-p", "--pretty", help="Pretty-print JSON", action="store_true")
    args = parser.parse_args(argv)

    # Read and parse
    if args.input:
        try:
            env = load_from_file(args.input)
        except OSError as exc:
            print(
                f"env2json: cannot read '{args.input}': {exc.strerror or exc}",
                file=sys.stderr,
            )
            return 1
    else:
        env = parse_env_lines(_read_input(args.input))

    # Dump JSON
    dump_kwargs = {"indent": 2} if args.pretty else {}
    json_text = json.dumps(env, **cast(Dict[str, Any], dump_kwargs))

    if args.output:
        with open(args.output, 'w', encoding='utf-8') as fh:
            fh.write(json_text + "\n")
    else:
        sys.stdout.write(json_text + "\n")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
