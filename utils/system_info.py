import platform
import socket
import re
import uuid
import requests

def get_system_info():
    try:
        info = {
            'Platform': platform.system(),
            'OS Release': platform.release(),
            'OS Version': platform.version(),
            'Architecture': platform.machine(),
            'Hostname': socket.gethostname(),
            'Local IP': socket.gethostbyname(socket.gethostname()),
            'MAC Address': ':'.join(re.findall('..', '%012x' % uuid.getnode())),
            'Processor': platform.processor(),
        }

        try:
            ip_data = requests.get('https://api.ipify.org?format=json', timeout=5)
            info['Public IP'] = ip_data.json().get('ip', 'Unavailable')
        except Exception:
            info['Public IP'] = 'Unavailable'

        return info
    except Exception as e:
        print(f"Error fetching system info: {e}")
        return {}
