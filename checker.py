import re
import requests

STEAM_URL = "https://store.steampowered.com/account/registerkey"

KEY_PATTERNS = [
    re.compile(r"^[A-Z0-9]{5}-[A-Z0-9]{5}-[A-Z0-9]{5}$"),
    re.compile(r"^[A-Z0-9]{5}-[A-Z0-9]{5}-[A-Z0-9]{5}-[A-Z0-9]{5}-[A-Z0-9]{5}$"),
]

def is_valid_format(key):
    key = key.strip().upper()
    return any(p.match(key) for p in KEY_PATTERNS)

def check_on_steam(key):
    if not is_valid_format(key):
        return {"valid": False, "reason": "Invalid format"}

    session = requests.Session()
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://store.steampowered.com/",
    })

    try:
        r = session.post(STEAM_URL, data={"product_key": key}, timeout=15)

        if "application/json" not in r.headers.get("Content-Type", ""):
            return {"valid": False, "reason": "Steam demande une connexion - ouvre https://store.steampowered.com dans ton navigateur d'abord"}

        data = r.json()

        if data.get("success") == 1:
            return {"valid": True, "reason": "Key is valid and not used"}
        elif data.get("success") == 2:
            return {"valid": True, "reason": "Key already used on this account"}
        else:
            return {"valid": False, "reason": data.get("message", "Unknown response")}

    except requests.exceptions.JSONDecodeError:
        return {"valid": False, "reason": "Steam a retourné une page HTML (connexion requise)"}
    except Exception as e:
        return {"valid": False, "reason": f"Erreur: {e}"}
