# Worked Examples — Functions

Cover the solution and try each one yourself first.

---

### Example 1: Basic evaluation
**Problem:** `f(x) = 2x + 3`. Find `f(4)`.

**Step 1:** Substitute `4` for `x`: `f(4) = 2(4) + 3`
**Step 2:** Simplify: `8 + 3 = 11`

**Answer: f(4) = 11**

---

### Example 2: Evaluating with a negative input and an exponent
**Problem:** `f(x) = x² - 5`. Find `f(-3)`.

**Step 1:** Substitute `-3` for `x`: `f(-3) = (-3)² - 5`
**Step 2:** Square first: `(-3)² = 9` → `9 - 5`
**Step 3:** Simplify: `4`

**Answer: f(-3) = 4**

*Watch the parentheses — `(-3)²` is 9, but `-3²` (without parentheses around the -3) would mean `-(3²) = -9`. Substituting negative inputs always keeps them in parentheses.*

---

### Example 3: Finding the domain
**Problem:** State the domain of `f(x) = 1/(x - 2)`.

**Step 1:** Identify what makes the denominator zero: `x - 2 = 0` → `x = 2`
**Step 2:** Exclude that value from the domain.

**Answer: Domain is all real numbers except x = 2 (written x ≠ 2)**

---

### Example 4: Solving for the input given the output
**Problem:** `f(x) = 3x - 1`. Find `x` such that `f(x) = 11`.

This flips the usual direction — instead of plugging in `x`, you're told the output and need to find the input. Set the function equal to the given output and solve like any linear equation.

**Step 1:** Set up the equation: `3x - 1 = 11`
**Step 2:** Add 1: `3x = 12`
**Step 3:** Divide by 3: `x = 4`

**Check:** `f(4) = 3(4) - 1 = 11` ✓

**Answer: x = 4**

---

### Example 5: Function composition
**Problem:** `f(x) = 2x + 1`, `g(x) = x - 4`. Find `f(g(3))`.

**Step 1:** Evaluate the inside function first: `g(3) = 3 - 4 = -1`
**Step 2:** Plug that result into f: `f(-1) = 2(-1) + 1 = -2 + 1 = -1`

**Answer: f(g(3)) = -1**
