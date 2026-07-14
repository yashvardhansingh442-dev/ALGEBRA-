# Module 01 — Foundation: Integers, Order of Operations, and Variables

Before you can do algebra, you must feel automatic with three core ideas:

1. **Integers** (whole numbers, including negatives)
2. **Order of operations** (the fixed rules for evaluating expressions)
3. **Variables** (placeholders for unknown or changing numbers)

This module explains each idea in detail, shows how to use them correctly, and gives you patterns you can rely on as you move into algebra.

---

## 1. Integers

### 1.1 What Integers Are

Integers are the set of whole numbers:

```
{ ... , −3, −2, −1, 0, 1, 2, 3, ... }
```

**Key properties:**
- They are whole: no fractions or decimals.
- They include:
  - Positive integers: 1, 2, 3, ...
  - Negative integers: −1, −2, −3, ...
  - Zero: 0 (neither positive nor negative)

You will use integers constantly in algebra, especially when solving equations and working with slopes, rates, and coordinates.

### 1.2 Adding and Subtracting Integers: The Number Line Trick

The hardest part of integer arithmetic is not recognizing integers; it's doing arithmetic with negatives correctly.

**The number line model**

Imagine a horizontal line:
- Numbers to the right are larger (more positive).
- Numbers to the left are smaller (more negative).
- 0 is the center.

**Rules:**
- Adding a number → move **right** by that amount.
- Subtracting a number → move **left** by that amount.

This works for both positive and negative numbers.

#### Example 1: Adding a negative

`5 + (−3)`

- Start at 5.
- Adding −3 means move left 3 steps.
- 5 → 4 → 3 → 2

**Result: 5 + (−3) = 2**

#### Example 2: Subtracting a positive

`−4 − 2`

- Start at −4.
- Subtracting 2 means move left 2 steps.
- −4 → −5 → −6

**Result: −4 − 2 = −6**

#### Example 3: Subtracting a negative

`−4 − (−2)`

- Subtracting a negative flips the direction.
- −(−2) is the same as +2.
- So this is the same as −4 + 2.
- Start at −4. Add 2 → move right 2 steps.
- −4 → −3 → −2

**Result: −4 − (−2) = −2**

#### Pattern summary

- `a + (−b) = a − b`
- `a − (−b) = a + b`

> Subtracting a negative always becomes adding the positive version.

### 1.3 Multiplying and Dividing Integers: The Sign Rule

When multiplying or dividing integers, the sign of the result depends on whether the signs are the same or different.

**Sign rule:**

- **Same signs → result is positive:**
  - (−3) × (−4) = 12
  - (−6) ÷ (−2) = 3

- **Different signs → result is negative:**
  - (−3) × 4 = −12
  - 6 ÷ (−2) = −3

You can think of this as:

| Operation | Result |
|---|---|
| Negative × Negative | Positive |
| Negative × Positive | Negative |
| Positive × Negative | Negative |

And the same pattern holds for division.

### 1.4 More Complex Integer Chains

Real problems often involve several operations in a row. Use the number line idea step by step.

**Example:** `−3 + 5 − 2 − (−4)`

Step-by-step:
1. `−3 + 5`: start at −3, move right 5 → 2
2. `2 − 2`: move left 2 → 0
3. `0 − (−4) = 0 + 4`: move right 4 → 4

**Result: −3 + 5 − 2 − (−4) = 4**

---

## 2. Order of Operations (PEMDAS)

When an expression has multiple operations, you cannot just go left to right. You must follow a fixed order.

### 2.1 The PEMDAS Rule

PEMDAS stands for:

- **P**arentheses (and other grouping symbols like brackets, fraction bars, etc.)
- **E**xponents (powers and roots)
- **M**ultiplication and **D**ivision (same priority, left to right)
- **A**ddition and **S**ubtraction (same priority, left to right)

**Important points:**
- Multiplication and division are equal priority. Do whichever comes first when reading left to right.
- Addition and subtraction are equal priority. Do whichever comes first when reading left to right.

> This "same tier" rule is the most common source of PEMDAS mistakes.

### 2.2 Step-by-Step PEMDAS Example

Evaluate: `3 + 4 × 2²`

**Step 1: Parentheses** — none. Skip.

**Step 2: Exponents**
- `2² = 4`
- Expression becomes: `3 + 4 × 4`

**Step 3: Multiplication and Division (left to right)**
- `4 × 4 = 16`
- Expression becomes: `3 + 16`

**Step 4: Addition and Subtraction (left to right)**
- `3 + 16 = 19`

**Final answer: 19**

### 2.3 Common PEMDAS Mistake: Same-Tier Operations

Many people wrongly think multiplication always comes before division, or addition before subtraction. **That is not correct.**

**Example:** `8 ÷ 4 × 2`

