import csv
from collections import defaultdict
from datetime import datetime


def valid_row(row):
    if not row["tid"] or not row["acc"]:
        return False, "missing data"

    if row["type"] not in ["CREDIT", "DEBIT"]:
        return False, "invalid type"

    try:
        amount = float(row["amount"])
    except:
        return False, "amount is not numeric"

    if amount <= 0:
        return False, "amount must be positive"

    try:
        datetime.strptime(row["time"], "%Y-%m-%dT%H:%M:%S")
    except:
        return False, "invalid timestamp"

    return True, ""


def main():
    try:
        file_name = input().strip()
        balance = defaultdict(float)

        with open(file_name, "r", newline="") as file:
            reader = csv.DictReader(file)

            with open("credit.csv", "w", newline="") as credit_file,                  open("debit.csv", "w", newline="") as debit_file,                  open("error.csv", "w", newline="") as error_file:

                fields = ["tid", "acc", "type", "amount", "time"]

                credit_writer = csv.DictWriter(credit_file, fieldnames=fields)
                debit_writer = csv.DictWriter(debit_file, fieldnames=fields)
                error_writer = csv.DictWriter(
                    error_file, fieldnames=fields + ["reason"]
                )

                credit_writer.writeheader()
                debit_writer.writeheader()
                error_writer.writeheader()

                for row in reader:
                    try:
                        ok, reason = valid_row(row)

                        if not ok:
                            new_row = row.copy()
                            new_row["reason"] = reason
                            error_writer.writerow(new_row)
                            continue

                        amount = float(row["amount"])

                        if row["type"] == "CREDIT":
                            credit_writer.writerow(row)
                            balance[row["acc"]] += amount
                        else:
                            debit_writer.writerow(row)
                            balance[row["acc"]] -= amount

                    except Exception as e:
                        new_row = row.copy()
                        new_row["reason"] = str(e)
                        error_writer.writerow(new_row)

        print("Console:")
        accounts = sorted(
            balance,
            key=lambda x: (-abs(balance[x]), x)
        )

        for account in accounts:
            value = balance[account]
            if value.is_integer():
                value = int(value)
            print(account, value)

        print("Files created: credit.csv, debit.csv, error.csv")

    except Exception:
        print("ERROR")


if __name__ == "__main__":
    main()
