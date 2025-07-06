import secrets
import os
from django.db import transaction
from typing import Union, List

from .emails import send_account_creation_email
from .models import BankAccount


def generate_account_number(currency: str) -> str:
    bank_code = os.environ.get("BANK_CODE")
    branch_code = os.environ.get("BANK_BRANCH_CODE")

    currency_code = {
        "us_dollar": os.environ.get("CURRENCY_CODE_USD"),
        "euro": os.environ.get("CURRENCY_CODE_EUR"),
        "pound_sterling": os.environ.get("CURRENCY_CODE_GBP"),
    }

    currency_code = currency_code.get(currency)

    if not currency_code:
        raise ValueError("Invalid currency: ", currency)

    prefix = f"{bank_code}{branch_code}{currency_code}"
    remaining_digits = 16 - len(prefix) - 1

    random_digits = "".join(
        secrets.choice("0123456789") for _ in range(remaining_digits)
    )
    partial_account_number = f"{prefix}{random_digits}"

    check_digit = calculate_luhn_check_digit(partial_account_number)

    return f"{partial_account_number}{check_digit}"


def calculate_luhn_check_digit(number: str) -> int:

    def split_into_digits(n: Union[str, int]) -> List[int]:
        return [int(digit) for digit in str(n)]

    digits = split_into_digits(number)
    odd_digits = digits[-1::-2]
    even_digits = digits[-2::-2]
    total = sum(odd_digits)

    for d in even_digits:
        double = d * 2
        total += sum(split_into_digits(double))

    return (10 - (total % 10)) % 10

def create_bank_account(user, currency: str, account_type: str) -> str:
    with transaction.atomic():
        while True:
            account_number = generate_account_number(currency)

            if not BankAccount.objects.filter(account_number=account_number).exists():
                break

        is_primary = not BankAccount.objects.filter(user=user).exists()

        bank_account = BankAccount.objects.create(
            user=user,
            account_number=account_number,
            currency=currency,
            account_type=account_type,
            is_primary=is_primary
        )

        send_account_creation_email(user, bank_account)

        return bank_account