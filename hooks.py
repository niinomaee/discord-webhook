def load_hooks(cfg):
    return cfg.get("hooks", {})


def pick_hook(hooks):
    names = list(hooks.keys())

    print("\nAvailable webhooks:")
    for i, name in enumerate(names, 1):
        print(f"  [{i}] {name}")

    while True:
        choice = input("\nPick a webhook (number or name): ").strip()

        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(names):
                selected = names[idx]
                print(f"  -> Using: {selected}\n")
                return hooks[selected]
            else:
                print(f"  [!] Invalid number. Pick between 1 and {len(names)}.")

        elif choice in hooks:
            print(f"  -> Using: {choice}\n")
            return hooks[choice]

        else:
            print(f"  [!] '{choice}' not found. Try again.")