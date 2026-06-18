import argparse
import uvicorn

from dotenv import load_dotenv
from fastapi import FastAPI

from service import encrypt_and_send, decrypt_and_read
from api import router

# Load environment variables from .env file
load_dotenv()

def main():
    parser = argparse.ArgumentParser(description="Safebin: Secure Pastebin CLI")
    
    parser.add_argument("-c", "--cli", action="store_true", help="Run in command line mode")

    args = parser.parse_args()

    if args.cli:
        print("--- Safebin: Secure Pastebin CLI ---")
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
    else:
        app = FastAPI(title="Safebin API")
        app.include_router(router)

        @app.get("/")
        async def root():
            return {"message": "Welcome to Safebin"}

        uvicorn.run(app, host="127.0.0.1", port=8000)

if __name__ == "__main__":
    main()
