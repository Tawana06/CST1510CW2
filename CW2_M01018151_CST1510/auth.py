import bcrypt
import os

USER_DATA_FILE = "users.txt"

import bcrypt

def hash_password(plain_text_password):
	password_bytes = plain_text_password.encode('utf-8')
	salt = bcrypt.gensalt()
	hashed_password = bcrypt.hashpw(password_bytes, salt)
	hashed_password_text = hashed_password.decode ('utf-8')
	return hashed_password_text

def verify_password(plain_text_password, hashed_password):
	password_bytes = plain_text_password.encode('utf-8')
	hashed_password_bytes = hashed_password.encode('utf-8')
	return bcrypt.checkpw(password_bytes, hashed_password_bytes)

def register_user(username, password):
	hashed_password = hash_password(password)
	with open("users.txt", "a") as f:
		f.write(f"{username}, {hashed_password}\n")
	print(f"User '{username}' registered")

def user_exists(username):
	if not os.path.exists("users.txt"):
		return False
	with open("users.txt", "r") as f :
		for line in f :
			existing_usernames = line.strip().split(",")
			if existing_usernames == username :
				return True
	return False

def login_user(username,password):
	with open("users.txt", "r") as f :
		for line in f.readlines() :
			user, hash = line.strip().split(',', 1)
			if user == username :
				return verify_password(password, hash)
	return False

def validate_username(username):
	return True

def validate_password(password):
	return True

def display_menu():
	"""" Displays the main menu options."""
	print("\n" + "="*50)
	print(" MULTI-DOMAIN INTELLIGENCE PLATFORM")
	print(" Secure Authentication System")
	print("="*50)
	print("\n[1] Register a new user")
	print("[2] Login")
	print("[3] Exit")
	print("-"*50)

def main():
	""""Main program loop"""
	print("\nWelcome to the Week 7 Authentication System!")

	while True :
		display_menu()
		choice = input("\nPlease select an option (1-3): ").strip()

		if choice == '1' :
			#Registration flow
			print("\n--- USER REGISTRATION ---")
			username = input("Enter a username: ").strip()

			#Validate username
			is_valid, error_msg = validate_username(username)
			if not is_valid :
				print(f"Error: {error_msg}")
				continue
			password = 	input("Enter a password: ").strip()

			#Validate password
			is_valid, error_msg = validate_password(password)
			if not is_valid:
				print(f"Error: {error_msg}")
				continue

			#Confirm password
			password_confirm = input("Confirm password: ").strip()
			if password != password_confirm:
				print("Error: Passwords do not match.")
				continue

			#Registeer the user
			register_user(username,password)

		elif choice == '2' :
			#Login flow
			print("\n--- USER LOGIN ---")
			username = input("Enter your username: ").strip()
			username = input("Enter your username: ").strip()


			if login_user(username, password) : #Attempt login
				print("\nYou are now logged in.")
				print("(In a real application, you would now access the domain")

				input("\nPress Enter to return to main menu...") #Optional:Ask If they want to logout or exit
		elif choice == '3' :
			#Exit
			print("\nThank you for using the authentication system.")
			print("Exiting...")
			break

		else:
			print("\nError: Invalid option. Please select 1, 2, or 3.")

if __name__ == "__main__" :
	main()