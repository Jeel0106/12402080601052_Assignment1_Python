def repeated_char(password):
    count = 1
    for i in range(1, len(password)):
        if password[i] == password[i - 1]:
            count += 1
            if count > 3:
                return True
        else:
            count = 1
    return False


def banned_word(password, banned):
    password = password.lower()
    for word in banned:
        if word.lower() in password:
            return True
    return False


def check_password(password, banned):
    if len(password) < 6 or len(password) > 12:
        return "WEAK_LENGTH"

    if banned_word(password, banned):
        return "COMPROMISED"

    if repeated_char(password):
        return "WEAK_PATTERN"

    lower = False
    upper = False
    digit = False
    special = False

    for ch in password:
        if ch.islower():
            lower = True
        if ch.isupper():
            upper = True
        if ch.isdigit():
            digit = True
        if ch in "$#@":
            special = True

    if lower and upper and digit and special:
        return "STRONG"

    return "WEAK_PATTERN"


def main():
    try:
        b = int(input())
        banned = []

        for i in range(b):
            banned.append(input().strip())

        n = int(input())

        for i in range(1, n + 1):
            password = input().rstrip("\n")
            result = check_password(password, banned)
            print(str(i) + ": " + result)

    except Exception:
        print("INVALID")


if __name__ == "__main__":
    main()
