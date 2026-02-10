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


# Switching from DVWA Container to Local Installation

And since the DVWA container is missing some labs, I had to switch to local web server installation.

That's why I will switch to normal local installation to do those missed labs.

So let's start by cloning the GitHub repo into `/var/www/html` and change its permission, so let's give full permissions to everyone on the DVWA folder and all its contents (since it's a local lab, that's okay).

And then make a backup of `config.inc.php`:

<img width="926" height="248" alt="Screenshot from 2026-02-10 18-22-09" src="https://github.com/user-attachments/assets/31f73a21-c8bc-41ee-8699-af94dfc6c4d0" />

<img width="960" height="206" alt="Screenshot from 2026-02-10 18-24-21" src="https://github.com/user-attachments/assets/69e710a7-5c24-41bc-a1be-6db499589171" />


And let's change the default credentials to something easy like: `admin:password`:

<img width="656" height="109" alt="Screenshot from 2026-02-10 18-25-44" src="https://github.com/user-attachments/assets/dd88f564-c792-4a88-879d-9b9565183bea" />


And let's add that user to MySQL DB with:
```sql
CREATE USER 'admin'@'127.0.0.1' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON dvwa.* TO 'admin'@'127.0.0.1';
FLUSH PRIVILEGES;
```

Then install Apache and install PHP for it:
```bash
sudo apt install apache2
sudo apt install php libapache2-mod-php php-mysql
```

Then change values of `allow_url_fopen` and `allow_url_include` inside `/etc/php/yourversion/apache2/php.ini`, both of them should be on.

<img width="789" height="161" alt="Screenshot from 2026-02-10 18-50-04" src="https://github.com/user-attachments/assets/e592118f-8087-438e-b777-e8bebb3e0413" />

The first one is for: Allows PHP functions to open remote URLs as files.

And second one: Allows remote files to be included as PHP code.

And just restart Apache2, and login to http://127.0.0.1/dvwa.

And here we have the missed labs:

<img width="179" height="106" alt="Screenshot from 2026-02-10 19-02-02" src="https://github.com/user-attachments/assets/b8842a87-1200-4051-a084-fd66e6906a6b" />
