# 02 — Linear Equations

A linear equation is any equation where the variable appears only to the first power — no `x²`, no `x` inside a square root, no `x` in a denominator. If you can draw its graph and get a straight line, it's linear. This module builds on the "isolate the variable" idea from `01-foundations` and extends it to messier, multi-step equations.

## 1. What makes an equation "linear"

These are linear:
```
x + 5 = 12
3x - 7 = 2x + 4
2(x - 3) = 10
```

These are **not** linear (you'll meet them later):
```
x² + 5 = 12        ← quadratic (Module 09)
1/x = 4            ← rational (Module 07)
√x = 3             ← radical (Module 08)
```

## 2. The core method: isolate x

Every linear equation is solved with the same four moves, used in whatever order gets `x` alone:

1. **Distribute** — clear any parentheses
2. **Combine like terms** — simplify each side first
3. **Move variable terms to one side, numbers to the other** — using the golden rule (do the same thing to both sides)
4. **Divide by the coefficient of x** — the last step, once `x` has a single number multiplying it

**Example:** `3(x - 2) = 2x + 5`

Step 1 — Distribute: `3x - 6 = 2x + 5`
Step 2 — Move variable terms to one side: subtract `2x` from both sides → `x - 6 = 5`
Step 3 — Move numbers to the other side: add `6` to both sides → `x = 11`

**Check by substituting back in:** `3(11 - 2) = 3(9) = 27`, and `2(11) + 5 = 22 + 5 = 27` ✓ — both sides match.

## 3. Variables on both sides

When `x` shows up on both sides of the equation, pick *one* side to collect it on — it doesn't matter which, the answer will be the same either way.

**Example:** `5x - 3 = 2x + 9`
- Subtract `2x` from both sides: `3x - 3 = 9`
- Add `3` to both sides: `3x = 12`
- Divide by `3`: `x = 4`

## 4. Equations with fractions

Multiply every term on both sides by the denominator to clear the fraction *before* doing anything else — this turns a fraction problem into a plain linear equation.

**Example:** `x/3 + 2 = 7`
- Multiply everything by 3: `x + 6 = 21`
- Subtract 6: `x = 15`

## 5. Special cases

Not every linear equation has exactly one solution:

- **No solution:** simplifying leads to something false, like `5 = 8`. Example: `2x + 3 = 2x + 7` → subtract `2x` from both sides → `3 = 7`, which is never true. No value of `x` works.
- **Infinite solutions:** simplifying leads to something always true, like `4 = 4`. Example: `2(x + 3) = 2x + 6` → distribute → `2x + 6 = 2x + 6`, true for *every* `x`.

These aren't mistakes — they're valid outcomes, and worth recognizing rather than assuming you did something wrong.

## What's next

Once multi-step equations (including both-sides and fraction cases) feel routine, move to `03-inequalities`, which uses the exact same isolating technique with one new rule: flipping the inequality sign when multiplying or dividing by a negative.

See `worked-examples.md` for more step-by-step problems, and `common-mistakes.md` before starting the practice set.

