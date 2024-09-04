import secrets
import string


generator = secrets.SystemRandom()


def randint() -> int:
    """Возвращает случайное 64-битное целое.

    От 1 до 9223372036854775807.
    """
    return generator.randint(1, 2**63 - 1)


def randstr(length: int = 10) -> str:
    return ''.join(generator.choices(string.ascii_uppercase + string.digits, k=length))
