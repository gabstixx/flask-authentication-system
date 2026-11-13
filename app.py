
import os
from dotenv import load_dotenv
from flask import (
    Flask,
    request,
    session,
    redirect,
    url_for,
    render_template,
    flash
)
from database import get_db_connection
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf.csrf import CSRFProtect

load_dotenv()

app = Flask(__name__)

# Load and validate secret key
app.secret_key = os.getenv("SECRET_KEY")

if not app.secret_key:
    raise ValueError("SECRET_KEY is not configured")

# Enable CSRF protection
csrf = CSRFProtect(app)

# Session security settings
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"


# Enable secure cookies only in production (HTTPS)
is_production = os.getenv("FLASK_ENV") == "production"
app.config["SESSION_COOKIE_SECURE"] = is_production


@app.route("/")
def home():
    return render_template("login.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    email = request.form.get("email")
    password = request.form.get("password")

    if not email or not password:
        flash("Email and password are required.")
        return redirect(url_for("home"))

    connection = get_db_connection()

    user = connection.execute(
        "SELECT * FROM users WHERE email = ?",
        (email,)
    ).fetchone()

    connection.close()

    if user and check_password_hash(user["password_hash"], password):
        session.clear()
        session["user_id"] = user["id"]
        return redirect(url_for("dashboard"))

    flash("Invalid email or password.")
    return redirect(url_for("home"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")

    # Validate required fields
    if not username or not email or not password:
        flash("All fields are required.")
        return redirect(url_for("register"))

    # Validate password length
    if len(password) < 8:
        flash("Password must contain at least 8 characters.")
        return redirect(url_for("register"))

    # Validate password number requirement
    if not any(char.isdigit() for char in password):
        flash("Password must contain at least one number.")
        return redirect(url_for("register"))

    connection = get_db_connection()

    # Check for existing email or username
    existing_user = connection.execute(
        "SELECT id FROM users WHERE email = ? OR username = ?",
        (email, username)
    ).fetchone()

    if existing_user:
        connection.close()
        flash("Email or username already registered!")
        return redirect(url_for("register"))

    # Hash password
    hashed_password = generate_password_hash(password)

    # Insert new user
    connection.execute(
        "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
        (username, email, hashed_password)
    )

    connection.commit()
    connection.close()

    flash("Registration successful!")
    return redirect(url_for("home"))


@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("home"))

    connection = get_db_connection()

    user = connection.execute(
        "SELECT username FROM users WHERE id = ?",
        (session["user_id"],)
    ).fetchone()

    connection.close()

    if not user:
        session.clear()
        return redirect(url_for("home"))

    return render_template("dashboard.html", username=user["username"])


@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
