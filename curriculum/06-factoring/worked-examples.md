# Worked Examples — Factoring

Cover the solution and try each one yourself first. Always verify by multiplying back out.

---

### Example 1: Factoring out the GCF
**Problem:** Factor `6x³ + 9x² - 12x`

**Step 1:** Find the GCF of the coefficients: GCF of 6, 9, 12 is `3`
**Step 2:** Find the common variable part: every term has at least `x`, so `x`
**Step 3:** GCF = `3x`. Divide each term by it: `6x³ ÷ 3x = 2x²`, `9x² ÷ 3x = 3x`, `-12x ÷ 3x = -4`
**Step 4:** Write the result: `3x(2x² + 3x - 4)`

**Check:** `3x · 2x² = 6x³`, `3x · 3x = 9x²`, `3x · (-4) = -12x` ✓

**Answer: 3x(2x² + 3x - 4)**

---

### Example 2: Simple trinomial (positive terms)
**Problem:** Factor `x² + 7x + 12`

**Step 1:** Find two numbers that multiply to `12` and add to `7`
**Step 2:** Try pairs: `1·12` (sum 13), `2·6` (sum 8), `3·4` (sum 7) ✓
**Step 3:** Write the factors: `(x + 3)(x + 4)`

**Check (FOIL):** `x² + 4x + 3x + 12 = x² + 7x + 12` ✓

**Answer: (x + 3)(x + 4)**

---

### Example 3: Trinomial with a negative constant
**Problem:** Factor `x² - 2x - 15`

**Step 1:** Need two numbers that multiply to `-15` and add to `-2`
**Step 2:** The product is negative, so one number is positive and one is negative. Try: `-5` and `3` → product `-15`, sum `-2` ✓
**Step 3:** Write the factors: `(x - 5)(x + 3)`

**Check (FOIL):** `x² + 3x - 5x - 15 = x² - 2x - 15` ✓

**Answer: (x - 5)(x + 3)**

---

### Example 4: Difference of squares
**Problem:** Factor `x² - 49`

**Step 1:** Recognize the pattern: `x²` is a perfect square, `49 = 7²` is a perfect square, and they're being subtracted
**Step 2:** Apply `a² - b² = (a - b)(a + b)` with `a = x`, `b = 7`

**Check:** `(x - 7)(x + 7) = x² + 7x - 7x - 49 = x² - 49` ✓

**Answer: (x - 7)(x + 7)**

---

### Example 5: Leading coefficient other than 1 (the ac method)
**Problem:** Factor `2x² + 7x + 3`

**Step 1:** Multiply `a · c = 2 · 3 = 6`
**Step 2:** Find two numbers that multiply to `6` and add to `7`: `1` and `6`
**Step 3:** Split the middle term: `2x² + x + 6x + 3`
**Step 4:** Group: `(2x² + x) + (6x + 3)`
**Step 5:** Factor each group: `x(2x + 1) + 3(2x + 1)`
**Step 6:** Factor out the shared binomial: `(2x + 1)(x + 3)`

**Check (FOIL):** `2x² + 6x + x + 3 = 2x² + 7x + 3` ✓

**Answer: (2x + 1)(x + 3)**
