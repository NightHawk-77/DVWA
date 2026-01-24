## What is DVWA?

**Damn Vulnerable Web Application (DVWA)** is an intentionally vulnerable web application designed for learning and practicing web application security.

It includes multiple common real-world vulnerabilities, such as:

- SQL Injection  
- Cross-Site Scripting (XSS)  
- Command Injection  
- Cross-Site Request Forgery (CSRF)  
- File Upload vulnerabilities  
- And more  

DVWA is intentionally insecure and should **never** be deployed on a public or production server.

---

## DVWA Installation Using Docker

To ensure a clean, isolated, and reproducible environment, DVWA was installed using **Docker**.

---

### Step 1: Verify Docker Is Installed and Running

Verify that Docker is installed and the service is running:

`sudo systemctl status docker`

If Docker is not installed, it must be installed before proceeding.

---

### Step 2: Grant Docker Permissions to the Current User

To avoid using `sudo` with every Docker command, add the current user to the Docker group:

`sudo usermod -aG docker $USER`

After running this command, log out and log back in for the changes to take effect.

---

### Step 3: Pull the DVWA Docker Image

Download the official DVWA Docker image:

`docker pull vulnerables/web-dvwa`

<img width="1920" height="658" alt="Screenshot from 2026-01-24 20-26-28" src="https://github.com/user-attachments/assets/4145e6d0-ded1-4856-a62e-510ff89ed855" />


---

### Step 4: Run the DVWA Container

Start the DVWA container and expose it on port 8000:

`docker run --rm -it -p 8000:80 vulnerables/web-dvwa`

This command maps port 8000 on the host machine to port 80 inside the container.

<img width="1920" height="350" alt="Screenshot from 2026-01-24 20-33-20" src="https://github.com/user-attachments/assets/6e7af713-52f4-40f3-bd2f-309065b2359b" />

---

### Step 5: Access DVWA in the Browser

Once the container is running, access DVWA using a web browser:

`http://localhost:8000`

<img width="1920" height="963" alt="Screenshot from 2026-01-24 20-31-36" src="https://github.com/user-attachments/assets/a0346b36-40a7-4faa-a511-f85533b94457" />

At this point, the DVWA application is successfully installed and accessible locally.

