# ReceiptAnalyzer

A Telegram bot that analyzes receipts and returns different information about them.
The initial idea was to create a database to view all the spends and to have a better understanding of the money flow. (Maybe to use this in a budgeting app)

The ReceiptAnalyzer bot is a Python-based Telegram bot that analyzes QR code images from receipts to extract detailed transaction data. This tool leverages OpenCV for image processing and integrates with the Sistemul Informațional Automatizat "Monitorizarea Electronică a Vânzărilor" ([MEV](https://mev.sfs.md/)) system at <https://mev.sfs.md/receipt-verifier> to verify and scrape receipt details.

## Features

- Telegram Bot Integration: Interact with the analyzer directly through Telegram for convenience.
- QR Code Processing: Utilizes OpenCV to process and decode QR codes from receipt images.
- Data Verification: Retrieves and scrapes detailed transaction data (e.g., receipt number, date, amount) from the official MEV receipt verification site.
- Automated Workflow: Provides a seamless, user-friendly experience for verifying and analyzing fiscal receipts.

## Instalation & Configuration

- Install the dependencies with `pip install -r requirements.txt`
- Create a bot or use an existing one in Telegram and get the token.
- Put the token in the `.env` file ***and only in it***. `.env` file should look like this: `KEY=VALUE`
- Use it in the vscode with a workspace so that the environment variables are loaded.

## Usage

```bash
git clone https://github.com/DumitruVartic/ReceiptAnalyzer.git
cd receipt-analyzer-bot
pip install -r requirements.txt
```

Get token for telegram bot, Put the token in the `.env` file ***and only in it***. `.env` file should look like this: `KEY=VALUE`

Run it

```bash
python main.py
```
