def is_repeated(s: str) -> bool:
    """Check if a string contains only the same character."""
    return len(set(s)) == 1

def remove_non_digits(cpf_number: str) -> str:
    """Remove non-digit characters from a CPF string."""
    return ''.join(char for char in cpf_number if char.isdigit())

def convert_to_digits(cpf: str) -> list[int]:
    """Convert a CPF string to a list of integers."""
    return [int(digit) for digit in cpf]

def calculate_check_digit(digits: list[int], weights: list[int]) -> int:
    """Calculate a single check digit based on the provided digits and weights."""
    total_sum = sum(d * w for d, w in zip(digits, weights))
    remainder = total_sum % 11
    return 0 if remainder < 2 else 11 - remainder

def get_check_digits(digits: list[int]) -> list[int]:
    """Calculate and return the two check digits of a CPF."""
    # First check digit
    first_weights = list(range(10, 1, -1))
    first_check_digit = calculate_check_digit(digits[:9], first_weights)

    # Second check digit
    second_weights = list(range(11, 1, -1))
    second_check_digit = calculate_check_digit(digits[:9] + [first_check_digit], second_weights)

    return [first_check_digit, second_check_digit]