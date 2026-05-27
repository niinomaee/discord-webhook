# webhook-cli

Send Discord messages and embeds from your terminal via webhook.

> No dependencies — uses Python standard library only.

## Usage

### Manage webhooks (add, remove, list)

```bash
python manage.py
```

### Send a message

```bash
# Simple text
python send.py -m "Hello from terminal!"

# Pick webhook interactively (if -H is omitted)
python send.py -m "Hello!" 

# Use a named webhook
python send.py -H general -m "Hello!"

# Use a direct URL
python send.py --url https://discord.com/api/webhooks/... -m "Hello!"
```

### Send an embed

```bash
python send.py -H alerts \
  --title "Deploy complete" \
  --description "v1.2.0 is live 🚀" \
  --color "#00FF99" \
  --footer "GitHub Actions" \
  --field "Branch|main" \
  --field "Status|Success|true"
```

### Combine message + embed

```bash
python send.py -H general \
  -m "@here heads up!" \
  --title "Server restarting" \
  --description "Back in ~2 minutes" \
  --color "#FF5733"
```

### Override sender identity

```bash
python send.py -H general -m "Boo!" --username "Ghost" --avatar "https://example.com/ghost.png"
```

## Options

| Flag | Short | Description |
|---|---|---|
| `--hook` | `-H` | Named webhook from config.json |
| `--url` | | Direct webhook URL |
| `--message` | `-m` | Plain text message |
| `--title` | `-t` | Embed title |
| `--description` | `-d` | Embed description |
| `--color` | `-c` | Embed color in hex (`#RRGGBB`) |
| `--footer` | `-f` | Embed footer text |
| `--image` | `-i` | Embed image URL |
| `--field` | | Add field: `Name\|Value` or `Name\|Value\|true` (inline). Repeatable. |
| `--username` | | Override sender username |
| `--avatar` | | Override sender avatar URL |

## Getting a Webhook URL

1. Open your Discord server → channel settings → **Integrations** → **Webhooks**
2. Click **New Webhook**, copy the URL
3. Add it via `python manage.py`

## Config reference (`config.json`)

```json
{
  "default_username": "My Bot",
  "default_avatar": "https://example.com/avatar.png",
  "hooks": {
    "general": "https://discord.com/api/webhooks/...",
    "alerts": "https://discord.com/api/webhooks/..."
  }
}
```