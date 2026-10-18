
# 04 — Functions

Everything so far has been about solving for `x`. This module shifts the question slightly: instead of "what value of `x` makes this true," a function asks "what output do I get for a given input?" That shift in thinking is the foundation for almost everything in math after algebra.

## 1. What is a function

A function is a rule that takes an input and produces **exactly one** output for that input. Think of it like a machine: you feed in a number, it does something to it, and exactly one number comes out.

The everyday example: `y = 2x + 3` is a function. For every value of `x` you put in, there's one specific value of `y` that comes out — never two different answers for the same input.

**Not a function example:** if a rule said "input 4 could give either 2 or -2," that's not a function — a single input mapping to more than one output breaks the definition.

## 2. Function notation

Instead of writing `y = 2x + 3`, functions are usually written as:

```
f(x) = 2x + 3
```

Read this as **"f of x"** — it does *not* mean "f times x." The name `f` is just a label for the function (you could call it `g`, `h`, or anything else), and `(x)` shows what the input variable is called.

`f(x) = 2x + 3` and `y = 2x + 3` describe the exact same relationship — function notation just makes it explicit which variable is the input.

## 3. Evaluating a function

To evaluate `f(4)`, substitute `4` everywhere you see `x` in the function's definition.

**Example:** `f(x) = 2x + 3`, find `f(4)`
```
f(4) = 2(4) + 3 = 8 + 3 = 11
```

So `f(4) = 11` — meaning "when the input is 4, the output is 11."

## 4. Domain: what inputs are allowed

The **domain** of a function is the set of all inputs that are valid for it. For most functions you've seen so far (like `f(x) = 2x + 3`), any real number works — the domain is "all real numbers."

But some functions have restrictions. The most common one at this stage: **you can never divide by zero.**

**Example:** `f(x) = 1/(x - 2)`

If `x = 2`, the denominator becomes `2 - 2 = 0`, and division by zero is undefined. So `x = 2` is **not** in the domain.

**Domain: all real numbers except x = 2** — written as `x ≠ 2`.

(You'll meet more domain restrictions — square roots of negative numbers, for instance — once you reach the Exponents & Radicals module. For now, the division-by-zero check is the one to master.)

## 5. Range: what outputs are possible

The **range** is the set of all possible outputs a function can produce. This is often harder to determine just by looking at the equation — it usually helps to think about the function's graph, which is covered in more depth in later modules once you've built up more tools.

## 6. Function composition (a quick preview)

Sometimes you plug the output of one function into another. `f(g(x))` means: first evaluate `g(x)`, then plug *that result* into `f`.

**Example:** `f(x) = 2x + 1`, `g(x) = x - 4`. Find `f(g(3))`.

**Step 1:** Evaluate the inside function first: `g(3) = 3 - 4 = -1`
**Step 2:** Plug that result into `f`: `f(-1) = 2(-1) + 1 = -1`

So `f(g(3)) = -1`. Order matters here — `f(g(x))` and `g(f(x))` are usually different functions entirely.

## What's next

Once evaluating functions, checking domain restrictions, and basic composition feel comfortable, move on to `05-polynomials`, where you'll work with functions that have multiple terms and higher powers of `x`.

See `worked-examples.md` for more step-by-step problems, and `common-mistakes.md` before starting the practice set.
