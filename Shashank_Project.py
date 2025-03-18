import json

# Multi-line string
multi_line_string = """This is a 
string that spans 
multiple lines."""

# Docstring for a function
""" This function does something.It can have multiple lines of explanation ."""

class BankAccount:
    """A class representing a bank account with basic operations."""
    
    def __init__(self, account_number, owner, password, balance=0.0):
        self.account_number = account_number
        self.owner = owner
        self.__password = password  # Private attribute
        self.balance = balance
        self.transactions = []  # Store transaction history
    
    def authenticate(self, password):
        """Check if the entered password matches the stored one."""
        return self.__password == password

    def deposit(self, amount):
        """Deposit money into the account."""
        try:
            assert amount > 0, "Deposit amount must be positive."
            self.balance += amount
            self.transactions.append(f"Deposited: ${amount}")
            print(f"Success! ${amount} deposited. New balance: ${self.balance}")
        except AssertionError as e:
            print(f"Error: {e}")

    def withdraw(self, amount):
        """Withdraw money from the account."""
        try:
            assert amount > 0, "Withdrawal amount must be positive."
            assert amount <= self.balance, "Insufficient funds."
            self.balance -= amount
            self.transactions.append(f"Withdrew: ${amount}")
            print(f"Success! ${amount} withdrawn. New balance: ${self.balance}")
        except AssertionError as e:
            print(f"Error: {e}")

    def get_balance(self):
        """Return the current balance."""
        return self.balance

    def get_transaction_history(self):
        """Return the transaction history."""
        return self.transactions if self.transactions else ["No transactions yet."]


class Bank:
    """A class representing a simple banking system."""
    
    def __init__(self):
        self.accounts = self.load_accounts()

    def load_accounts(self):
        """Load accounts from a JSON file."""
        try:
            with open("accounts.json", "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def save_accounts(self):
        """Save accounts to a JSON file."""
        with open("accounts.json", "w") as f:
            json.dump(self.accounts, f, indent=4)

    def create_account(self, account_number, owner, password):
        """Create a new bank account."""
        if account_number in self.accounts:
            print("Error: Account number already exists.")
        else:
            self.accounts[account_number] = {
                "owner": owner,
                "password": password,
                "balance": 0.0,
                "transactions": []
            }
            self.save_accounts()
            print(f"Account created successfully for {owner}!")

    def login(self, account_number, password):
        """Authenticate a user and return the account if valid."""
        account_data = self.accounts.get(account_number)
        if account_data and account_data["password"] == password:
            print(f"Welcome, {account_data['owner']}!")
            return BankAccount(account_number, account_data["owner"], password, account_data["balance"])
        else:
            print("Error: Invalid account number or password.")
            return None


def main():
    bank = Bank()

    while True:
        print("\nBanking System Menu:")
        print("1. Create Account")
        print("2. Login")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            acc_number = input("Enter account number: ")
            owner = input("Enter account holder name: ")
            password = input("Set your password: ")
            bank.create_account(acc_number, owner, password)

        elif choice == "2":
            acc_number = input("Enter account number: ")
            password = input("Enter password: ")
            account = bank.login(acc_number, password)

            if account:
                while True:
                    print("\nAccount Menu:")
                    print("1. Deposit")
                    print("2. Withdraw")
                    print("3. Check Balance")
                    print("4. Transaction History")
                    print("5. Logout")
                    sub_choice = input("Enter your choice: ")

                    if sub_choice == "1":
                        amount = float(input("Enter amount to deposit: "))
                        account.deposit(amount)
                    elif sub_choice == "2":
                        amount = float(input("Enter amount to withdraw: "))
                        account.withdraw(amount)
                    elif sub_choice == "3":
                        print(f"Current Balance: ${account.get_balance()}")
                    elif sub_choice == "4":
                        print("Transaction History:")
                        for transaction in account.get_transaction_history():
                            print(transaction)
                    elif sub_choice == "5":
                        print("Logging out...")
                        break
                    else:
                        print("Invalid choice, please try again.")

        elif choice == "3":
            print("Thank you for using the banking system. Goodbye!")
            break

        else:
            print("Invalid option. Please try again.")

# Run the program
if __name__ == "__main__":
    main()
