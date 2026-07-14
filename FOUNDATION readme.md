# 01 — Foundations

Before you can do algebra, you need three things to feel automatic: **integers, order of operations, and variables.** This module builds all three.

## 1. Integers

Integers are whole numbers, positive, negative, or zero: `..., -3, -2, -1, 0, 1, 2, 3, ...`

The part that trips people up isn't recognizing integers — it's **arithmetic with negatives.**

**The number line trick:** think of every number as a position on a line. Adding moves right, subtracting moves left.

- `5 + (-3)` → start at 5, move left 3 → `2`
- `-4 - 2` → start at -4, move left 2 (subtracting always moves left) → `-6`
- `-4 - (-2)` → subtracting a negative flips direction → move *right* 2 → `-2`

**Multiplying/dividing negatives — the sign rule:**
- Same signs → positive result: `(-3) × (-4) = 12`
- Different signs → negative result: `(-3) × 4 = -12`

## 2. Order of Operations (PEMDAS)

When an expression has multiple operations, you don't just go left to right — you follow a fixed order:

**P**arentheses → **E**xponents → **M**ultiplication/**D**ivision (left to right) → **A**ddition/**S**ubtraction (left to right)

Note: Multiplication and division are the *same priority tier* — you do whichever comes first reading left to right. Same for addition and subtraction. This is the #1 source of PEMDAS mistakes (see `common-mistakes.md`).

**Example:** `3 + 4 × 2²`
1. Exponent first: `2² = 4` → `3 + 4 × 4`
2. Multiplication: `4 × 4 = 16` → `3 + 16`
3. Addition: `3 + 16 = 19`

## 3. Variables

A variable is just a placeholder for a number we don't know yet (or one that can change). Instead of saying "some number plus 5 equals 12," we write:

```
x + 5 = 12
```

Algebra is the practice of **isolating the variable** — getting it alone on one side of the equation — using operations that keep both sides equal.

**Golden rule of equations:** whatever you do to one side, you must do to the other.

```
x + 5 = 12
x + 5 - 5 = 12 - 5     ← subtract 5 from both sides
x = 7
```

That's it — that single idea (do the same thing to both sides to isolate the variable) is the engine behind almost everything in algebra that follows.

## What's next

Once integers, order of operations, and variables feel natural — not something you have to think hard about — move on to `02-linear-equations`, where you'll use these tools to solve real equations.

See `worked-examples.md` for more step-by-step problems, and `common-mistakes.md` before you start the practice set — it'll save you time.
