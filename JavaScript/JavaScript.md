# JavaScript Attacks

JavaScript attacks are client-side attacks where an attacker injects or manipulates JavaScript to run malicious code in a victim's browser.

## About (Said by DVWA Creators)

The attacks in this section are designed to help you learn about how JavaScript is used in the browser and how it can be manipulated. The attacks could be carried out by just analyzing network traffic, but that isn't the point and it would also probably be a lot harder.

## Objective

Simply submit the phrase "success" to win the level. Obviously, it isn't quite that easy, each level implements different protection mechanisms, the JavaScript included in the pages has to be analyzed and then manipulated to bypass the protections.

## LOW

So basically, it's saying enter the word success to win, but when trying it, we got "Invalid token":

<img width="761" height="205" alt="Screenshot from 2026-02-10 17-10-41" src="https://github.com/user-attachments/assets/2b917ee9-ccd4-4409-b4b0-dee48e9e8779" />

So I checked the source code and looked for the word token:

<img width="1812" height="290" alt="Screenshot from 2026-02-10 17-17-06" src="https://github.com/user-attachments/assets/4c7675a7-8046-48c8-8327-8d199a804427" />


The important part is:
```javascript
function generate_token() {
    var phrase = document.getElementById("phrase").value;
    document.getElementById("token").value = md5(rot13(phrase));
}
```

So the token should be equal to: the MD5 of ROT13("success")

So let's first ROT13("success") then apply MD5 on it using CyberChef:

<img width="1503" height="602" alt="Screenshot from 2026-02-10 17-35-14" src="https://github.com/user-attachments/assets/b5f00d39-8f9a-433e-b01e-13763ee9fc63" />


Then let's use it as our token:

<img width="1543" height="821" alt="Screenshot from 2026-02-10 17-33-50" src="https://github.com/user-attachments/assets/39be489f-08b1-428c-a14c-bc0650468439" />


And we solved it.

## MEDIUM

First let's start checking the source code:

<img width="1032" height="136" alt="Screenshot from 2026-02-10 17-39-50" src="https://github.com/user-attachments/assets/3786f12a-0074-46f6-9f0e-c5eda0242562" />


We can see that `medium.js` is responsible for client-side token generation and validation logic before the form is submitted.

So let's see that `medium.js`:

<img width="1366" height="142" alt="image" src="https://github.com/user-attachments/assets/33081329-252b-4421-b67d-12295bb4ddb8" />


The function `do_something` is for reversing an input.

And the function `do_elsesomething` is for token generation: `token = reverse("XX" + phrase + "XX")`

Something like: `token = XXsseccusXX`

So let's try, first let's capture the request and change the token value:

<img width="1552" height="661" alt="Screenshot from 2026-02-10 17-48-21" src="https://github.com/user-attachments/assets/d51933e5-b885-40d3-9048-b850e878f004" />

## HIGH

First things first, let's see that `high.js` script:

<img width="1920" height="922" alt="Screenshot from 2026-02-10 17-49-42" src="https://github.com/user-attachments/assets/e1a1291f-36e2-4a9a-8544-77d998dde928" />


And it is an obfuscated JavaScript, so let's use a JavaScript Deobfuscator to read it.

I used https://deobfuscate.io/ for that.

<img width="1318" height="787" alt="Screenshot from 2026-02-10 17-52-50" src="https://github.com/user-attachments/assets/1bab6f58-6740-40cc-9f62-399dcbf7ab51" />


Basically this code does:

1. They reverse input like before and add XX: `"XX" + reverse(success)` → `XXsseccus`
2. And they apply SHA256 on it: `SHA256(XXsseccus)`
3. Then they append ZZ after hashing: `SHA256(XXsseccus) + "ZZ"`
4. And they SHA256 all of it: `SHA256(SHA256(XXsseccus) + "ZZ")`

So let's do this using CyberChef:

First let's SHA256 `XXsseccus`:

<img width="1506" height="634" alt="Screenshot from 2026-02-10 18-05-51" src="https://github.com/user-attachments/assets/ba80c484-a0d7-45aa-8da0-696ef4baf49a" />


Then append ZZ on that hash, and apply SHA256 again:

<img width="1506" height="634" alt="Screenshot from 2026-02-10 18-06-15" src="https://github.com/user-attachments/assets/bc1efe91-ac7d-4d1c-a98b-822d79b0cc21" />


And let's replace it on token:

<img width="1537" height="701" alt="Screenshot from 2026-02-10 18-06-25" src="https://github.com/user-attachments/assets/17021e4e-b8ad-418f-a42b-7c5ceb03d1e9" />
