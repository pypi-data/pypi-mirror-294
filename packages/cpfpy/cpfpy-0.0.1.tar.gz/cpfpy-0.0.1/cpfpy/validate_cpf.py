from cpfpy.utils.digits import get_check_digits, convert_to_digits, is_repeated, remove_non_digits

def validate_cpf(cpf_number: str) -> bool:
    """Validate a CPF number."""
    if not isinstance(cpf_number, str):
        raise("CPF is not a string.")

    unformatted_cpf = remove_non_digits(cpf_number)

    # Check if CPF has 11 digits and if it's not a repeated sequence
    if len(unformatted_cpf) != 11 or is_repeated(unformatted_cpf):
        return False

    digits = convert_to_digits(unformatted_cpf)
    check_digits = get_check_digits(digits)

    # Compare the calculated check digits with the provided ones
    return digits[9:] == check_digits