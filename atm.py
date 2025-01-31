import hashlib

# Global variables
accounts = {
    "user1": {"pin": hashlib.sha256("1234".encode()).hexdigest(), "balance": 1000, "transactions": []},
    "user2": {"pin": hashlib.sha256("5678".encode()).hexdigest(), "balance": 2000, "transactions": []},
}
admin_pin = hashlib.sha256("admin123".encode()).hexdigest()
current_user = None

# Function to authenticate the user
def authenticate():
    global current_user
    attempts = 3
    while attempts > 0:
        username = input("Enter your username: ")
        pin = input("Enter your PIN: ")
        hashed_pin = hashlib.sha256(pin.encode()).hexdigest()

        # Check if the user is an admin
        if username == "admin" and hashed_pin == admin_pin:
            current_user = "admin"
            return True
        # Check if the user is a regular user
        elif username in accounts and accounts[username]["pin"] == hashed_pin:
            current_user = username
            return True
        else:
            attempts -= 1
            print(f"Incorrect username or PIN. {attempts} attempts remaining.")
    return False

# Function to create a new user
def create_user():
    username = input("Enter a new username: ")
    if username in accounts:
        print("Username already exists. Please choose a different username.")
        return
    pin = input("Enter a new PIN: ")
    if len(pin) != 4 or not pin.isdigit():
        print("PIN must be a 4-digit number.")
        return
    balance = get_float_input("Enter the initial balance: $")
    if balance < 0:
        print("Initial balance cannot be negative.")
        return
    hashed_pin = hashlib.sha256(pin.encode()).hexdigest()
    accounts[username] = {"pin": hashed_pin, "balance": balance, "transactions": []}
    print(f"User '{username}' created successfully with an initial balance of ${balance:.2f}.")

# Function to check balance
def check_balance():
    print(f"Your current balance is: ${accounts[current_user]['balance']:.2f}")

# Function to deposit money
def deposit():
    amount = get_float_input("Enter the amount to deposit: $")
    if amount > 0:
        accounts[current_user]["balance"] += amount
        accounts[current_user]["transactions"].append(f"Deposited ${amount:.2f}")
        print(f"${amount:.2f} deposited successfully.")
    else:
        print("Invalid amount.")

# Function to withdraw money
def withdraw():
    amount = get_float_input("Enter the amount to withdraw: $")
    if amount > 0 and amount <= accounts[current_user]["balance"]:
        accounts[current_user]["balance"] -= amount
        accounts[current_user]["transactions"].append(f"Withdrew ${amount:.2f}")
        print(f"${amount:.2f} withdrawn successfully.")
    else:
        print("Invalid amount or insufficient balance.")

# Function to view transaction history
def view_transactions():
    if not accounts[current_user]["transactions"]:
        print("No transactions found.")
    else:
        print("Transaction History:")
        for transaction in accounts[current_user]["transactions"]:
            print(f"- {transaction}")

# Function to handle numeric input
def get_float_input(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Invalid input. Please enter a numeric value.")

# Admin mode to view all accounts and transactions
def admin_mode():
    while True:  # Loop for admin mode
        print("\nAdmin Mode")
        print("1. View All Accounts")
        print("2. View All Transactions")
        print("3. Create New User")
        print("4. Exit Admin Mode")
        choice = input("Enter your choice: ")
        if choice == "1":
            print("\nAll Accounts:")
            for username, details in accounts.items():
                print(f"Username: {username}, Balance: ${details['balance']:.2f}")
        elif choice == "2":
            print("\nAll Transactions:")
            for username, details in accounts.items():
                print(f"Username: {username}:")
                for transaction in details["transactions"]:
                    print(f"- {transaction}")
        elif choice == "3":
            create_user()
        elif choice == "4":
            print("Exiting admin mode.")
            return  # Exit admin mode and return to main menu
        else:
            print("Invalid choice.")

# Main menu function
def main_menu():
    global current_user
    print("Welcome to the ATM")
    if authenticate():
        while True:
            if current_user == "admin":
                admin_mode()
                current_user = None  # Reset current_user after exiting admin mode
                break  # Break out of the loop to return to login screen
            else:
                print("\nMain Menu")
                print("1. Check Balance")
                print("2. Deposit")
                print("3. Withdraw")
                print("4. View Transactions")
                print("5. Logout")
                choice = input("Enter your choice: ")
                if choice == "1":
                    check_balance()
                elif choice == "2":
                    deposit()
                elif choice == "3":
                    withdraw()
                elif choice == "4":
                    view_transactions()
                elif choice == "5":
                    print("Logging out...")
                    current_user = None
                    break
                else:
                    print("Invalid choice. Please try again.")
    else:
        print("Too many incorrect attempts. Exiting...")

# Entry point of the program
if __name__ == "__main__":
    while True:
        main_menu()
        if input("Do you want to restart the ATM? (yes/no): ").lower() != "yes":
            print("Thank you for using the ATM. Goodbye!")
            break