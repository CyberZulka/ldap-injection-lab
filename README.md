# Cyber Zulka — LDAP Injection Lab

## Project Overview

This project demonstrates LDAP Injection in a controlled, local cybersecurity lab environment.

It compares a deliberately vulnerable Flask application with a secure implementation that escapes special LDAP filter characters.

The purpose is to understand how unsafe LDAP filter construction can expose directory information and how secure coding practices help prevent this vulnerability.

## Lab Objectives

- Understand LDAP directory structure and Distinguished Names (DNs).
- Configure a local OpenLDAP directory.
- Create fictional users, groups, and a dedicated application service account.
- Demonstrate LDAP filter injection through an unsafe search endpoint.
- Implement secure LDAP filtering using `escape_filter_chars()`.
- Implement password-based LDAP authentication.
- Compare vulnerable and secure application behavior.
- Apply directory access controls.

## Technologies Used

- Parrot OS
- OpenLDAP
- Python 3
- Flask
- ldap3
- Requests
- Git and GitHub

## Lab Architecture

The application communicates with a local OpenLDAP directory.

- Flask provides the HTTP API.
- The LDAP service account performs directory searches.
- The vulnerable endpoint inserts user input directly into an LDAP filter.
- The secure endpoint escapes special LDAP filter characters.
- Secure login verifies the supplied password by binding as the matching LDAP user.

## Demonstrated Vulnerability

### Vulnerable endpoint

`GET /vulnerable/search?username=*`

The application inserts the supplied username directly into its LDAP filter.

A wildcard (`*`) can therefore broaden the search and return multiple directory entries.

### Secure endpoint

`GET /secure/search?username=*`

The application uses `escape_filter_chars()` before constructing the LDAP filter.

The wildcard is treated as a literal character rather than an LDAP wildcard.

### Demonstration results

| Test | Vulnerable behavior | Secure behavior |
|---|---|---|
| Normal username | Returns matching user | Returns matching user |
| Wildcard username | Returns multiple users | Returns no matching users |

## Secure Authentication

The application also provides:

`POST /secure/login`

The login process:

1. Receives a username and password.
2. Escapes the username before building the LDAP search filter.
3. Searches for exactly one matching user.
4. Retrieves the user's Distinguished Name.
5. Attempts authentication using that user's LDAP credentials.
6. Returns success only when authentication succeeds.

### Authentication test results

| Test | Expected HTTP status | Result |
|---|---:|---|
| Correct credentials | 200 | Authentication successful |
| Incorrect password | 401 | Authentication rejected |
| Wildcard username | 401 | Authentication rejected |

A wildcard search result alone cannot authenticate a user. Password verification is still required.

## Security Improvements

- Escape user-controlled LDAP filter input.
- Use a dedicated LDAP application service account instead of the directory administrator account.
- Restrict anonymous directory searches through LDAP access controls.
- Verify user credentials through LDAP authentication.
- Keep the Flask development server bound to localhost.
- Keep credentials outside application source code using environment variables.

## Running the Application

### 1. Clone the repository

```bash
git clone https://github.com/CyberZulka/ldap-injection-lab.git
cd ldap-injection-lab
```

Replace the repository URL with your actual GitHub repository URL.

### 2. Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the service account password

```bash
read -s -p "Enter Flask service account password: " LDAP_APP_PASSWORD
echo
export LDAP_APP_PASSWORD
```

Use the password configured for the local `flask-reader` LDAP account.

### 5. Start the Flask application

```bash
python app/app.py
```

The application runs locally at:

`http://127.0.0.1:5000`

The local OpenLDAP directory and service account must already be configured.

## Important Security Notice

This project is an educational lab designed for an isolated local environment.

The vulnerable endpoint is intentionally insecure and must never be exposed to the public internet.

The lab uses LDAP simple binds over local LDAP. Production deployments should use StartTLS or LDAPS with proper certificate validation.

Do not commit passwords, password hashes, or sensitive terminal logs to GitHub.

## Project Structure

```text
ldap-injection-lab/
├── app/
│   ├── __init__.py
│   ├── app.py
│   └── ldap_utils.py
├── documentation/
│   ├── directory-structure.ldif
│   ├── organizational-units.ldif
│   ├── users.ldif
│   ├── groups.ldif
│   └── lab-journal.md
├── screenshots/
├── requirements.txt
└── README.md
```

## Learning Outcome

This lab demonstrates why LDAP filter construction must be handled carefully.

It highlights the difference between vulnerable input handling and secure LDAP filtering, while showing that authentication must independently verify user credentials.

**Project:** Cyber Zulka LDAP Injection Lab  
**Purpose:** Application Security Learning and Practical Vulnerability Demonstration

