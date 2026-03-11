# SECTION: 1. What was broken when you started?
# BUG 1:
writing lower value than the guess give hint to input lower value and similarly higher value than the guess tells you to input higher value

# BUG 2:
you can input negative numbers and exceed the upper bound number with no error or warning. BUG 1 is also present here. Decimal numbers are truncated and accepted as correct guess.

# BUG 3:
easy has less attempts than medium and all the difficulties have the same range of numbers to guess from.

# BUG 4:
negative scores

# BUG 5:
reset logic (new game only resets attempt)

# BUG 6: 
state problems
