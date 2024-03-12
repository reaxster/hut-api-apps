import math
from app.lib.util.ProgressBar import progressBar
import time

def countdown(min, msg, suffix):
    # A List of Items
    items = list(range(0, math.floor(min * 60)))

    print(f" >> {msg}")

    # A Nicer, Single-Call Usage
    for item in progressBar(items, prefix=' >> Waiting:', suffix=suffix, length=50):
        # Do stuff...
        time.sleep(1)