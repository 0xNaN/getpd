What is getpd
==============

The aim of getpd is to get the probability distribution (*GetProbabilityDistribution*) of a **rule** inside a set of uniform datas.


*N.B*: Getpd uses the version and the sintax provided from Python to handle **RegEX**. <br>
For the best use of getpd you have to know the [Slice](http://en.wikipedia.org/wiki/Array_slicing#1991:_Python) Notation which Python uses to handle the intervals.

Known of the *rule*
==================

The way in which getpd knows which patterns (or set of patterns) has to analyze is to pass to it a *rule*.

Basically a rule is composed by one **regular expression** and a **cut interval**.

The goal of getpd is to understand this rule and to looking for all the datas that matches the regular expression and - for each tocket found - it removes the symbols inside the interval provided and computes the probability compared to the set of uniform datas passed to it.

Getpd uses the interval to know which of the token parts has to consider as a possible *determination* and which is the pattern that have to search (the *Random Variable*).

With some example the powerfull of the rule to describe a *question* of probability will be more clear:

e.g:

1. Question: "*Which density of probability follow the symbol after the literal 'n' in Italian?*"

     A rule able to describe this question is the following: 'n.' [-1]

     With the RegEX *'n.'* we ask to getpd to match all the pair which start with 'n' and have any symbol after it (i.e 'no', 'na', ...); with the interval [-1] we ask to getpd to consider the *last* char as the symbol of which we want to know the probability distribution ('o' and 'a' are possibles determinations) and the remaining is the pattern that specify *where* we want to perform this analysis (the Random Variable).

     To get the probability distribution that answer to the question you have to do only two things:

   1. Get a lot of data written in Italian
   2. Make a rule that describe your question

    In this example you have only to run this command:

            getpd 'n.' [-1] ITALIANDATA.txt ITALIANDATA2.txt

2. Question: "*Which density of probability follow the symbols after* **any possible symbol** *in Italian?*"

    A rule to answer this question is still quite simple: '..' [-1]

    In this case getpd match any couple of symbols.
    The first character -that is any possible symbol- is *where* you perform the analysis; the last character is one of the all possible determinations.

    In this case you don't get only one result but a number of distribution of probability that depends of the number of symbols     present in the alphabet of the information in analisys.

3. Question: "*How is the probability, in Italian, to have a word which starts with a capitalized letter but only inside the range A-D, that is at least long five char, to ends with an 'a'?*"

    Yes, a complicated and unusefull question, but this demonstrate the flexibility to use a RegEx with an interval and this is not all =)

    Well you can summarize into this rule: '\[A-D]([a-z]){3}.' [-1]

    When you run the command you get the probability of the match \[A-D]([a-z]){3} to have **ANY** possibile symbols.

    So to answer to the question you have only to look to the probability of the symbol 'a'.

4. Question: "*Which density of probability follow two literals between the pair 'sh' and 'on' in English?*"

    A rule to describe this question show an advanced use of the Intervals.

    For example you can use this rule: 'sh..on' [2:4]

    With [2:4] you specify that the portion '..' has to be considered as a determination, while the rest 'sh' 'on' is the condition in the question.
    For example: the word "sharon" matches the regex, so in the result you will probably have (to understand the following output read *What I get when I run this command*):

        A: {'aa', 'ab', ..., 'on', ...}

        'sh..on' [2:4] : {..., ..., ..., 0.01234, ...}

    the number 0.01234 will be the probabilty of having the word 'sharon' in the English if you have analized a **big quantity**
    of english Data.

What I get when I run this command?
===================================

The output of the first command for example is something like this:

    A: {'a', 'b', 'c', 'd, 'e', 'f', 'g', 'd', 'e', 'f', ..., '1', '2', ... , ',', ...}

    'n.' [-1]: {0.0123, 0.002, 0.3, ...}

The first line is the set of the symbols that getpd has found (the alphabet of this information); the second line is the heart of the analysis: first block ( left to the colon) is a memory of the rule used (and the *"name"* of the Random Variable), the rest is the probability obtained.
The first number refer to the first symbol of the alphabet, the second to the second, and so on. =)

The output of the second command is more intresting; you get something like this:

    A: {'a', 'b', 'c', 'd, 'e', 'f', 'g', 'd', 'e', 'f', ..., '1', '2', ... , ',', ...}

    'a.' [-1]:  {0.0123, 0.002, 0.3, ...}
    'b.' [-1]:  {0.0123, 0.002, 0.3, ...}
    'c.' [-1]:  {0.0123, 0.002, 0.3, ...}
    'd.' [-1]:  {0.0123, 0.002, 0.3, ...}
    ...  ...
    ...  ...
    '1.'  [-1]:  {0.0123, 0.002, 0.3, ...}
    ...  ...

How you can see here we have a lot of density of probability. This because of the quadratic nature of the rule.

Getpd automatically make a new density of probabilty when it find a new element.

When should I use getpd?
========================

Basically you can use getpd whenever you have to perform analysis of a *pattern* inside an Information.

The first goal of this software is to help another project: build a compressor that takes full advantage of the Huffman coding.

However there are other situations where you can use this tool:

1. Cryptanalysis (see: [Frequency Analysis](http://en.wikipedia.org/wiki/Frequency_analysis))
2. Compute statistics inside uniform data
3. Answer stupid question like the example above
