# 06 — Factoring

In Module 05 you multiplied polynomials out: `(x + 3)(x - 5)` became `x² - 2x - 15`. Factoring is that exact process **run backward** — you start with the expanded form and find the pieces that were multiplied together.

Why bother? Because factored form makes problems much easier to solve (Module 09 on quadratics depends on it completely) and it's essential for simplifying fractions with variables (Module 07).

**Always check your work:** multiply your factors back out. If you get the original expression, you're right.

## 1. Factoring out the GCF (Greatest Common Factor)

Always try this **first**, before anything else. Find the largest number and the highest power of `x` that divides evenly into every term, and pull it out front.

**Example:** `6x³ + 9x² - 12x`
- Numbers: the GCF of 6, 9, 12 is `3`
- Variables: every term has at least one `x`, so `x` is common
- GCF = `3x`
- Divide each term by `3x`: `2x²`, `3x`, `-4`

```
6x³ + 9x² - 12x = 3x(2x² + 3x - 4)
```

## 2. Factoring trinomials of the form x² + bx + c

Here the leading coefficient is 1. You're looking for **two numbers that multiply to `c` and add to `b`**.

**Example:** `x² + 7x + 12`
- Need two numbers that multiply to `12` and add to `7`
- `3 × 4 = 12` and `3 + 4 = 7` ✓

```
x² + 7x + 12 = (x + 3)(x + 4)
```

**With negatives:** `x² - 2x - 15`
- Multiply to `-15`, add to `-2`
- Since the product is negative, one number is positive and one is negative
- `-5 × 3 = -15` and `-5 + 3 = -2` ✓

```
x² - 2x - 15 = (x - 5)(x + 3)
```

**Sign shortcuts:**
- `c` positive, `b` positive → both numbers positive
- `c` positive, `b` negative → both numbers negative
- `c` negative → one positive, one negative (the larger one takes the sign of `b`)

## 3. Difference of squares

Remember `(x - 6)(x + 6) = x² - 36` from Module 05, where the middle terms cancelled out? Run it backward:

```
a² - b² = (a - b)(a + b)
```

**Example:** `x² - 49 = (x - 7)(x + 7)`

This only works for a **difference** (subtraction) of two perfect squares. `x² + 49` does **not** factor this way.

## 4. Perfect square trinomials

Also from Module 05: `(x + 5)² = x² + 10x + 25`. Running it backward:

```
a² + 2ab + b² = (a + b)²
a² - 2ab + b² = (a - b)²
```

**How to spot one:** the first and last terms are perfect squares, and the middle term is twice the product of their square roots.

**Example:** `x² + 10x + 25` → `x²` is `x·x`, `25` is `5·5`, and the middle `10x = 2·x·5` ✓ → `(x + 5)²`

## 5. Trinomials with a leading coefficient: ax² + bx + c

When `a` isn't 1, use the **"ac method"**:

**Example:** `2x² + 7x + 3`
1. Multiply `a · c = 2 · 3 = 6`
2. Find two numbers that multiply to `6` and add to `b = 7`: `1` and `6`
3. Split the middle term using those numbers: `2x² + 1x + 6x + 3`
4. Group in pairs and factor each: `x(2x + 1) + 3(2x + 1)`
5. Factor out the common binomial `(2x + 1)`: `(2x + 1)(x + 3)`

**Check by FOIL:** `(2x + 1)(x + 3) = 2x² + 6x + x + 3 = 2x² + 7x + 3` ✓

## The factoring checklist

Run through these in order every time:
1. **GCF first** — can anything be pulled out of every term?
2. **Count the terms.** Two terms → difference of squares? Three terms → trinomial methods above.
3. **Check if it factors further** — sometimes a factor can be broken down again (e.g., `2x² - 18 = 2(x² - 9) = 2(x - 3)(x + 3)`).
4. **Multiply back** to verify.

## What's next

Once factoring feels natural, move on to `07-rational-expressions`, where factoring lets you simplify fractions containing variables — and then on to Module 09, where factoring is the main tool for solving quadratic equations.

See `worked-examples.md` for more step-by-step problems, and `common-mistakes.md` before starting the practice set.
