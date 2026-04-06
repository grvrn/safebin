# Safebin

Safebin is a secure Command Line Interface (CLI) tool for storing and retrieving text on Pastebin. It prioritizes privacy and security by implementing robust cryptographic measures before any data leaves your machine.

## Features

- **Secure Encryption:** Uses **AES-256-CBC** with PKCS7 padding to ensure your data is unreadable to anyone without the key.
- **Data Integrity:** Implements an **Encrypt-then-MAC** pattern using **HMAC-SHA256** to prevent tampering and chosen-ciphertext attacks.
- **Replay Protection:** Includes signed timestamps in every payload to prevent older messages from being replayed.
- **Privacy First:** Data is encapsulated in a JSON structure and hex-encoded before being sent to Pastebin.
- **Interactive CLI:** Simple menu-driven interface for easy operation.

## Prerequisites

- Python 3.7+
- A Pastebin Developer API Key ([Get one here](https://pastebin.com/doc_api#1))

## Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd safebin
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   If there is an error while installing cryptography, you can try installing those packages manually by running:
   ```bash
   pip install cryptography pyopenssl
   ```

3. **Configure the environment:**
   Create a `.env` file in the root directory (or update the existing one):
   ```ini
   PASTEBIN_API_DEV_KEY="your_pastebin_api_key"
   AES_KEY="your_32_byte_hex_aes_key"
   HMAC_KEY="your_32_byte_hex_hmac_key"
   ```
   *Note: Keys should be 64-character hex strings (32 bytes).*

## Usage

Run the main application:

```bash
chmod +x main.py
python main.py
```

### Options:

1. **Post a paste:** 
   - Enter your message.
   - (Optional) Enter a title.
   - The tool will encrypt, sign, and upload the payload, returning the Pastebin URL.

2. **Read a paste:**
   - Enter the Pastebin key (e.g., `83u757s` from `https://pastebin.com/83u757s`).
   - The tool will fetch, verify the signature/timestamp, and decrypt the message.

## Security Architecture

Safebin follows industry best practices for secure messaging:

1. **Encryption:** `AES-CBC` provides confidentiality.
2. **Authentication:** `HMAC-SHA256` covers both the `ciphertext` and the `timestamp`.
3. **Encapsulation:** The final payload follows this structure:
   `hex(json({"ciphertext": "...", "timestamp": 1234..., "hmac": "..."}))`
4. **Verification:** Any modification to the Pastebin content will result in an HMAC verification failure, and any message older than 10 minutes is rejected by default to prevent replay.

## License

MIT
