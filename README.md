mtspell
=======

A spelling correction tool that uses source side information to make better suggestions.

When post-editing MT output a translator may introduce spelling mistakes. 
This project tries to find these and to offer good suggestions which take into account the context as well the
source side that was used for the initial suggestion.

Common tools for spelling correction look at each word individually, compare the word to a dictionary of known words, and suggest another word with low edit distance or similar pronounciation if the word is unknown. More advanced spelling correction as applied by search engines can take the sentence context into account (think language model) to produce a more helpful suggestion.

In the special case where we know that the text at hand is the translation of a given source sentence this information is likely to be very helpful to produce even better translation and to spot real-word errors when the wrong word appears in the dictionary, e.g. 'from' vs. 'form'.
