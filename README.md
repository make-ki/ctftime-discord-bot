# CtfTime Discord Bot

A Discord bot that fetches upcoming Capture The Flag (CTF) events from CTFtime and posts them in a designated Discord channel.

## Features

- Fetches and displays the latest CTF events.
- Sends weekly announcements for upcoming CTFs.
- Uses embeds to format event details.
- Includes event logo, start time, end time, and prizes.

## File Structure

```
ctftime-discord-bot/
│── ctf_bot.py           # Main bot script
│── requirements.txt    # Python dependencies
│── .env                # Environment variables (DO NOT SHARE)
│── README.md           # Project documentation
│── .gitignore          # Ignoring sensitive files
```

## Setup Instructions

### Prerequisites

- Python 3.8+
- A Discord bot token
- `nextcord` library
- A happy life

### Installation

1. Clone the repository:
   ```sh
   https://github.com/make-ki/ctftime-discord-bot
   cd ctfime-discord-bot
   ```
2. Create a virtual environment (Recommended though Optional):
   ```sh
   python3 -m venv myenv
   source myenv/bin/activate  # On Windows, use myenv\Scripts\activate
   ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
4. Create a `.env` file and add (or hardcode if running locally):
   ```env
   TOKEN = your_discord_bot_token
   CTFTIME_API = ctftime_v1_events_api
   CHANNEL_ID = discord_channel_to_send_message
   CTF_ROLE_ID = discord_role_you_want_to_ping
   ```

### Running the Bot

```sh
python ctf_bot.py
```

## Deployment

- Use Railway, Fly.io, or a free VPS for 24/7 hosting.

## Security Considerations

- **DO NOT** hardcode tokens in the script.
- Use `.env` for secrets and add `.env` to `.gitignore`.
- Rotate your tokens if exposed.

## License

MIT License

## Contributions

Feel free to submit pull requests or issues. I am not very smart so I won't mind. I will be adding more features to it in upcoming weeks.

---

Maintained by make-ki

