# Content Security Policy (CSP) Vulnerability

CSP is a browser security feature that tells the browser which sources are allowed to load content (JS, CSS, images, etc.).

It's mainly used to reduce XSS and data injection attacks.

A CSP vulnerability happens when the policy is misconfigured or too permissive, allowing attackers to bypass CSP and execute malicious code.

## Objective

Bypass Content Security Policy (CSP) and execute JavaScript in the page.

## LOW

First things first, this lab provides a feature to execute external JS scripts.

<img width="759" height="211" alt="Screenshot from 2026-02-07 19-50-38" src="https://github.com/user-attachments/assets/3311cc73-302a-405c-80cc-b754a8bba419" />

But we should check the CSP policy, so by clicking `Ctrl + Shift + I`, then going to the Network tab and checking `csp/`, we can see pastebin, example.com, and code.jquery.com...

<img width="1799" height="212" alt="Screenshot from 2026-02-07 19-52-28" src="https://github.com/user-attachments/assets/7805087f-43b6-4f64-8b4d-f5a20cba3f4d" />


So I tried to create a paste on Pastebin containing a very simple JS:
```javascript
alert("CSP BYPASS WORKED");
```

<img width="523" height="102" alt="Screenshot from 2026-02-07 20-02-17" src="https://github.com/user-attachments/assets/a4d0aae5-3c4e-4b43-9b2b-e4dea6b4b824" />


And I used the raw URL as an input, but nothing happened.

I checked the Network tab to see what was happening, and I found that the script was loaded, but it was not executed.

And this is because Pastebin serves files as text, not as JS:
```
Content-Type: text/plain
```

<img width="1231" height="616" alt="Screenshot from 2026-02-07 20-15-57" src="https://github.com/user-attachments/assets/221a711d-b62f-44cd-bb5a-e271fcbdab17" />


We can also see:
```
X-Content-Type-Options: nosniff
```

which means the browser is FORBIDDEN from guessing the type.

This is called **MIME Type Blocking** (modern browsers do it by default).

Basically, the CSP bypass is working, because the JS file was loaded, but due to this MIME type blocking, it can't be executed.

I tried GitHub Gist, but since it's not CSP whitelisted, it didn't work (it was obvious it wouldn't, but GitHub Gist serves files with their real extensions, not as text, so it was worth the try):

<img width="1915" height="543" alt="Screenshot from 2026-02-07 20-21-11" src="https://github.com/user-attachments/assets/ad78be92-ca22-49b5-b066-1883dd9fc6e7" />

Then I tried loading a code.jquery.com script like:
```
https://code.jquery.com/jquery-3.6.0.min.js
```

And by checking the Network tab and then the Response, I could see the JS code there.

So I think there is an issue with the lab — maybe it's outdated, because we can't use Pastebin anymore for this purpose.

## MEDIUM

After examining the `csp/`, there is a nonce. A nonce (number used once) is a random value generated per page load.

<img width="1907" height="350" alt="Screenshot from 2026-02-09 04-38-33" src="https://github.com/user-attachments/assets/1a001af4-ac63-47d4-b08b-ed3c78587aea" />


Basically, only scripts that contain this exact nonce are allowed to run.

So our script should contain that nonce, something like:
```html
<script nonce="TmV2ZXIgZ29pbmcgdG8gZ2l2ZSB5b3UgdXA="> alert(1); </script>
```

But since Pastebin isn't working as expected, there is nothing much I can do here.

## HIGH

I started by capturing the request via Burp Suite:

<img width="1547" height="716" alt="Screenshot from 2026-02-10 16-44-03" src="https://github.com/user-attachments/assets/af1dc9fa-5252-41cc-8aa7-a2b46242a1fa" />

The interesting thing is the server is calling a function named `solveSum` to calculate the sum.

So maybe we can abuse that callback function somehow.

First things first, let's understand this situation:

JSONP (JSON with Padding) is an old technique used to bypass the browser's Same-Origin Policy by abusing how `<script>` tags work.

So basically our JSONP allows arbitrary JavaScript execution if the callback parameter is not strictly validated.

Let's try injecting something like `callback=alert("BE-CAREFUL");`, by intercepting the request and forwarding it:

<img width="1920" height="923" alt="Screenshot from 2026-02-10 16-51-32" src="https://github.com/user-attachments/assets/7037be4b-5753-41a6-8546-196dff220306" />
