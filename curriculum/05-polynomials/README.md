# 05 — Polynomials

So far every expression has had at most one or two terms with `x` to the first power. A polynomial is what you get when you allow **multiple terms** and **higher powers of x** in the same expression. This module covers what polynomials are, how to add/subtract them, and how to multiply them — factoring them comes next, in Module 06.

## 1. What is a polynomial

A polynomial is a sum of terms, where each term is a number (a **coefficient**) times a variable raised to a whole-number power. For example:

```
3x² - 5x + 2
```

This has three **terms**: `3x²`, `-5x`, and `2`.

- The **coefficient** of a term is the number multiplying the variable (`3` and `-5` above; `2` is a constant term with no variable).
- The **degree** of a term is the exponent on its variable (`x²` has degree 2, `-5x` has degree 1, `2` has degree 0).
- The **degree of the polynomial** is the highest degree among its terms — so `3x² - 5x + 2` has degree 2.

**Standard form** means writing terms from highest degree to lowest, left to right — exactly how the example above is written.

## 2. Classifying polynomials

By number of terms:
- **Monomial** — one term (`5x²`)
- **Binomial** — two terms (`x + 7`)
- **Trinomial** — three terms (`x² - 5x + 2`)
- Four or more terms is just called a "polynomial with n terms"

By degree:
- Degree 1 — **linear** (`2x + 3`)
- Degree 2 — **quadratic** (`x² - 4`)
- Degree 3 — **cubic** (`x³ + 2x`)

## 3. Adding and subtracting polynomials

This is exactly the "combine like terms" skill from Module 01 — **like terms** are terms with the same variable raised to the same power (`3x²` and `5x²` are like terms; `3x²` and `3x` are not).

**Example — adding:** `(3x² + 2x - 5) + (x² - 4x + 7)`

Group like terms together: `(3x² + x²) + (2x - 4x) + (-5 + 7)`
Combine: `4x² - 2x + 2`

**Example — subtracting:** `(5x² - 3x + 1) - (2x² + 4x - 6)`

Subtracting means distributing a `-1` across every term in the second polynomial first:
`5x² - 3x + 1 - 2x² - 4x + 6`
Then group and combine: `(5x² - 2x²) + (-3x - 4x) + (1 + 6) = 3x² - 7x + 7`

**The subtraction step is the #1 place people slip up** — forgetting to flip the sign on *every* term in the second polynomial, not just the first one. See `common-mistakes.md`.

## 4. Multiplying a polynomial by a monomial

Distribute the monomial across every term, exactly like distributing a number in Module 02 — just with variables and exponents added in.

**Example:** `3x(2x² - 5x + 4)`
```
3x · 2x² = 6x³
3x · (-5x) = -15x²
3x · 4 = 12x
```
Result: `6x³ - 15x² + 12x`

**Remember the exponent rule for multiplication:** `xᵃ · xᵇ = xᵃ⁺ᵇ` (add the exponents). This gets covered in more depth in Module 08, but you'll use it constantly here.

## 5. Multiplying two binomials (FOIL)

**FOIL** stands for **F**irst, **O**uter, **I**nner, **L**ast — a way to remember which pairs of terms to multiply when multiplying two binomials together.

**Example:** `(x + 3)(x - 5)`

- **First:** `x · x = x²`
- **Outer:** `x · (-5) = -5x`
- **Inner:** `3 · x = 3x`
- **Last:** `3 · (-5) = -15`

Add them all together: `x² - 5x + 3x - 15`
Combine like terms: `x² - 2x - 15`

FOIL is really just the distributive property applied twice — it works because `(x+3)(x-5)` means "distribute `(x-5)` across both terms of `(x+3)`."

## What's next

Once combining polynomials and multiplying them (including FOIL) feel routine, move on to `06-factoring`, which is essentially FOIL run in reverse — starting from the expanded form and working backward to find the original factors.

See `worked-examples.md` for more step-by-step problems, and `common-mistakes.md` before starting the practice set.
