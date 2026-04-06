import json
import time
from binascii import hexlify, unhexlify
from dotenv import load_dotenv
from pastebin_utils import post_to_pastebin, get_from_pastebin
from crypto_utils import encrypt, decrypt, sign, verify

# Load environment variables from .env file
load_dotenv()

def encrypt_and_send(msg, name=None):
    """
    Encrypts msg, creates a signed JSON payload with a timestamp,
    then encodes the whole thing to hex before posting to Pastebin.
    """
    print("Encrypting...")
    ciphertext = encrypt(msg)
    timestamp = int(time.time())
    
    print("Signing...")
    # sign combination of timestamp and ciphertext
    hmac_tag = sign(f"{timestamp}:{ciphertext}")
    
    payload = {
        "ciphertext": ciphertext,
        "timestamp": timestamp,
        "hmac": hmac_tag
    }
    
    # JSON string -> hex encode
    json_str = json.dumps(payload)
    hex_payload = hexlify(json_str.encode()).decode()
    
    print("Posting to Pastebin...")
    return post_to_pastebin(hex_payload, name=name)

def decrypt_and_read(paste_key):
    """
    Fetches hex payload from Pastebin, decoes it, parses JSON,
    verifies HMAC/timestamp, and finally decrypts the message.
    """
    print("Fetching from Pastebin...")
    hex_payload = get_from_pastebin(paste_key)
    if not hex_payload or hex_payload.startswith("Bad API request"):
        return f"Error: {hex_payload}"
        
    try:
        # Hex decode -> JSON parse
        json_str = unhexlify(hex_payload).decode()
        payload = json.loads(json_str)
        
        ciphertext = payload["ciphertext"]
        timestamp = payload["timestamp"]
        hmac_tag = payload["hmac"]
        
        print("Verifying timestamp...")
        # 1. Verify Timestamp (Replay Attack Prevention)
        max_age = 600 # 10 minutes
        if abs(int(time.time()) - timestamp) > max_age:
            return "Error: Paste has expired (potential replay attack)."

        print("Verifying HMAC signature...")    
        # 2. Verify HMAC Signature
        if not verify(f"{timestamp}:{ciphertext}", hmac_tag):
            return "Error: HMAC verification failed! Data may be tampered."
        
        print("Decrypting...")
        # 3. Decrypt
        return decrypt(ciphertext)
        
    except Exception as e:
        return f"Error processing payload: {str(e)}"


def main():
    print("--- Safebin: Pastebin CLI ---")
    print("1. Post a paste")
    print("2. Read a paste")
    
    choice = input("\nEnter choice (1 or 2): ").strip()
    
    if choice == '1':
        content_str = input("\nEnter the content you want to paste: ").strip()

        if not content_str:
            print("Error: No content to paste.")
            return

        name = input("Enter a title for your paste (optional): ").strip() or None
        
        print("\n")
        result = encrypt_and_send(content_str, name=name)
        print(f"\nResult: {result}")
        
    elif choice == '2':
        paste_key = input("\nEnter the Pastebin key (ID): ").strip()
        if not paste_key:
            print("Error: No paste key provided.")
            return
            
        print("\n")
        content = decrypt_and_read(paste_key)
        print("\n--- Paste Content ---")
        print(content)
        print("---------------------")
        
    else:
        print("Invalid choice.")

if __name__ == "__main__":
    main()
