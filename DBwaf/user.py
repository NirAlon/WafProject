import re  # for regular expressions

regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'


def check_strong_password(password: object) -> object:
    print("HERE check_strong_password")
    # Primary conditions for password validation :
        # Minimum 8 characters.
        # The alphabets must be between [a-z]
        # At least one alphabet should be of Upper Case [A-Z]
        # At least 1 number or digit between [0-9].
        # At least 1 special character

    if len(password) >= 8:
        if not re.search("[a-z]", password):
            return False
        elif not re.search("[0-9]", password):
            return False
        elif not re.search("[A-Z]", password):
            return False
        elif not re.search("[@_!#$%^&*()<>?/\|}{~:]", password):
            return False
        elif re.search("\s", password):
            return False
        else:
            return True  # Valid Password
    else:
        print("Password must be at least 8 characters long")
        return False


def validation_email(email):
    print("HERE validation_email")
    if re.search(regex, email):
        return True
    else:
        return False


if __name__ == '__main__':

    pass
