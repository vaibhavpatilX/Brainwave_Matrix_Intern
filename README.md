

This is an ATM interface implemented in Python. It supports the following functionalities:
- **User Authentication**: Login with a username and PIN.
- **Check Balance**: View the current account balance.
- **Deposit**: Add funds to the account.
- **Withdraw**: Withdraw funds from the account.
- **Transaction History**: View a list of all transactions.
- **Admin Mode**: Admins can view all accounts and transactions, and create new users.
- **Logout**: Log out and switch users.

## Features
- **Multiple Accounts**: Supports multiple users with unique PINs.
- **Secure PIN Storage**: PINs are securely hashed using SHA-256.
- **Transaction Tracking**: Keeps a record of all deposits and withdrawals.
- **Admin Privileges**: Admins can view all accounts, transactions, and create new users.
- **User-Friendly Interface**: Simple and intuitive menu-driven interface.

## How to Run
1. **Ensure Python is installed** on your system (Python 3.6 or higher recommended).
2. **Download the Project**:
   - Clone this repository or download the `atm.py` file.
3. **Navigate to the Project Folder**:
   - Open a terminal or command prompt.
   - Navigate to the folder containing `atm.py`.
4. **Run the Script**:
   - Use the following command to run the program:
     ```bash
     python atm.py
     ```
5. **Follow the On-Screen Instructions**:
   - Log in as a regular user or admin.
   - Use the menu to perform transactions.

## Example Logins
### Regular Users:
- **Username**: `user1`, **PIN**: `1234`
- **Username**: `user2`, **PIN**: `5678`

### Admin:
- **Username**: `admin`, **PIN**: `admin123`

## Admin Features
- **View All Accounts**: See a list of all users and their balances.
- **View All Transactions**: See a list of all transactions for every user.
- **Create New User**: Add a new user with a unique username, PIN, and initial balance.
- **Exit Admin Mode**: Return to the main menu.
   
