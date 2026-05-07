from datetime import datetime


class Amount:
    def __init__(self, amount: float, timestamp: datetime, transaction_type: str):
        self.amount = float(amount)
        self.timestamp = timestamp
        self.transaction_type = transaction_type

    def __str__(self) -> str:
        return (
            f"[{self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}] "
            f"{self.transaction_type}: {self.amount:.2f}"
        )


class PersonalAccount:
    def __init__(self, account_number: int, account_holder: str):
        self.account_number = account_number
        self.account_holder = account_holder
        self.balance = 0.0
        self.transactions = []

    def deposit(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Deposit amount must be greater than 0.")

        transaction = Amount(amount, datetime.now(), "DEPOSIT")
        self.transactions.append(transaction)
        self.balance += amount

    def withdraw(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Withdrawal amount must be greater than 0.")

        if amount > self.balance:
            raise ValueError("Insufficient funds.")

        transaction = Amount(amount, datetime.now(), "WITHDRAWAL")
        self.transactions.append(transaction)
        self.balance -= amount

    def print_transaction_history(self) -> None:
        if not self.transactions:
            print("No transactions yet.")
            return

        print("--- Transaction History ---")
        for tx in self.transactions:
            print(str(tx))

    def get_balance(self) -> float:
        return self.balance

    def get_account_number(self) -> int:
        return self.account_number

    def set_account_number(self, account_number: int) -> None:
        self.account_number = account_number

    def get_account_holder(self) -> str:
        return self.account_holder

    def set_account_holder(self, account_holder: str) -> None:
        self.account_holder = account_holder

    def __str__(self) -> str:
        return (
            f"PersonalAccount(account_number={self.account_number}, "
            f"account_holder='{self.account_holder}', "
            f"balance={self.balance:.2f})"
        )

    def __add__(self, amount: float):
        self.deposit(float(amount))
        return self

    def __sub__(self, amount: float):
        self.withdraw(float(amount))
        return self


def run_sample_test() -> None:
    print("=== Personal Account Management ===")
    account_number = int(input("Enter account number: ").strip())
    account_holder = input("Enter account holder name: ").strip()

    account = PersonalAccount(account_number, account_holder)

    while True:
        print("\n1. Deposit")
        print("2. Withdraw")
        print("3. Check Balance")
        print("4. Print Transaction History")
        print("5. Print Account Info")
        print("6. Exit")

        choice = input("Choose an option (1-6): ").strip()

        try:
            if choice == "1":
                amount = float(input("Enter deposit amount: ").strip())
                account.deposit(amount)
                print("Deposit successful.")

            elif choice == "2":
                amount = float(input("Enter withdrawal amount: ").strip())
                account.withdraw(amount)
                print("Withdrawal successful.")

            elif choice == "3":
                print(f"Current balance: {account.get_balance():.2f}")

            elif choice == "4":
                account.print_transaction_history()

            elif choice == "5":
                print(account)

            elif choice == "6":
                print("Goodbye")
                break

            else:
                print("Invalid option. Please choose 1-6.")

        except ValueError as err:
            print(f"Error: {err}")


if __name__ == "__main__":
    run_sample_test()
