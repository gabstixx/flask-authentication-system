# Flask Authentication System

## About the Project

Flask Authentication System is a web application that allows users to create accounts, log in, and access a protected dashboard.

It uses Flask to handle application routes and authentication logic, SQLite to store user information, and Werkzeug to securely hash passwords.

## Features

1. User registration with username, email, and password.
2. Password validation requiring at least 8 characters and one number.
3. Duplicate username and email prevention.
4. Secure password hashing and verification.
5. Login authentication.
6. Protected dashboard for authenticated users.
7. Session management and logout functionality.
8. CSRF protection for form submissions.
9. Flash messages for registration and login feedback.
10. Environment-based secret key configuration.

## Technologies Used

1. Python
2. Flask
3. SQLite
4. HTML5
5. CSS3
6. Werkzeug
7. Flask-WTF
8. python-dotenv

## Project Structure

```text
flask-authentication-system/
|
|-- app.py
|-- database.py
|-- requirements.txt
|-- .gitignore
|
|-- static/
|   |-- css/
|       |-- style.css
|
|-- templates/
|   |-- login.html
|   |-- register.html
|   |-- dashboard.html
|
|-- screenshots/
    |-- 01-register.png
    |-- 02-login.png
    |-- 03-dashboard.png
```

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/flask-authentication-system.git
cd flask-authentication-system
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```env
SECRET_KEY=your-secret-key
```

Generate a secure secret key rather than using the example value.

### 5. Run the Application

```bash
python app.py
```

Open `http://127.0.0.1:5000` in your browser.

The SQLite database and users table are created automatically when the application starts.

## Future Improvements

1. Email verification and password reset.
2. Improved input validation and error handling.
3. Automated tests.
4. Deployment to a production environment.
