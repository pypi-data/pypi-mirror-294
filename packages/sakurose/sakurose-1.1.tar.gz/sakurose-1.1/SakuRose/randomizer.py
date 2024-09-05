import random
import string

generated_numbers = []
generated_strings = []

def random_number(min_value, max_value, unique=False):
    """Genera un número aleatorio, con opción de evitar repetición."""
    num = random.randint(min_value, max_value)
    if unique:
        while num in generated_numbers:
            num = random.randint(min_value, max_value)
        generated_numbers.append(num)
    return num

def random_string(length, unique=False):
    """Genera una cadena aleatoria, con opción de evitar repetición."""
    letters = string.ascii_letters + string.digits
    rand_str = ''.join(random.choice(letters) for _ in range(length))
    if unique:
        while rand_str in generated_strings:
            rand_str = ''.join(random.choice(letters) for _ in range(length))
        generated_strings.append(rand_str)
    return rand_str