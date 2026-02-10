# Open HTTP Redirect Vulnerability

An Open HTTP Redirect vulnerability happens when a website redirects users to any URL provided by user input without proper validation.

Attackers abuse this to send victims to malicious sites, while the link still looks like it belongs to a trusted domain.

Something like: `https://example.com/redirect?url=https://attacker-site.com`

## Objective

Abuse the redirect page to move the user off the DVWA site or onto a different page on the site than expected.

## LOW

The feature provides two links to some famous hacker quotes.

<img width="684" height="195" alt="Screenshot from 2026-02-10 19-59-24" src="https://github.com/user-attachments/assets/24286cda-e47e-4a16-ab60-00222978ed69" />

When clicking the first one: its path is `http://127.0.0.1/dvwa/vulnerabilities/open_redirect/source/info.php?id=1`

When I checked the source code:

<img width="675" height="175" alt="Screenshot from 2026-02-10 20-02-09" src="https://github.com/user-attachments/assets/d0e2363c-e917-4dc7-a80b-863308926b49" />


I could see a redirect parameter: `low.php?redirect=info.php?id=1`

So let's try to abuse it, let's replace `info.php` with something like: `https://google.com`

<img width="1549" height="455" alt="Screenshot from 2026-02-10 20-04-37" src="https://github.com/user-attachments/assets/23bdcbed-8461-448f-8f2c-823fd8de08f9" />


We can see it's redirecting us, let's follow redirection:

<img width="1557" height="744" alt="Screenshot from 2026-02-10 20-05-27" src="https://github.com/user-attachments/assets/343b74f9-5f99-4c6a-9e76-c023dde15386" />


## MEDIUM

Let's check the source code for this one too:

<img width="1424" height="244" alt="Screenshot from 2026-02-10 20-07-17" src="https://github.com/user-attachments/assets/1ecf44c0-3a18-495b-8a0d-2582bd18973b" />

And let's try the same redirection abuse we used in LOW:

<img width="859" height="93" alt="Screenshot from 2026-02-10 20-08-11" src="https://github.com/user-attachments/assets/dbf5c6d8-b88d-4f54-9556-f704c3c64385" />


So probably they are checking for strings like: `http://` or `https://`

I thought about URL encoding:

<img width="1542" height="430" alt="Screenshot from 2026-02-10 20-12-07" src="https://github.com/user-attachments/assets/7d21cc20-6b3f-4526-92ef-bbe949cb7ea8" />


But it didn't work, so it's not a literal check for `http://` or `https://`

I was searching in PayloadsAllTheThings:

https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Open%20Redirect/README.md

And I found this:

<img width="1068" height="126" alt="Screenshot from 2026-02-10 20-19-25" src="https://github.com/user-attachments/assets/cb00bd98-c162-42f0-be26-93db226ecab0" />


And it works because browsers automatically add the current scheme (http or https), it's called protocol-relative URL.

So let's try it:

<img width="1543" height="509" alt="Screenshot from 2026-02-10 20-21-38" src="https://github.com/user-attachments/assets/0e36ec4b-8f21-4412-94d0-9428838d1f0f" />


And it's redirecting us to google.com:

<img width="1555" height="693" alt="Screenshot from 2026-02-10 20-22-28" src="https://github.com/user-attachments/assets/8b42000e-d9f9-4012-a621-41cbc446ecf1" />


## HIGH

Straight to the point, I tried `//google.com` redirection:

<img width="765" height="86" alt="Screenshot from 2026-02-10 20-23-46" src="https://github.com/user-attachments/assets/1d15c3cb-d69c-45b5-bafd-7b11fe2da303" />


So basically they are checking the presence of `info.php` to ensure something like `http://127.0.0.1/dvwa/vulnerabilities/open_redirect/source/info.php?id=1` or `id=2`.

So we should include it in our redirection, just for bypassing the check.

So we can use something like: `source/high.php?redirect=//google.com/?a=info.php`

`?a=info.php` is just a query parameter, external sites don't care about it.

<img width="1561" height="573" alt="Screenshot from 2026-02-10 20-33-01" src="https://github.com/user-attachments/assets/8291dcdc-7937-4c94-9c69-ae2acc7e9d30" />
