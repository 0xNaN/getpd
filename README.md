What is getpd
==============

The aim of getpd is to get the probability distribution of a patterns (or a rule) inside a set of uniform data.


Rule
====

The way of getpd to know which patterns (or set of patterns) has to analyze is to pass it a *rule*.

Basically a rule is a pair of one **regular expression** and a **cut interval**.
The goal of getpd is to understand this rule and to search for all the datas that matches the regular expression, and - for
each tocket finded - it removes the symbol inside the interval and compute the probability compared to the set of uniform
data passed to it.

e.g :
    A.txt, B.txt and C.txt are three long files written in Italian.
    we want to answer questions like this: "Which density of probability follow the symbols after the literal 'n' in Italian?"

    Answer this question with getpd is quite easy. You have to do only two thing:

        1. Find a lot of datas all written in Italian
        2. Make a rule that explain your question

    In this case you can run this command:

        getpd 'n.' [0] A.txt B.txt C.txt

    In this command the pair: 'n.' [0:], is the *rule*.
    It says: well, find all the data that matches the RegEx 'n.' (e.g the the word 'no', the pair 'né', ...), for each token
    **remove** the symbols in the interval [0:] - only the first character 'n' - the result is a data that
    the information in exams *allow*, so put in a table (if is the first time that you see it) and compute the probability of
    this patterns in all the data available.

    When getpd is done, you get an answer like this:

    A: {'a', 'b', ... }

    'n.' [0] : {0.113, 0.500, ... }

    The first line is the alphabeth that getpd has findend. The second line is the rule used with a list of the result :)

