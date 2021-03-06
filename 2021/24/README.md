# AoC 2021/24

Welp. Took more than 24 hours (not straight coding time, I've been spending some time with the fam for the holiday.)

Am I proud of the code here? Some of it, yes. Some of it, not so much.

Some working out I did is recorded [later in this README](#arithmetic-hand-work).

## Some Description of the Process
### Code/Automation
I started with a super naive brute force, just walk backwards from 99999999999999 and run the full instructions on each number until you get a success.

While that was slowly trodding along, I thought about optimizations - first the somewhat obvious ones like pre-computing operations with only constants and reducing identity expressions (e.g. `var1 * 0` ā `0`).

Around this phase, I figured it would be easier to debug if I had a graph representation of the expression to be evaluated. So I quickly refreshed my [DOT language](http://graphviz.org/doc/info/lang.html) skills so that I could use [graph-easy](https://github.com/ironcamel/Graph-Easy) to render the graph in the terminal for ease in testing. This wasn't too cumbersome, but it was my first install after recently setting up WSL, so it took a little while longer than it perhaps should have.

The graph form actually helped me see that \[a\] distributive rule~~s~~ would actually be helpful. That started making the reduction logic even more ugly, and I was starting to not like it.

It was at this point that I recognized I already had a pretty decent compiler on hand: `gcc`. At this point, programmatically translating the input to fairly concise C code was relatively easy. So I spun that up, and it was cranking through much faster! This solution would be able to search through the entire space in a mere handful of weeks, and likely get the highest valid model# by morning tomorrow!

But I was unsatisfied with this, knowing that there was a faster solution. Thus began the arithmetic.

### Arithmetic/Hand Work

The variables (vā and dā) referenced here are as noted in `monad.c` (as produced by `sol.py` for my input), and references to those statements will be labeled as [Cxx] where xx is the line number.

We are looking for constraints on possible bindings for all `d` that result in the monad function returning 0, i.e.
```
 0. 0 = (vāā//26)*(1+25vāā) + (dāā+2)vāā      [C18]
```
Additional useful constraints derived from the problem description with minimal workings-out:
```
 1. 1 ā¤ dā ā¤ 9 | 0 ā¤ x ā¤ 14
 2. vā ā {0,1} | x ā {9,26,40,54,65,76,87}
```
A short proof by contradiction showed that vāā must be 0:
```
 |   3. vāā ā  0                          []
 |   4. vāā = 1                          [3, 2]
 |   5. 0 = (vāā//26)*(26) + (dāā+2)      [0, 4, sub.]
 |   6. vāā//26 = (dāā+2)/26              [5]
 |   7. 3/26 ā¤ vāā//26 ā¤ 11/26           [6, 1]
 |   8. vāā//26 ā ā¤                      [7]
 |   9. vāā//26 ā ā¤                      [// prop.]
10. vāā = 0                          [pbc]
```

And we're off! This is looking good, we have a strong conclusion for one of our unknowns! Unfortunately, the working out is far less clean beyond this first conclusions, and only resulted in possible ranges of values, not specific values, for the unknown variables and digits.

So I started working from the other side `[C4]`, seeing if anything better would come of it. As I was doing this working out, the operations began to feel strangely familiar...this is you would read a number in base 26!

Armed with this realization and a good bit of reasoning power, the lines in the monad function began to make perfect sense! And I could finally thank myself for the work I did earlier with reductions in expressions, as I'm fairly certain that the difficulty in interpretation would have been much higher without the reductions.

Without too much detail into the proofs or what operations are which, the main operations performed in the evaluation are adding a base26 digit to a number, getting the last base26 digit, comparing the difference between two digits to a fixed delta, and conditionally adding a digit based on the truthiness of a previous comparison.

After translating the operations, you can express the intermediate variables relatively easily as base26 numbers and inequality comparisons. Adding digits is sometimes conditional on previous comparisons, these are enclosed in `[]`s:
```
v4 = <dā+8,dā+8,dā+12>

vā = inequal?(dā, dā+12-8)

vāā = <dā+8,dā+8[,dā+10],dā+2,dā+8>

vāā = inequal?(dā, dā+8-11)

vāā = <dā+8,dā+8[,dā+10],dā+2[,dā+4],dā+9>

vāā = inequal?(dā, dā+9-3)

vāā = <dā+8,dā+8[,dā+10],dā+2[,dā+4][,dā+10],dā+3>

vāā = inequal?(dāā, dā+3-3)

vāā = <dā+8,dā+8[,dā+10],dā+2[,dā+4][,dā+10][,dā0+7]>
```

At this point, the expressions for these variables would become even more complicated. However, the last value must be 0, which means vāā must be one (base26) digit, vāā must be two digits, and vāā three. So all the optional digits must be unset, meaning that all the `inequal?` values must be false, and thus we arrive at a list of necessary equalities:
```
dā = dā+4
dā = dā-3
dā = dā+6
dāā = dā
dāā = dā+1
dāā = dā-2
dāā = dā-8
```
From these equalities, finding the largest number composed of these digits is nearly trivial - for each pair of digits in an equality, set the larger to 9 and the smaller to satisfy the equality. Finding the smallest number is very similar.

## Final Thoughts

As I get to this section, I'm wondering why wrote this the way I did. And how to appropriately end