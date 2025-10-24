import os
from utils.chrome_data_viewer import extract_chrome_data
from utils.clipboard_viewer import get_clipboard_content
from utils.system_info import get_system_info

def main():
    print("=" * 60)
    print(" USER DATA INSPECTOR - Local Privacy Awareness Tool ")
    print("=" * 60)

    consent = input("\nThis tool will read your local Chrome data, clipboard, and system info.\nUse this only on your own system. Continue? (y/n): ").strip().lower()
    if consent != 'y':
        print("Operation cancelled by user.")
        return

    print("\n[+] Extracting Chrome saved logins...")
    credentials = extract_chrome_data()
    if credentials:
        for cred in credentials:
            print(f"\nProfile: {cred['profile']}")
            print(f"URL: {cred['url']}")
            print(f"Username: {cred['username']}")
            print(f"Password: {cred['password']}")
    else:
        print("No credentials found or decryption failed.")

    print("\n[+] Reading clipboard content...")
    clipboard = get_clipboard_content()
    if clipboard:
        print(f"Clipboard Content:\n{clipboard}")
    else:
        print("No clipboard data found.")

    print("\n[+] Gathering system information...")
    sys_info = get_system_info()
    for k, v in sys_info.items():
        print(f"{k}: {v}")

    print("\nCompleted. This data is only shown locally and not transmitted anywhere.")
    print("=" * 60)

if __name__ == "__main__":
    main()
