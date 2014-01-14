What is getpd
==============

The aim of getpd is to get the probability distribution of a **rule** inside a set of uniform data.


*N.B*: Getpd uses the version and the sintax provided from Python to handle **RegEX**.
       For the best use of getpd you have to know the (Slice)[http://en.wikipedia.org/wiki/Array_slicing#1991:_Python]
       notation which Python uses to handle the interval.

Known of the *rule*
==================

The way of getpd knows which patterns (or set of patterns) has to analyze is to pass it a *rule*.

Basically a rule is a pair of one **regular expression** and a **cut interval**.

The goal of getpd is to understand this rule and to search for all the datas that matches the regular expression, and - for
each tocket finded - it removes the symbols inside the interval provied and compute the probability compared to the set of uniform
data passed to it.

Getpd uses the interval to know which part of the token has to consider a possible *determination* and which is the pattern to
search.

With some example the powerfull of the rule to describe a *question* will be more clear:

e.g:
        1. Question: "Which density of probability follow the simbol after the literal 'n' in Italian?"

            A rule able to describe this question is the following: 'n.' [-1]
            Where, with the  'n.' we ask to getpd to match all the pair that start with 'n' and has any simbol next
            (i.e 'no', 'né', ...); with the interval [-1] we ask to getpd to consider the *last* char as the symbol
            that we want to know the probability distribution, and the remaining is the pattern that specify *where*
            we want to perform this analysis.

            To get the probability distribution that answer to the question you have to do only two things:
                1. Get a lot of data written in Italian
                2. Make a rule that describe your question

            In this example you have only to run this command:

                getpd 'n.' [-1] ITALIANDATA.txt ITALIANDATA2.txt

        2. Question: "Which density of probability follow the simbol after **any possible simbol** in Italian?"

            A rule to answer this question is still quite simple: '..' [-1]
            In this case getpd match any couple of simbols. The first character -that is any possible symbol-
            is *where* you perform the analysis; the last character is one of the all possible determinations.
            In this case you doesn't get only one result but a number of distribution of probability that depends
            of the number of simbols present in the alphabet of the information in analisys.

        3. Question: "How is the probability, in Italian, to have a word that start with a capitalized letter but
                      only inside the range A-D, that is at least long five char, to ends with an 'a' ?

             Yes, a complicated and unusefull question, but this demostrate the flexibility to use a RegEx with an
             interval and this is not all =)
             Well you can summarize into this rule: [A-D]([a-z]){3}. [-1]
             When you run the command you get the probability of the match [A-D]([a-z]){3} to have ANY possibile
             symbol. So to asnwer to the question you have only to look the probility of the simbol 'a'

What fuck I get when run this bullshit command?
==============================================

The output of the first command for example is something like this:

    A: {'a', 'b', 'c', 'd, 'e', 'f', 'g', 'd', 'e', 'f', ..., '1', '2', ... , ',', ...}

    'n.' [-1]: {0.0123, 0.002, 0.3, ...}

The first line is a all the symbols that getpd has finded (the alphabet of this information); the second line is the core of the
analysis: first block (left to the colon) is a memory of the rule used, the rest is the probability obtained. The first number
refer to the first simbol of the alphabet, the second to the second, and so on. =)

The output of the second command is more intresting; you get something like this:

    A: {'a', 'b', 'c', 'd, 'e', 'f', 'g', 'd', 'e', 'f', ..., '1', '2', ... , ',', ...}

    'a.' [-1]:  {0.0123, 0.002, 0.3, ...}
    'b.' [-1]:  {0.0123, 0.002, 0.3, ...}
    'c.' [-1]:  {0.0123, 0.002, 0.3, ...}
    'd.' [-1]:  {0.0123, 0.002, 0.3, ...}
    ...  ...
    ...  ...
    '1'  [-1]:  {0.0123, 0.002, 0.3, ...}
    ...  ...

How you can see here we have a lot of density of probability. This because the quadratic nature of the rule.
Getpd automatically make a new density of probabilty when it find a new element.
