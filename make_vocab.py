#!/usr/bin/env python
import sys
from collections import defaultdict
import re

def tokens(text):
    """List all the word tokens (consecutive letters) in a text.
    Normalize to lowercase."""
    return re.findall('[a-z]+', text.lower())

counts = defaultdict(int)
for line in sys.stdin:
    for w in tokens(line.strip()):
        counts[w] += 1

for w in counts:
    sys.stdout.write("%s\t%s\n" %(w, counts[w]))
