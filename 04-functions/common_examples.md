# Common Mistakes — Functions

## 1. Reading f(x) as "f times x"

`f(x)` is function notation, not multiplication. `f(4)` means "evaluate the function `f` at input 4" — it does not mean `f` multiplied by `4`. This confusion is extremely common the first time function notation is introduced.

## 2. Dropping parentheses around a negative input

When substituting a negative number into a function, keep it in parentheses through every step.

Wrong: `f(x) = x²`, find `f(-3)` → `-3² = -9` ❌ (this computes `-(3²)`, not `(-3)²`)
Right: `f(-3) = (-3)² = 9` ✓

This is the exact same trap as `-2²` vs `(-2)²` from Module 01 — it just shows up again here because substitution reintroduces negative numbers into expressions with exponents.

## 3. Confusing "solve for x" with "evaluate f(x)"

These are opposite directions:
- **Evaluate:** you're given `x`, find the output. `f(4) = ?`
- **Solve:** you're given the output, find `x`. `f(x) = 11`, find `x`.

Mixing these up — for example, trying to "plug in 11" as if it were the input — leads nowhere. If the output is given and `x` is unknown, set up an equation and solve for `x` using the same tools from Module 02.

## 4. Forgetting to exclude domain restrictions

For `f(x) = 1/(x - 5)`, it's easy to just state "domain: all real numbers" out of habit, forgetting to check whether the denominator can hit zero. Before answering a domain question, always ask: **is there a denominator, and can it ever equal zero?**

## 5. Composing functions in the wrong order

`f(g(x))` and `g(f(x))` are generally **not** the same function. Always evaluate the *innermost* function first — the one closest to `x` — and use that result as the input to the outer function.

Wrong: for `f(g(3))`, evaluating `f(3)` first, then plugging that into `g` ❌
Right: evaluate `g(3)` first, then plug that result into `f` ✓

## 6. Forgetting to fully expand and simplify symbolic evaluations

When a problem asks for something like `f(a + 1)` in terms of `a`, it's not enough to just write `(a + 1)² - 2(a + 1)` and stop — that's substitution, not simplification. Expand and combine like terms to get a fully reduced expression (as in Module 02's distributing skills).

---

**Contributing?** Add mistakes you've actually seen or made — real confusion is more valuable here than hypothetical edge cases. See `CONTRIBUTING.md`.
