# API Vulnerability Attack

An API vulnerability attack happens when an attacker exploits weaknesses in an API to:

- Access data they shouldn't
- Perform unauthorized actions
- Take over accounts or systems

APIs often expose business logic and sensitive data, so when they're weak, impact is usually high.

## Objective

Each level has its own objective but the general idea is to exploit weak API implementations.

## Before Starting

During initial setup of the DVWA API module, the frontend failed to retrieve user data due to an environmental deployment issue: the API router is designed to be served from its `public/` directory, but when embedded inside DVWA this caused routing failures and 404/403 responses. To restore the intended lab functionality, I configured a dedicated Apache virtual host pointing to the API's public directory, enabled `mod_rewrite`, and aligned Apache with PHP 8.2 to satisfy Composer dependencies. This exposed the API at `http://dvwa-api.local/v2/user`, after which the frontend was updated to reference this endpoint. These changes did not introduce new functionality or vulnerabilities; they simply corrected the environment so the API operated as designed.

## LOW

First things first, since I'm dealing with APIs, I consulted the Network tab in Developer Tools:

<img width="1918" height="323" alt="image" src="https://github.com/user-attachments/assets/e97fc875-4f1a-4f4a-b9f0-02909972670d" />

And I see `v2` in the API endpoint:

<img width="601" height="391" alt="image" src="https://github.com/user-attachments/assets/3c6ba8b1-016a-4c15-97bc-82c6f17f9c18" />


`v1` is usually the first basic implementation and often has weak security or legacy logic, `v2` typically introduces bug fixes, improved validation, better authentication, and new features, while `v3+` focuses on performance optimization, stronger security controls, cleaner responses, and feature expansion — from a security perspective, older versions (especially `v1`) are more likely to contain vulnerabilities.

They keep old API versions because old clients still depend on them. Mobile apps, IoT devices, etc.

So I tried switching from `v2` to `v1`:

<img width="951" height="420" alt="Screenshot from 2026-02-14 18-59-05" src="https://github.com/user-attachments/assets/639d8710-aa47-4509-b1ec-a0758f4a3268" />


And we can see hashed password for each user, that looks like MD5 so let's crack it using CrackStation:

<img width="1054" height="437" alt="Screenshot from 2026-02-14 18-59-52" src="https://github.com/user-attachments/assets/38a33245-ea92-47b8-90ab-573e254b71aa" />


## MEDIUM

After accessing the API endpoint, I saw the existence of a `level` value, and the lab said, level 0 grants admin privileges:

<img width="923" height="240" alt="Screenshot from 2026-02-14 19-20-11" src="https://github.com/user-attachments/assets/d380d8d3-d4a8-4c63-859f-89033ce9ae2c" />


So I tried intercepting the request and set level 0 for user morph:

<img width="1553" height="573" alt="Screenshot from 2026-02-14 19-19-31" src="https://github.com/user-attachments/assets/d3a39ea5-f26b-4002-bba5-5f21111dfb19" />

And we can see the level was updated to 0:

<img width="730" height="243" alt="Screenshot from 2026-02-14 19-20-18" src="https://github.com/user-attachments/assets/8a835190-4869-42d9-a51c-4998817aa104" />
