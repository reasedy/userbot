
-----
markdown
# 🕵️ Telegram Userbot

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python)
![Pyrogram](https://img.shields.io/badge/Pyrogram-Latest-yellow?style=for-the-badge&logo=telegram)
![Status](https://img.shields.io/badge/Status-Active-success?style=for-the-badge)

A powerful, lightweight **Telegram Userbot** built with Pyrogram. It automates your personal account, caches deleted messages, saves self-destructing media, and provides ghost-tagging capabilities.

---

## ⚡ Features

* **🔥 TTL Media Saver:** Automatically downloads and saves self-destructing photos/videos to your "Saved Messages" before they disappear.
* **🗑️ Anti-Delete (Spy Mode):** Detects when someone deletes a message in PMs or specific groups and forwards the deleted content to your "Saved Messages".
* **👻 Ghost Mention:** Tag users (or everyone) without triggering a visible notification link.
* **💤 Smart AFK:** Auto-reply system when you are away.
* **⌨️ Typewriter Effect:** Animate your text messages with a retro typing style.
* **💩 Auto-React:** Automatically react with emojis to specific users' messages (troll mode).

---

## 🛠️ Installation & Setup

### 1. Clone the repository
```bash
git clone [https://github.com/reasedy/userbot.git](https://github.com/reasedy/userbot.git)
cd userbot
````

### 2\. Install dependencies

```bash
pip install -r requirements.txt
```

### 3\. Configure Environment Variables

Create a `.env` file in the root directory. **Do not upload this file to GitHub\!**

```ini
API_ID=12345678
API_HASH=your_api_hash_here
```

> *You can get your `API_ID` and `API_HASH` from [my.telegram.org](https://my.telegram.org).*

### 4\. Run the bot

```bash
python main.py
```

-----

## 🎮 Command List

| Command | Description | Example |
| :--- | :--- | :--- |
| `.type [text]` | Sends text with a typewriter animation. | `.type Hello World` |
| `.afk [reason]` | Sets your status to AFK. Auto-replies to DMs. | `.afk Sleeping` |
| `.unafk` | Disables AFK mode. | `.unafk` |
| `.tag [id]` | Ghost-tags a user by ID (invisible link). | `.tag 12345678` |
| `.all [text]` | Ghost-tags up to 50 active members in the chat. | `.all Wake up!` |
| `.del [n]` | Purges your last `n` messages. | `.del 10` |
| `.r` | **Reply only.** Toggles auto-reaction (💩) on the user. | Reply to user with `.r` |
| `.id` | Shows the current Chat ID. | `.id` |

-----

## ⚠️ Disclaimer

This project is for **educational purposes only**.
Using userbots may violate Telegram's Terms of Service if abused (e.g., spamming). The developer is not responsible for any account bans or restrictions. Use responsibly.

-----

### 👨‍💻 Author

**Raymon** — [GitHub Profile](https://www.google.com/search?q=https://github.com/reasedy)