**Wrong reasoning:** Some people incorrectly believe "multiplication before division," and compute:
- `8 ÷ (4 × 2) = 8 ÷ 8 = 1` ❌

This is wrong because it ignores the left-to-right rule for same-tier operations.

**Correct reasoning:**
- Multiplication and division are the same priority; read left to right.
- First operation: `8 ÷ 4 = 2`
- Then: `2 × 2 = 4`

**Correct result: 8 ÷ 4 × 2 = 4**

### 2.4 Extra PEMDAS Examples

**Example 1:** `(6 + 3) × 2² − 4`

1. Parentheses: `6 + 3 = 9` → `9 × 2² − 4`
2. Exponents: `2² = 4` → `9 × 4 − 4`
3. Multiplication: `9 × 4 = 36` → `36 − 4`
4. Subtraction: `36 − 4 = 32`

**Result: 32**

**Example 2:** `10 − 3 + 2 × (4 − 1)`

1. Parentheses: `4 − 1 = 3` → `10 − 3 + 2 × 3`
2. Multiplication: `2 × 3 = 6` → `10 − 3 + 6`
3. Addition/Subtraction left to right:
   - `10 − 3 = 7`
   - `7 + 6 = 13`

**Result: 13**

---

## 3. Variables

### 3.1 What a Variable Is

A variable is a symbol (usually a letter like `x`, `y`, `t`) that represents:
- A number we don't know yet, or
- A number that can change.

Instead of saying:

> "Some number plus 5 equals 12."

We write:

`x + 5 = 12`

Here, `x` is the variable. The goal is usually to find what number `x` must be.

### 3.2 Equations and the Golden Rule

An equation is a statement that two expressions are equal, like:

`x + 5 = 12`

**Golden rule of equations:**

> Whatever you do to one side of the equation, you must do to the other side as well.

This keeps the equation balanced and ensures the solution stays correct.

### 3.3 Isolating the Variable

The main task in basic algebra is **isolating the variable**: getting it alone on one side of the equation, with everything else on the other side.

#### Example: Solving x + 5 = 12

We want `x` alone.

Current equation: `x + 5 = 12`

The `+5` is blocking `x`. To remove it, subtract 5 from both sides:

`x + 5 − 5 = 12 − 5`

Simplify:
- Left side: `x + 5 − 5 = x`
- Right side: `12 − 5 = 7`

**So: x = 7**

**Check:** plug x = 7 back into the original equation:
`7 + 5 = 12` ✓

### 3.4 Common Isolation Patterns

You will see many equations that fit simple patterns. Memorize these:

| Pattern | Action | Solution |
|---|---|---|
| `x + a = b` | Subtract `a` from both sides | `x = b − a` |
| `x − a = b` | Add `a` to both sides | `x = b + a` |
| `ax = b` (a ≠ 0) | Divide both sides by `a` | `x = b/a` |
| `x/a = b` (a ≠ 0) | Multiply both sides by `a` | `x = a × b` |

These patterns are the building blocks for solving more complex equations later.

### 3.5 A Slightly More Complex Example

Solve: `3x − 7 = 8`

Goal: isolate `x`.

**Step 1: Remove the −7**

Add 7 to both sides:
- `3x − 7 + 7 = 8 + 7`
- `3x = 15`

**Step 2: Remove the factor 3**

Divide both sides by 3:
- `3x/3 = 15/3`
- `x = 5`

**Check:** `3(5) − 7 = 15 − 7 = 8` ✓

---

## 4. How These Three Ideas Work Together

Algebra problems will usually combine:
- Integer arithmetic (especially with negatives),
- Order of operations (when simplifying expressions),
- Variable isolation (when solving equations).

### Example Combining All Three

Solve: `−2x + 3 = −7`

**Step 1: Isolate the term with x**

Subtract 3 from both sides:
- `−2x + 3 − 3 = −7 − 3`
- `−2x = −10`

*(Notice integer arithmetic with negatives: −7 − 3 = −10.)*

**Step 2: Isolate x**

Divide both sides by −2:
- `−2x / −2 = −10 / −2`
- `x = 5`

**Check:** `−2(5) + 3 = −10 + 3 = −7` ✓

*(Here we used integer addition: −10 + 3 = −7.)*

---

## 5. What's Next

Once these three ideas feel automatic:
- You can add/subtract/multiply/divide with negatives without hesitation.
- You can evaluate expressions using PEMDAS correctly, especially same-tier operations.
- You can isolate variables in simple equations using the golden rule.

Then you should move to **Module 02 — Linear Equations**, where you will:
- Solve more complex equations.
- Use these foundation skills to model real situations (rates, distances, costs, etc.).

**Before you start practice problems:**
- Review `worked-examples.md` for more step-by-step examples.
- Read `common-mistakes.md` to avoid typical errors in integer arithmetic, PEMDAS, and equation solving.

> Mastering this foundation is the key to making algebra feel manageable instead of confusing.
