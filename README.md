Getpd
=====

The aim of getpd is to get the probability distribution (*GetProbabilityDistribution*) of a **rule** inside a set of uniform data.

**N.B**: Getpd actually is under design. If you want to see the code and pull a request, see the branch 'dev'.

Known of the *rule*
==================

The way in which getpd knows which patterns (or set of patterns) has to analyze is to pass to it a *rule*.  
Basically a rule is composed by one **regular expression** and a **cut interval**.  
The goal of getpd is to filter the data passed to it through the RegEX and -for each token found- to isolate one possible *Determination* from data necessary only to describe where it has to perform the analisys (this thanks the cut interval) and store all this possibles results inside a *Random Variable*.

The syntax of the rule is quite simple: \[**Regex**][**cut interval**]

*N.B*: getpd uses the version and the syntax provided from Python to handle the RegEX.
       The cut interval is provided through the [Slice](http://en.wikipedia.org/wiki/Array_slicing#1991:_Python)     notation which Python uses to handle the intervals.

Examples
========

__Question__: "*Which density of probability follow the symbols after the literal 'n' in Italian?*"

To answer this question, in mathematical terms, you have to compute the *conditional probability* of the event *A* `'any symbols'` assuming that the event *B* `'symbol n'` has occured.

A rule able to describe this question is the following: `[n.][-1]`

With the RegEX `n.` inside the first square brackets, we ask to getpd to match all the pair which start with 'n' (the B event) and have any symbol after it (the A event), i.e: 'no', 'na', ... .  
With the interval `[-1]` we ask to getpd to consider the *last* character of any matches such as a possibile determination of the Random Variable *n.*.

When you have made a rule that describe your question, you have only to get a lot of data written in Italian to analyze.

In this example you have only to run this command:

    getpd [n.][1] ITALIANDATA.txt ITALIANDATA2.txt

__Question__: "*Which density of probability follow the symbols after* **any possible symbol** *in Italian?*"

A rule to answer this question is still quite simple: `[..][-1]`

In terms of conditional probability the events are A:'any symbols' assuming that the event B:'any symbols' has occured.

You can notice that the *condition* B is dynamic and this implies that the answer to this question is a bidimensional Random Value.

__Question__: "*What is the probability, in Italian, that the fifth character in a word is an 'a' if I know that the first character is an uppercase letter inside the range A-D?*"

Yes, a complicated and maybe unuseful question, but this demonstrate the flexibility to use a RegEx with an interval.

You can summarize into this rule: `[[A-D]([a-z]){3}.][-1]`

In the density of probability that you obtain, you have only to look what is the probability assigned to the character 'a' to solve your question.

What I get when I run this command?
===================================

The output of the first command for example is something like this:

    A: {'a', 'b', 'c', 'd, 'e', 'f', 'g', 'd', 'e', 'f', ..., '1', '2', ... , ',', ...}
    
    ['n.'][-1]: {0.0123, 0.002, 0.3, ...}

The first line is the set of the symbols that getpd has found (the alphabet of this information / the sample space of the Random Variable).  
The second line contains a memory of the rule used (and the *"name"* of the Random Variable), and the probability computed.

The first number refer to the first symbol of the alphabet, the second to the second, and so on.

When should I use getpd?
========================

Basically you can use getpd whenever you have to perform analysis of a *pattern* inside an Information.  
This is usefull if you want to bring out statistical dependecy between subset of an information (such as grammar rule in a Language) or to analyze an unknown information.

The first goal of this software is to provide a tool to bring out as much as possible statistical information in a set of data and to use it to optimize a compression through the Huffman coding.

However there are other situations where you can use this tool:

1. Cryptanalysis (see: [Frequency Analysis](http://en.wikipedia.org/wiki/Frequency_analysis))
2. Compute statistics inside uniform data
3. Test PRGN
4444. Answer stupid question like the example above
