import json
import sys
import argparse
import urllib.request
import urllib.error
from hooks import load_hooks, pick_hook

CONFIG_FILE = "config.json"


def load_config():
    try:
        with open(CONFIG_FILE) as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def hex_to_int(hex_color):
    hex_color = hex_color.lstrip("#")
    return int(hex_color, 16)


def build_payload(args, cfg):
    payload = {}

    if args.username or cfg.get("default_username"):
        payload["username"] = args.username or cfg.get("default_username")
    if args.avatar or cfg.get("default_avatar"):
        payload["avatar_url"] = args.avatar or cfg.get("default_avatar")

    if args.message:
        payload["content"] = args.message

    if any([args.title, args.description, args.color, args.field, args.footer, args.image]):
        embed = {}

        if args.title:
            embed["title"] = args.title
        if args.description:
            embed["description"] = args.description
        if args.color:
            try:
                embed["color"] = hex_to_int(args.color)
            except ValueError:
                print(f"[!] Invalid color '{args.color}', skipping.")
        if args.footer:
            embed["footer"] = {"text": args.footer}
        if args.image:
            embed["image"] = {"url": args.image}
        if args.field:
            fields = []
            for f in args.field:
                parts = f.split("|")
                if len(parts) < 2:
                    print(f"[!] Invalid field format '{f}'. Use 'Name|Value' or 'Name|Value|inline'")
                    continue
                field = {
                    "name": parts[0],
                    "value": parts[1],
                    "inline": parts[2].lower() == "true" if len(parts) > 2 else False
                }
                fields.append(field)
            if fields:
                embed["fields"] = fields

        payload["embeds"] = [embed]

    if not payload.get("content") and not payload.get("embeds"):
        print("[!] Nothing to send. Provide --message and/or embed options.")
        sys.exit(1)

    return payload


def send_webhook(url, payload):
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json", "User-Agent": "DiscordBot (webhook-cli, 1.0)"},
        method="POST"
    )
    try:
        with urllib.request.urlopen(req) as res:
            if res.status == 204:
                print("-> Message sent.")
            else:
                print(f"-> Sent with status {res.status}")
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f"[!] HTTP {e.code}: {body}")
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"[!] Connection error: {e.reason}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        prog="send.py",
        description="Discord Webhook CLI — send messages and embeds from your terminal."
    )

    parser.add_argument("-H", "--hook", help="Webhook name (from config.json). If omitted, prompts to pick.")
    parser.add_argument("-u", "--url", help="Direct webhook URL (skip config lookup).")
    parser.add_argument("-m", "--message", help="Plain text message content.")
    parser.add_argument("-t", "--title", help="Embed title.")
    parser.add_argument("-d", "--description", help="Embed description.")
    parser.add_argument("-c", "--color", help="Embed color in hex, e.g. #FF5733.")
    parser.add_argument("-f", "--footer", help="Embed footer text.")
    parser.add_argument("-i", "--image", help="Embed image URL.")
    parser.add_argument(
        "--field", action="append", metavar="Name|Value[|inline]",
        help="Add a field. Format: 'Name|Value' or 'Name|Value|true'. Can be used multiple times."
    )
    parser.add_argument("--username", help="Override webhook username.")
    parser.add_argument("--avatar", help="Override webhook avatar URL.")

    args = parser.parse_args()

    cfg = load_config()
    hooks = load_hooks(cfg)

    if args.url:
        webhook_url = args.url
    elif args.hook:
        if args.hook not in hooks:
            print(f"[!] Hook '{args.hook}' not found in config.json.")
            print(f"    Available: {', '.join(hooks.keys()) or '(none)'}")
            sys.exit(1)
        webhook_url = hooks[args.hook]
    else:
        if not hooks:
            print("[!] No webhooks configured. Run: python manage.py")
            sys.exit(1)
        webhook_url = pick_hook(hooks)

    payload = build_payload(args, cfg)
    send_webhook(webhook_url, payload)


if __name__ == "__main__":
    main()