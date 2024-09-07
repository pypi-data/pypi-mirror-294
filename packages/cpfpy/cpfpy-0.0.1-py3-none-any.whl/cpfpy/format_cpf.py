# Format a CPF number
def format_cpf(cpf_number: str):
  if not isinstance(cpf_number, str):
    raise ValueError('Invalid CPF number')

  unformatted_cpf = ''.join(filter(str.isdigit, cpf_number))

  if len(unformatted_cpf) != 11:
      raise ValueError('Invalid CPF number')

  return f'{unformatted_cpf[:3]}.{unformatted_cpf[3:6]}.{unformatted_cpf[6:9]}-{unformatted_cpf[9:]}'