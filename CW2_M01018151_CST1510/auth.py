import re
import bcrypt
import os
import time

USER_DATA_FILE = "users.txt"
LOCKOUT_TIME = 300  # 5 minutes in seconds
MAX_FAILED_ATTEMPTS = 3

# Track failed login attempts
failed_attempts = {}  # {username: [attempt_count, last_failed_time]}


#  PASSWORD HASHING
def hash_password(plain_text_password):
    password_bytes = plain_text_password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, salt)
    return hashed_password.decode('utf-8')


def verify_password(plain_text_password, hashed_password):
    password_bytes = plain_text_password.encode('utf-8')
    hashed_password_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_password_bytes)


# Checking for the user
def user_exists(username):
    if not os.path.exists(USER_DATA_FILE):
        return False

    with open(USER_DATA_FILE, "r") as f:
        for line in f:
            user = line.strip().split(",")[0]
            if user == username:
                return True
    return False


# input validation (ChatGpt debugging)
def validate_username(username):
    if len(username) < 3:
        return False, "Username must be at least 3 characters long."
    if " " in username:
        return False, "Username cannot contain spaces."
    if not re.match(r"^[A-Za-z0-9_]+$", username):
        return False, "Username can only contain letters, numbers, and underscores."
    if user_exists(username):
        return False, f"Username '{username}' already exists."
    return True, ""


def validate_password(password):
    if len(password) < 8:
        return False, "Password must be at least 8 characters long."
    if not re.search(r"[a-z]", password):
        return False, "Password must contain at least one lowercase letter."
    if not re.search(r"[A-Z]", password):
        return False, "Password must contain at least one uppercase letter."
    if not re.search(r"[0-9]", password):
        return False, "Password must contain at least one number."
    if not re.search(r"[!@#$%^&*()_+\-=\[\]{};':,.<>/?]", password):
        return False, "Password must contain at least one special character."
    return True, ""


# registration of user
def register_user(username, password, role="user"):
    """Register a new user with role."""
    if user_exists(username):
        print(f"Error: Username '{username}' already exists.")
        return False

    hashed_password = hash_password(password)
    with open(USER_DATA_FILE, "a") as f:
        f.write(f"{username},{hashed_password},{role}\n")

    print(f"User '{username}' registered with role '{role}'")
    return True

#user login
def login_user(username, password):
    """Authenticate a user and handle lockout."""
    global failed_attempts

    # Check for lockout
    if username in failed_attempts:
        attempts, last_time = failed_attempts[username]
        if attempts >= MAX_FAILED_ATTEMPTS and (time.time() - last_time) < LOCKOUT_TIME:
            remaining = int(LOCKOUT_TIME - (time.time() - last_time))
            print(f"Account locked. Try again in {remaining} seconds.")
            return False
        elif (time.time() - last_time) >= LOCKOUT_TIME:
            # Reset failed attempts after lockout period
            failed_attempts[username] = [0, 0]

    if not os.path.exists(USER_DATA_FILE):
        print("Error: No users registered yet.")
        return False

    with open(USER_DATA_FILE, "r") as f:
        for line in f.readlines():
            parts = line.strip().split(",")
            if len(parts) < 3:
                continue
            user, hash_val, role = parts[0], parts[1], parts[2]
            if user == username:
                if verify_password(password, hash_val):
                    # Reset failed attempts after successful login
                    failed_attempts[username] = [0, 0]
                    print(f"\nYou are now logged in as '{username}' (Role: {role}).")
                    return True
                else:
                    # Increment failed attempts
                    if username not in failed_attempts:
                        failed_attempts[username] = [1, time.time()]
                    else:
                        failed_attempts[username][0] += 1
                        failed_attempts[username][1] = time.time()
                    attempts_left = MAX_FAILED_ATTEMPTS - failed_attempts[username][0]
                    if attempts_left > 0:
                        print(f"Error: Invalid password. Attempts left: {attempts_left}")
                    else:
                        print(f"Error: Account locked due to 3 failed attempts. Try again in 5 minutes.")
                    return False

    print("Error: Username not found.")
    return False


# main system
def display_menu():
    print("\n" + "="*50)
    print(" MULTI-DOMAIN INTELLIGENCE PLATFORM")
    print(" Secure Authentication System")
    print("="*50)
    print("\n[1] Register a new user")
    print("[2] Login")
    print("[3] Exit")
    print("-"*50)


def main():
    print("\nWelcome to the Week 7 Authentication System!")

    while True:
        display_menu()
        choice = input("\nPlease select an option (1-3): ").strip()

        if choice == '1':
            # Registration flow
            print("\n--- USER REGISTRATION ---")
            username = input("Enter a username: ").strip()

            # Validate username
            is_valid, error_msg = validate_username(username)
            if not is_valid:
                print(f"Error: {error_msg}")
                continue

            password = input("Enter a password: ").strip()

            # Validate password
            is_valid, error_msg = validate_password(password)
            if not is_valid:
                print(f"Error: {error_msg}")
                continue

            password_confirm = input("Confirm password: ").strip()
            if password != password_confirm:
                print("Error: Passwords do not match.")
                continue

            # role selection
            print("\nSelect a role for the user:")
            print("[1] User")
            print("[2] Admin")
            print("[3] Analyst")

            role_choice = input("Enter 1, 2, or 3: ").strip()
            if role_choice == "1":
                role = "user"
            elif role_choice == "2":
                role = "admin"
            elif role_choice == "3":
                role = "analyst"
            else:
                print("Error: Invalid role selected.")
                continue

            register_user(username, password, role)

        elif choice == '2':
            # Login flow
            print("\n--- USER LOGIN ---")
            username = input("Enter your username: ").strip()
            password = input("Enter your password: ").strip()

            login_user(username, password)

            input("\nPress Enter to return to main menu...")

        elif choice == '3':
            print("\nThank you for using the authentication system.")
            print("Exiting...")
            break

        else:
            print("\nError: Invalid option. Please select 1, 2, or 3.")


if __name__ == "__main__":
    main()

#chatgpt was used to debug