# File Inclusion Vulnerability

A File Inclusion vulnerability happens when a web application includes files based on user input without proper validation.

Attackers can abuse this to load unauthorized files, sometimes leading to data disclosure or remote code execution.

## Types of File Inclusion

### Local File Inclusion (LFI)

The attacker includes files already on the server.

### Remote File Inclusion (RFI)

The attacker includes a remote file from another server (if enabled).

## LOW

### LFI

There is no security measures, so doors are open.

<img width="1920" height="959" alt="Screenshot from 2026-02-01 18-26-47" src="https://github.com/user-attachments/assets/2a6137e7-7610-41a2-a0eb-50ea497c4dc5" />


We can directly access local files that exist on the server.

### RFI

I used a PHP payload, just changed the IP and port with my listener's.

<img width="1920" height="244" alt="Screenshot from 2026-02-01 19-13-40" src="https://github.com/user-attachments/assets/3716d616-85b6-4e74-b4d5-24979148e1f7" />

And because I'm using DVWA as a container, I have to find its IP.

<img width="1920" height="103" alt="Screenshot from 2026-02-01 19-15-25" src="https://github.com/user-attachments/assets/3d366b5d-4a75-4566-97a3-6bf046edbb9e" />

Then I set a listener on port 4444:
```bash
nc -nlvp 4444
```

And I started an HTTP server in the same location as the PHP reverse shell.

Then asked the website to access that remote file located on my HTTP server.

<img width="1920" height="959" alt="Screenshot from 2026-02-01 19-13-03" src="https://github.com/user-attachments/assets/500db7ad-ae51-4821-93b4-9932416eba10" />

The DVWA server successfully ran my PHP file, which allowed me to get a reverse shell.

<img width="1920" height="244" alt="Screenshot from 2026-02-01 19-13-15" src="https://github.com/user-attachments/assets/6e5edb44-2daa-411b-88a2-658009860606" />

But true RFI (remote PHP execution) is rare today because:
```
allow_url_include = Off by default
```

## MEDIUM

### LFI

Working same as previous level without any changes.

<img width="1920" height="794" alt="Screenshot from 2026-02-01 20-13-53" src="https://github.com/user-attachments/assets/f13836b6-27d6-4f15-bb5f-cc8ca624b257" />

### RFI

The developer added a simple check for `http://` in the page parameter to prevent any attempts at remote file inclusion. It simply removes it, so we can bypass it using redundancy.

<img width="1920" height="1045" alt="Screenshot from 2026-02-01 20-16-23" src="https://github.com/user-attachments/assets/ba8b9e7d-9c60-4d91-a106-16c61dda52a2" />

And I got a reverse shell.

<img width="1920" height="279" alt="Screenshot from 2026-02-01 20-16-41" src="https://github.com/user-attachments/assets/ec0ab02e-6a1c-4444-a4ed-d1fc3362daf3" />

## HIGH

### LFI

Our LFI trick isn't working anymore

<img width="1920" height="279" alt="Screenshot from 2026-02-01 20-32-30" src="https://github.com/user-attachments/assets/df978826-f7c8-4223-ac0a-4d70de973550" />


but bruteforcing the page parameter with a LFI wordlist showed that the `file://` wrapper is working.

<img width="1920" height="782" alt="Screenshot from 2026-02-01 20-34-34" src="https://github.com/user-attachments/assets/95209554-1760-4cbf-860e-b95c4efa107e" />

The `file://` wrapper is a PHP stream wrapper that allows PHP to access local files using a URL-like syntax.
