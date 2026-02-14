# Cryptography Vulnerability

A cryptography vulnerability is a weakness in how encryption is designed, implemented, configured, or used, allowing attackers to read, modify, or forge protected data.

## Objective

Each level has its own objective but the general idea is to exploit weak cryptographic implementations.

## LOW

The feature allows to encode and decode messages, in order to ensure a secure communication, so only sender and receiver should encode and decode the messages.

<img width="677" height="545" alt="Screenshot from 2026-02-10 20-40-48" src="https://github.com/user-attachments/assets/1a3d0375-3ef5-4892-bb91-cb111835bcd4" />

First let's see what type of encoding is this.

Reminder: Decoding hides data temporarily (reversible), hashing destroys it into a fixed fingerprint (not reversible).

From first sight: this `Lg4WGlQZChhSFBYSEB8bBQtPGxdNQSwEHREOAQY=` looks like Base64. But when I tried decoding it:

<img width="998" height="582" alt="Screenshot from 2026-02-10 20-45-16" src="https://github.com/user-attachments/assets/cfe65d62-5f9c-4f8a-a656-2e776d40da1d" />

Using magic function in CyberChef, it confirms it could be Base64:

<img width="1493" height="665" alt="Screenshot from 2026-02-10 20-45-59" src="https://github.com/user-attachments/assets/ab8c09ed-be3f-4524-a5ed-2bf58b477d53" />


So maybe it's not an ordinary Base64, maybe it's combined with something else.

Let's try something classic, like Base64 with XOR:

<img width="1497" height="657" alt="Screenshot from 2026-02-10 21-06-59" src="https://github.com/user-attachments/assets/e458ea9e-aff4-49ea-a5d7-39d817135527" />


XOR hides data by flipping bits using a key, and the same key reveals it.


So the key is repetition of `wachtwoord`:

<img width="1497" height="657" alt="Screenshot from 2026-02-10 21-08-23" src="https://github.com/user-attachments/assets/784fa5aa-d8d8-4cce-b8eb-046a3edb1632" />


Using that key we can decode or encode whatever we like.

## MEDIUM

What we have here is three encrypted session tokens, encrypted with AES-128-ECB.

The plaintext format is JSON, something like this:
```json
{
  "user": "...",
  "ex": ...,
  "level": "...",
  "bio": "..."
}
```

We can't decrypt anything, but we can change blocks, because each block is represented as 32 chars (16 bytes).

So I started by putting all the sessions together and analyzing them:

<img width="457" height="429" alt="Screenshot from 2026-02-14 16-13-52" src="https://github.com/user-attachments/assets/31b9b412-ac8f-4db2-b937-2f70f5a67471" />

And for the user Sweep, their session is expired, so I replaced their expiration block with the one from user Soo. And for gaining higher privileges, I replaced their level with the level block of user Sooty (admin).

<img width="903" height="838" alt="image" src="https://github.com/user-attachments/assets/f0d1b83c-7882-4388-ac76-361437b7b83b" />


## HIGH

<img width="702" height="816" alt="Screenshot from 2026-02-14 16-14-26" src="https://github.com/user-attachments/assets/c62790ba-0419-4d24-ab87-fcb7820c67b9" />

Let's start with analyzing the token:
```json
{
  "token": "PhQwGVA3q+T2mT+L3Pe5Vg==",
  "iv": "MTIzNDU2NzgxMjM0NTY3OA=="
}
```

The token seems like one block of AES (when decoded from Base64 it results in 16 bytes).

The IV when decoded from Base64 it gives: `1234567812345678`, this is 16 bytes too.

This format strongly suggests: **AES-CBC** because of the existence of an IV.

Let's start with understanding what we have:

### CBC (Cipher Block Chaining)

An encryption mode where each plaintext block is XORed with the previous ciphertext block before being encrypted. This "chains" blocks together so patterns don't repeat.

### AES-CBC

AES (the cipher) + CBC (the mode).

AES encrypts data block-by-block, and CBC links those blocks together using chaining.

### IV (Initialization Vector)

A random 16-byte starting value used for the first block in CBC.

**Purpose**: Make the same plaintext encrypt differently each time.

IV is not secret, but must be random/unique.

After some researches I found we can use a famous attack with the AES-CBC encryption, it is **Padding Oracle Attack**. In simple terms:

Padding Oracle Attack is when an attacker uses a server's "padding valid / invalid" responses to decrypt or modify AES-CBC encrypted data without knowing the key, one byte at a time.

So basically you keep tweaking ciphertext and use padding errors as hints to reveal the plaintext.

The help section provided a script for doing this, so let's use it.

By running:
```bash
php oracle_attack.php --iv="MTIzNDU2NzgxMjM0NTY3OA==" --token="PhQwGVA3q+T2mT+L3Pe5Vg==" --url="http://localhost/dvwa/vulnerabilities/cryptography/source/check_token_high.php" > decrypt.txt
```

<img width="1151" height="434" alt="Screenshot from 2026-02-14 17-09-15" src="https://github.com/user-attachments/assets/c1440a64-91b2-47bb-ace1-9d85e0248306" />


And I used the resulted token and pasted it in DVWA:

<img width="903" height="838" alt="Screenshot from 2026-02-14 17-10-48" src="https://github.com/user-attachments/assets/cc084a58-c411-4a80-918e-7fa02cf1e1eb" />
