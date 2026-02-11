# Razor Token Checker

A fast and powerful Discord token checker that helps you check and sort your tokens easily.

## What it Does

- 🔍 **Token Checking**
  - Checks if tokens are valid
  - Finds Nitro tokens (with subscription period and days left)
  - Checks for available boosts and cooldown status
  - Shows how old accounts are
  - Checks account verification type (Unclaimed, Email verified, Phone verified, Fully verified)
  - Spots flagged accounts
  - Detects redeemable vs non-redeemable accounts (Nitro gift eligibility)

- ⚡ **Speed & Performance**
  - Multi-threaded checking (configurable thread count)
  - Optional proxy support
  - Automatic rate-limit handling (re-queues tokens)
  - Retry logic for connection/timeout/SSL errors
  - Uses `curl_cffi` with Chrome impersonation for reliability

- 📊 **Sorting & Organization**
  - Saves tokens in separate files by status and type
  - Groups by account age (Years / Month)
  - Nitro tokens sorted by cooldown, subscription length, and boost count
  - Type-based files (Unclaimed, Email verified, etc.)
  - Redeemable / Non Redeemable lists when enabled

- 🎨 **Easy to Use**
  - Live console stats and progress
  - Windows console title shows Valid, Invalid, Locked, Remaining, % checked, and CPS
  - Press Enter to exit when done

## How to Get Started

1. **Clone the repository**
```bash
git clone https://github.com/Ghost1503/Razor-Token-Checker.git
cd Razor-Token-Checker
```

2. **Install dependencies**
```bash
pip install colorama pystyle toml curl_cffi
```

3. **Set it up**
   - Put your tokens in `data/tokens.txt`
   - Add proxies to `data/proxies.txt` (optional; leave empty if using proxyless)
   - Configure `data/config.toml`
   - Configure `data/settings.json`

## Settings

### config.toml
```toml
[main]
threads = 100
proxyless = false
```

| Option     | Description                                      |
|-----------|--------------------------------------------------|
| `threads` | Number of concurrent checker threads             |
| `proxyless` | If `true`, run without proxies (ignore proxies.txt) |

### settings.json
```json
{
  "flagged": true,
  "type": true,
  "age": true,
  "nitro": true,
  "redeemable": true
}
```

| Option       | Description                                                                 |
|-------------|-----------------------------------------------------------------------------|
| `flagged`   | Save flagged tokens to `flagged.txt` and count them                        |
| `type`     | Resolve verification type and save to type-based files and Age subfolders  |
| `age`      | Compute account age and sort into `Age/[X] Years` or `Age/[X] Month`       |
| `nitro`    | Check Nitro/subscriptions, boosts, cooldown; sort into `Nitro/` and `No Nitro.txt` |
| `redeemable` | Check if account can receive Nitro gifts; save to `Redeemable.txt` / `Non Redeemable.txt` |

## How to Use

1. **Run the checker**
```bash
python main.py
```

2. Watch progress in the console (and in the window title on Windows).

3. **Results** are written to `output/[timestamp]/`:
   - `Valid.txt` – all working tokens
   - `invalid.txt` – invalid tokens
   - `locked.txt` – locked accounts
   - `flagged.txt` – flagged accounts (if `flagged` is true)
   - `No Nitro.txt` – valid tokens without Nitro (if `nitro` is true)
   - `Redeemable.txt` / `Non Redeemable.txt` – by Nitro gift eligibility (if `redeemable` is true)
   - Type-based: `Unclaimed.txt`, `Email verified.txt`, `Phone verified.txt`, `Fully verified.txt`
   - `Nitro/` – Nitro tokens sorted by cooldown, period, days left, and boosts
   - `Age/` – tokens grouped by account age

## Output Folder Structure

```
output/
└── [YYYY-MM-DD HH-MM-SS]/
    ├── Valid.txt
    ├── invalid.txt
    ├── locked.txt
    ├── flagged.txt
    ├── No Nitro.txt
    ├── Redeemable.txt
    ├── Non Redeemable.txt
    ├── Unclaimed.txt
    ├── Email verified.txt
    ├── Phone verified.txt
    ├── Fully verified.txt
    ├── Nitro/
    │   ├── No Cooldown/
    │   │   ├── 1 Month/
    │   │   │   └── [X] days/
    │   │   │       └── [N] boosts.txt
    │   │   └── 3 Month/
    │   │       └── ...
    │   └── Cooldown/
    │       └── [1 Month|3 Month]/
    │           └── [X] days/
    │               └── [Xd Xhrs].txt
    └── Age/
        ├── [X] Years/
        │   └── [type].txt
        └── [X] Month/
            └── [type].txt
```

## What it Checks

- **Token validity** – Discord API (`/users/@me/guilds`, `/users/@me`)
- **Nitro** – subscription period, days left, boost slots, cooldown
- **Account age** – from Discord user ID (snowflake)
- **Verification type** – email/phone and verified flags
- **Flagged** – user flags (e.g. spammer)
- **Redeemable** – inactive subscriptions to determine Nitro gift eligibility

## Requirements

- Python 3.x
- Windows (for console title updates and “Press Enter to exit”; core checking works on other OSes)

## Want to Help?

Feel free to improve this tool via a Pull Request.

## Legal

This project is for educational purposes only. Use it in compliance with Discord’s Terms of Service and applicable laws.

## Need Help?

Join the [Discord server](https://discord.gg/razor-cap) or open an issue on GitHub.

## Star Goal ⭐

Help us reach 20 stars to unlock the next update with more token info, better speed, new features, and bug fixes.

---

<div align="center">

### 🔗 Links
- [Discord Server](https://discord.gg/razor-cap)
- [GitHub Profile](https://github.com/Ghost1503)
- [Repository](https://github.com/Ghost1503/Razor-Token-Checker)

Made with ❤️ by Ghost | © 2025 Razor Token Checker

</div>
