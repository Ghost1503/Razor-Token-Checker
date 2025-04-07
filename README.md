# Razor Token Checker

A fast and powerful Discord token checker that helps you check and sort your tokens easily.

## What it Does

- 🔍 **Token Checking**
  - Checks if tokens are valid
  - Finds Nitro tokens
  - Checks for available boosts
  - Shows how old accounts are
  - Checks if accounts are verified
  - Finds redeemable tokens
  - Spots flagged accounts

- ⚡ **Speed & Performance**
  - Uses multiple threads for faster checking
  - Works with proxies
  - Handles rate limits automatically
  - Checks many tokens at once

- 📊 **Sorting & Organization**
  - Keeps everything neat and organized
  - Saves tokens in different files based on type
  - Groups tokens by account age
  - Sorts Nitro tokens by type
  - Tracks available boosts

- 🎨 **Easy to Use**
  - Shows stats in real-time
  - Tracks progress
  - Shows final results

## How to Get Started

1. Download the tool:
```bash
git clone https://github.com/ghost1545/razor-token-checker.git
cd razor-token-checker
```

2. Install what you need:
```bash
pip install -r requirements.txt
```

3. Set it up:
   - Put your tokens in `data/tokens.txt`
   - Add proxies to `data/proxies.txt` (if you want)
   - Set up `data/config.toml`
   - Check `data/settings.json`

## Settings

### config.toml
```toml
[main]
threads = 10
proxyless = false
```

### settings.json
```json
{
    "flagged": true,
    "type": true,
    "age": true,
    "nitro": true
}
```

## How to Use

1. Run the checker:
```bash
python main.py
```

2. Watch the progress in your console

3. Find your results in `output/[timestamp]`:
   - `valid.txt` - Working tokens
   - `invalid.txt` - Dead tokens
   - `locked.txt` - Locked tokens
   - `flagged.txt` - Flagged tokens
   - `Nitro/` - Tokens with Nitro
   - `Age/` - Tokens sorted by age

## Where to Find Results

```
output/
├── [timestamp]/
│   ├── valid.txt
│   ├── invalid.txt
│   ├── locked.txt
│   ├── flagged.txt
│   ├── Nitro/
│   │   ├── No Cooldown/
│   │   └── Cooldown/
│   ├── Age/
│   │   ├── [X] Years/
│   │   └── [X] Month/
```

## What it Checks

### Token Info
- Makes sure tokens work with Discord
- Finds Nitro and how long it lasts
- Shows how many boosts are available
- Tells you how old accounts are
- Checks if accounts are verified
- Finds tokens you can redeem
- Spots flagged accounts

### Speed Features
- You can set how many threads to use
- Works with proxies to avoid limits
- Handles rate limits by itself
- Checks tokens quickly

### How it Saves Results
- Makes a new folder with the date and time
- Saves tokens in the right places
- Keeps all the info about each token
- Makes it easy to find what you need

## Want to Help?

Feel free to help improve this tool! Just send a Pull Request.

## Legal Stuff

This is just for learning. Make sure you follow Discord's rules and the law.

## Need Help?

Join our [Discord server](https://discord.gg/razorcap) or open an issue here.

## Star Goal ⭐

Help us reach 20 stars to unlock the next update with:
- More token info
- Better speed
- New features
- Bug fixes

## Contributors

<div align="center">
  
  ### Our Amazing Team
  
  <a href="https://github.com/ghost1545/razor-token-checker/graphs/contributors">
    <img src="https://contrib.rocks/image?repo=ghost1545/razor-token-checker" />
  </a>
  
  ### Join Our Team!
  
  Want to be a contributor? [Join our Discord](https://discord.gg/razorcap) and let us know!
  
</div>

## Credits

<div align="center">
  
  ### Made with ❤️ by Ghost
  
  [![Discord](https://img.shields.io/discord/922631391806652467?color=7289da&label=Discord&style=for-the-badge)](https://discord.gg/razor-boost)
  [![GitHub](https://img.shields.io/github/followers/ghost1545?label=Follow&style=for-the-badge)](https://github.com/ghost1545)
  
</div>
