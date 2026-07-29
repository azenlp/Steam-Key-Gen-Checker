import random
import string

CHARS = string.ascii_uppercase + string.digits
GROUP_LENGTHS = [(5, 5, 5), (5, 5, 5, 5, 5)]

def generate_key(groups=3):
    if groups == 5:
        lengths = (5, 5, 5, 5, 5)
    else:
        lengths = (5, 5, 5)
    return "-".join(
        "".join(random.choices(CHARS, k=n)) for n in lengths
    )

def generate_keys(count=1, groups=3):
    return [generate_key(groups) for _ in range(count)]
