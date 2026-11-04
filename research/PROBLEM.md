# Erdős Problem 902

## Source

Canonical page: <https://www.erdosproblems.com/902>

The statement below is the text returned by the indexed page on 23 October 2026. A direct fetch of the HTML timed out in this session, so the quotation is from that indexed text, not from a freshly rendered browser view. The same wording appears on the indexed LaTeX page <https://www.erdosproblems.com/latex/902>. The indexed proof-claims thread <https://www.erdosproblems.com/forum/thread/902/proof-claims> said: "No proof claims have been submitted yet."

## Statement

> Let \(f(n)\) be minimal such that there is a tournament (a complete directed graph) on \(f(n)\) vertices such that every set of \(n\) vertices is dominated by at least one other vertex. Estimate \(f(n)\).

Schütte asked Erdős this in the early 1960s. The page records \(f(1) = 3\) and \(f(2) = 7\), Erdős (1963) for \(2^{n+1} - 1 \le f(n) \ll n^2 2^n\), and Szekeres–Szekeres (1965) for \(f(3) = 19\) and \(n 2^n \ll f(n)\).

## Definitions used in this repository

A **tournament** is a directed graph on a vertex set \(V\) in which every unordered pair of distinct vertices carries exactly one directed edge. Write \(u \to v\) when \(u\) beats \(v\).

For \(X \subseteq V\), the **dominator set** is

\[
D(X) = \{ w \in V \setminus X : w \to x \text{ for every } x \in X \}.
\]

\(X\) is **dominated** when \(D(X)\) is nonempty. The tournament has **property \(S_n\)** when every \(n\)-element set is dominated. Then

\[
f(n) = \min \{ |V| : \text{some tournament on } V \text{ has } S_n \}.
\]

Equivalently, \(S_n\) says that the domination number of the tournament is greater than \(n\): no set of \(n\) vertices meets every out-star in the sense of Moon's domination number. The repository uses the dominator formulation above, and every proof in `proof/` is about that formulation.

\(N^+(v)\), \(N^-(v)\), \(d^+(v)\) and \(d^-(v)\) are the out-set, in-set, out-degree and in-degree of \(v\).

## What "resolved" means here

The problem asks for an estimate of \(f(n)\). A complete resolution would pin down the order of \(f(n)\), which is still open between the shapes \(n \cdot 2^n\) and \(n^2 \cdot 2^n\), or would determine \(f(4)\) exactly. A partial theorem is recorded only as a partial theorem.

This file does not adopt unpublished bounds from `proof/` as part of the problem statement. Those claims are catalogued in `LEMMAS.md` with their verification status.
