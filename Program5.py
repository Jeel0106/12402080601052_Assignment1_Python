class Account:
    def __init__(self, account_id, balance):
        self.account_id = account_id
        self.balance = balance

    def deposit(self, amount):
        if amount <= 0:
            raise Exception("Invalid amount")
        self.balance += amount

    def withdraw(self, amount):
        if amount <= 0:
            raise Exception("Invalid amount")
        if amount > self.balance:
            raise Exception("Insufficient funds")
        self.balance -= amount


class Transaction:
    def __init__(self, operation, data):
        self.operation = operation
        self.data = data


class Bank:
    def __init__(self):
        self.accounts = {}
        self.history = []

    def add_account(self, account):
        self.accounts[account.account_id] = account

    def get_account(self, account_id):
        if account_id not in self.accounts:
            raise Exception("Account not found")
        return self.accounts[account_id]

    def deposit(self, account_id, amount):
        account = self.get_account(account_id)
        account.deposit(amount)
        self.history.append(Transaction("DEPOSIT", (account_id, amount)))

    def withdraw(self, account_id, amount):
        account = self.get_account(account_id)
        account.withdraw(amount)
        self.history.append(Transaction("WITHDRAW", (account_id, amount)))

    def transfer(self, first, second, amount):
        source = self.get_account(first)
        target = self.get_account(second)

        source.withdraw(amount)
        target.deposit(amount)

        self.history.append(
            Transaction("TRANSFER", (first, second, amount))
        )


def main():
    try:
        n = int(input())
        bank = Bank()

        for i in range(n):
            account_id, balance = input().split()
            bank.add_account(Account(account_id, int(balance)))

        q = int(input())
        batch_number = 0
        batch_data = None
        batch_failed = False
        failed_batches = []

        for i in range(q):
            command = input().split()

            if command[0] == "BATCH_BEGIN":
                batch_number += 1
                batch_data = {}
                for account_id in bank.accounts:
                    batch_data[account_id] = bank.accounts[account_id].balance
                batch_failed = False

            elif command[0] == "BATCH_END":
                if batch_failed:
                    for account_id in batch_data:
                        bank.accounts[account_id].balance = batch_data[account_id]
                    failed_batches.append(batch_number)
                batch_data = None
                batch_failed = False

            elif batch_data is not None and batch_failed:
                continue

            else:
                try:
                    if command[0] == "DEPOSIT":
                        bank.deposit(command[1], int(command[2]))
                    elif command[0] == "WITHDRAW":
                        bank.withdraw(command[1], int(command[2]))
                    elif command[0] == "TRANSFER":
                        bank.transfer(
                            command[1], command[2], int(command[3])
                        )
                    else:
                        raise Exception("Invalid operation")
                except Exception:
                    if batch_data is not None:
                        batch_failed = True
                    else:
                        raise

        for account_id in sorted(bank.accounts):
            print(account_id, bank.accounts[account_id].balance)

        for number in failed_batches:
            print("FAILED", number)

    except Exception:
        print("ERROR")


if __name__ == "__main__":
    main()
