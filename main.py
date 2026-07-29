import argparse
import sys
from generator import generate_keys
from checker import is_valid_format, check_on_steam


def cmd_generate(args):
    keys = generate_keys(args.count, args.groups)
    for k in keys:
        print(k)


def cmd_check(args):
    if args.key:
        keys = [args.key]
    elif args.file:
        with open(args.file) as f:
            keys = [line.strip() for line in f if line.strip()]
    else:
        keys = [line.strip() for line in sys.stdin if line.strip()]

    for k in keys:
        if not is_valid_format(k):
            print(f"[INVALID] {k}")
            continue

        if args.online:
            result = check_on_steam(k)
            status = "VALID" if result["valid"] else "INVALID"
            print(f"[{status}] {k} - {result['reason']}")
        else:
            print(f"[VALID] {k}")


def cmd_mass_gen_check(args):
    keys = generate_keys(args.count, args.groups)
    for k in keys:
        if args.online:
            result = check_on_steam(k)
            status = "VALID" if result["valid"] else "INVALID"
            print(f"[{status}] {k} - {result['reason']}")
        else:
            print(f"[VALID] {k}")


def main():
    parser = argparse.ArgumentParser(description="Steam Key Generator & Checker")
    sub = parser.add_subparsers(dest="command")

    gen = sub.add_parser("gen", help="Generate keys")
    gen.add_argument("-n", "--count", type=int, default=1, help="Number of keys (default: 1)")
    gen.add_argument("-g", "--groups", type=int, choices=[3, 5], default=3, help="Key format groups (3 or 5)")
    gen.set_defaults(func=cmd_generate)

    chk = sub.add_parser("check", help="Check keys")
    chk.add_argument("-k", "--key", help="Single key to check")
    chk.add_argument("-f", "--file", help="File with keys (one per line)")
    chk.add_argument("--online", action="store_true", help="Check against Steam servers")
    chk.set_defaults(func=cmd_check)

    mass = sub.add_parser("mass", help="Generate & check keys")
    mass.add_argument("-n", "--count", type=int, default=10, help="Number of keys")
    mass.add_argument("-g", "--groups", type=int, choices=[3, 5], default=3)
    mass.add_argument("--online", action="store_true", help="Check against Steam servers")
    mass.set_defaults(func=cmd_mass_gen_check)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    args.func(args)


if __name__ == "__main__":
    main()
