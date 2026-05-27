import json
import os

CONFIG_FILE = "config.json"


def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE) as f:
            return json.load(f)
    return {}


def save_config(cfg):
    with open(CONFIG_FILE, "w") as f:
        json.dump(cfg, f, indent=2)


def list_hooks(hooks):
    if not hooks:
        print("  (no webhooks configured)")
        return
    for name, url in hooks.items():
        short_url = url[:50] + "..." if len(url) > 50 else url
        print(f"  {name} -> {short_url}")


def add_hook(hooks):
    print("\n-- Add Webhook --")
    name = input("  Name (e.g. general, logs, alerts): ").strip()
    if not name:
        print("  [!] Name cannot be empty.")
        return hooks
    if name in hooks:
        overwrite = input(f"  '{name}' already exists. Overwrite? [y/N]: ").strip().lower()
        if overwrite != "y":
            print("  Cancelled.")
            return hooks
    url = input("  Webhook URL: ").strip()
    if not url.startswith("https://discord.com/api/webhooks/"):
        print("  [!] URL doesn't look like a Discord webhook. Saving anyway.")
    hooks[name] = url
    print(f"  '{name}' added.")
    return hooks


def remove_hook(hooks):
    if not hooks:
        print("  No webhooks to remove.")
        return hooks
    print("\n-- Remove Webhook --")
    list_hooks(hooks)
    name = input("\n  Name to remove: ").strip()
    if name not in hooks:
        print(f"  [!] '{name}' not found.")
        return hooks
    confirm = input(f"  Remove '{name}'? [y/N]: ").strip().lower()
    if confirm == "y":
        del hooks[name]
        print(f"  '{name}' removed.")
    else:
        print("  Cancelled.")
    return hooks


def set_defaults(cfg):
    print("\n-- Default Sender Identity --")
    current_username = cfg.get("default_username", "")
    current_avatar = cfg.get("default_avatar", "")
    val = input(f"  Default username [{current_username or 'none'}]: ").strip()
    cfg["default_username"] = val if val else current_username
    val = input(f"  Default avatar URL [{current_avatar or 'none'}]: ").strip()
    cfg["default_avatar"] = val if val else current_avatar
    return cfg


def main():
    cfg = load_config()
    hooks = cfg.get("hooks", {})

    while True:
        print("\n" + "=" * 36)
        print("  Discord Webhook Manager")
        print("=" * 36)
        print("  [1] List webhooks")
        print("  [2] Add webhook")
        print("  [3] Remove webhook")
        print("  [4] Set default username / avatar")
        print("  [5] Exit")

        choice = input("\n  Choice: ").strip()

        if choice == "1":
            print("\nWebhooks:")
            list_hooks(hooks)

        elif choice == "2":
            hooks = add_hook(hooks)
            cfg["hooks"] = hooks
            save_config(cfg)

        elif choice == "3":
            hooks = remove_hook(hooks)
            cfg["hooks"] = hooks
            save_config(cfg)

        elif choice == "4":
            cfg = set_defaults(cfg)
            save_config(cfg)
            print("  Defaults saved.")

        elif choice == "5":
            break

        else:
            print("  [!] Invalid choice.")


if __name__ == "__main__":
    main()