# Brute Force Attack 

## What is Brute Force Attack

A brute force attack is when an attacker repeatedly tries many username and password combinations until one works.
It relies on automation and persistence rather than skill, hoping weak credentials will eventually crack.

---

## LOW Level

No protection at all.

<img width="1920" height="918" alt="Screenshot from 2026-01-26 13-44-43" src="https://github.com/user-attachments/assets/36086b12-7c64-4048-8893-d0119a6a78b2" />



### Command
```bash
hydra -l admin \
-P /home/abdessamad/Desktop/cyber/SecLists/Passwords/Common-Credentials/10k-most-common.txt \
localhost -s 8000 http-get-form \
```

<img width="1920" height="317" alt="Screenshot from 2026-01-26 13-54-07" src="https://github.com/user-attachments/assets/e8d3c33d-5b6b-4c38-8aad-bbeee37c0c84" />

---

## Medium Level

This stage adds a sleep on the failed login screen. This mean when you login incorrectly, there will be an extra two second wait before the page is visible. This will only slow down the amount of requests which can be processed a minute, making it longer to brute force.

even using parallel requests failed. so this will force us to use a well crafted and small wordlist , or use another method like session rotation.

for that: I made a python script with the help of chatgpt: I used a list of passwords just for prove.

### Process

For each password in the list:

1. Create a new HTTP session (simulate a new browser).
2. Request the login page to obtain a new PHP sessionid and CSRF token.
3. Authenticate to DVWA using creds (brute force is inside it)
4. Request the security configuration page.
5. Extract a new CSRF token for the security page.
6. Change the DVWA security level to medium (by default it's low)
7. Access the brute-force vulnerability page.
8. Send a brute-force request using the current password.
9. Analyze the response to determine success or failure.
10. If successful, stop the process; otherwise, discard the session and continue.

<img width="1919" height="491" alt="Screenshot from 2026-01-27 17-26-09" src="https://github.com/user-attachments/assets/0b300a19-fb57-4e8f-acac-f3ea83b14d73" />

this bypasses the 2s waits for every single req

---

## Hard Level
### CSRF token
A CSRF token is a unique, secret value added to a request to make sure it really comes from the user and not a malicious website.
It helps protect applications from unauthorized actions performed without the user’s consent.


I added a step for csrf extraction

### Workflow

**Request Brute-Force Page**
- Send GET request to brute endpoint
- Receive fresh CSRF token bound to session

**Extract CSRF Token**
- Parse HTML response
- Store user_token for current attempt

**Submit Brute Attempt**
- Send login request with:
  - username
  - candidate password
  - CSRF token

**Validate Response**
- Analyze server response
- Detect success or failure

**Repeat Until Success or Exhaustion**
- Discard used token
- Fetch a new token for next attempt

<img width="1920" height="332" alt="Screenshot from 2026-01-27 18-48-58" src="https://github.com/user-attachments/assets/4cba926a-695f-48c5-b626-888da479b36a" />



<img width="586" height="226" alt="image" src="https://github.com/user-attachments/assets/f9848365-ebcd-4990-af24-d019cc270cd7" />


