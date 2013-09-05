mtspell
=======

A spelling correction tool that uses source side information to make better suggestions.

When post-editing MT output a translator may introduce spelling mistakes. 
This project tries to find these and to offer good suggestions which take into account the context as well the
source side that was used for the initial suggestion.

Common tools for spelling correction look at each word individually, compare the word to a dictionary of known words, and suggest another word with low edit distance or similar pronounciation if the word is unknown. More advanced spelling correction as applied by search engines can take the sentence context into account (think language model) to produce a more helpful suggestion.

In the special case where we know that the text at hand is the translation of a given source sentence this information is likely to be very helpful to produce even better translation and to spot real-word errors when the wrong word appears in the dictionary, e.g. 'from' vs. 'form'.

Example:
--------

Here is some simple but working example:

Consider this input:

a simpel tsk .

We look up each word in a dictionary and hypothesize all words that are further than edit distance 2 away.

For example simpel can be a misspelling of either:

simple, simmer, gimpel ...

We keep the edit distance and the log-count of the word as features. Then writing the hypergraph format as defined here [2] gives us something like this:

$ echo 'a simpel tsk' | ./spell.py > 0
$ cat 0
5 5056
1
<s> |||
2467
[0] a ||| Distance=0 LogCount=15.533660
[0] aa ||| Distance=1 LogCount=8.027150
[0] ac ||| Distance=1 LogCount=7.979681
[0] ae ||| Distance=1 LogCount=5.669881
[0] ad ||| Distance=1 LogCount=9.257796
[0] ag ||| Distance=1 LogCount=7.915713
[0] af ||| Distance=1 LogCount=6.226537
[0] ai ||| Distance=1 LogCount=7.402452
[0] ah ||| Distance=1 LogCount=7.742402
[0] ak ||| Distance=1 LogCount=7.068172
[0] aj ||| Distance=1 LogCount=6.437752
[0] am ||| Distance=1 LogCount=10.883072
[0] al ||| Distance=1 LogCount=10.599107
[...]
[2] nbk ||| Distance=2 LogCount=2.890372
[2] bpk ||| Distance=2 LogCount=1.098612
[2] hsm ||| Distance=2 LogCount=4.007333
[2] hsr ||| Distance=2 LogCount=3.178054
[2] hsp ||| Distance=2 LogCount=3.610918
1
[3] </s> |||

(the vocab I used is a bit rubbish but the thing is quite resiliant)

Then stick the graph into Ken's decoder and provide some weights:

$./decode --graph_dir /path/spellcheck/ \
  --beam 100 \
  --lm /path/spellcheck/eng.kenlm
  --weight WordPenalty=-1.0 LanguageModel=1 Distance=-1 LogCount=.1 LanguageModel_OOV=0

and voila:

0 |||  a simple task  ||| Distance=3 LogCount=34.8875 LanguageModel=-7.08252 LanguageModel_OOV=0 WordPenalty=-2.17147 ||| -4.4223
