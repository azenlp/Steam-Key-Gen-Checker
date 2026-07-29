import sys
from generator import generate_keys
from checker import is_valid_format, check_on_steam


def menu_gen():
    print()
    try:
        count = int(input("  Combien de clés veux-tu générer ? "))
    except ValueError:
        print("  Nombre invalide.")
        return

    groups = input("  Format 3x5 ou 5x5 ? (3/5) [défaut: 3] : ").strip()
    groups = int(groups) if groups in ("3", "5") else 3

    print(f"\n  Génération de {count} clé(s)...\n")
    keys = generate_keys(count, groups)

    for k in keys:
        if is_valid_format(k):
            print(f"  [VALID] {k}")
        else:
            print(f"  [INVALID] {k}")

    print()


def menu_check():
    print()
    key = input("  Entre la clé à vérifier : ").strip()
    if not key:
        return

    if not is_valid_format(key):
        print(f"\n  [INVALID] {key}  (Mauvais format)\n")
        return

    online = input("  Vérifier sur Steam ? (o/n) [défaut: n] : ").strip().lower()
    online = online == "o"

    if online:
        result = check_on_steam(key)
        status = "VALID" if result["valid"] else "INVALID"
        print(f"\n  [{status}] {key}  ({result['reason']})\n")
    else:
        print(f"\n  [VALID] {key}\n")


def main():
    while True:
        print("\n" + "=" * 40)
        print("  STEAM KEY GENERATOR & CHECKER")
        print("=" * 40)
        print("  1. Gen  — Générer + vérifier des clés")
        print("  2. Check — Vérifier une clé")
        print("  3. Quit")
        print("=" * 40)

        choice = input("  Choix : ").strip()

        if choice == "1":
            menu_gen()
        elif choice == "2":
            menu_check()
        elif choice in ("3", "q", "quit"):
            print("  Bye !")
            sys.exit(0)
        else:
            print("  Choix invalide.")


if __name__ == "__main__":
    main()
