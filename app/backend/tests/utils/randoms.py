import string
import random
from datetime import datetime

def random_string(length:int) -> str:
    chars=string.printable
    return ''.join(random.choice(chars) for _ in range(length))

def random_date(start:datetime=datetime.min, end:datetime=datetime.max) -> datetime:
    # Get a random amount of seconds between `start` and `end`
    diff = random.randint(0, int((end - start).total_seconds()))
    return start + datetime.timedelta(seconds=diff)

