# 03 — Inequalities

An inequality compares two expressions using `<`, `>`, `≤`, or `≥` instead of `=`. Everything you learned in `02-linear-equations` about isolating `x` still applies here — there's exactly **one** new rule to learn, and it's the single most important thing in this whole module.

## 1. The one new rule: flip the sign when multiplying/dividing by a negative

Solving `2x < 10` works exactly like an equation: divide both sides by 2 → `x < 5`. No surprises.

But watch what happens with a negative:

```
-2x < 10
```

If we divide both sides by `-2` **without changing anything else**, we'd get `x < -5`. Let's sanity-check with a real number: try `x = 10`. Is `-2(10) < 10`? That's `-20 < 10` — true. But does `x = 10` satisfy `x < -5`? No. Something's broken.

The fix: **whenever you multiply or divide both sides of an inequality by a negative number, flip the inequality sign.**

```
-2x < 10
x > -5      ← sign flipped from < to >
```

Check again with `x = 10`: is `10 > -5`? Yes ✓. And does the original hold? `-2(10) = -20 < 10` ✓. Now it's consistent.

**Why this happens:** multiplying by a negative reverses order on the number line. If `3 < 5`, multiplying both sides by `-1` gives `-3` and `-5` — and `-3 > -5`, not `-3 < -5`. The relationship flips because the number line itself flips direction.

## 2. Everything else works like linear equations

- Distribute parentheses first
- Combine like terms
- Move variable terms to one side, numbers to the other
- Divide by the coefficient of `x` — **flipping the sign only if that coefficient is negative**

**Example:** `3x + 4 ≤ 19`
- Subtract 4: `3x ≤ 15`
- Divide by 3 (positive, no flip): `x ≤ 5`

**Example:** `-4x + 7 > -9`
- Subtract 7: `-4x > -16`
- Divide by -4 (negative — flip the sign): `x < 4`

## 3. Graphing the solution on a number line

Inequality answers are usually a whole *range* of numbers, not one value. Number lines show this with:
- **Open circle** (○) at the boundary for `<` or `>` — the boundary value itself is *not* included
- **Closed/filled circle** (●) at the boundary for `≤` or `≥` — the boundary value *is* included
- A ray extending in the direction of the solution

`x < 5` → open circle at 5, ray pointing left (toward smaller numbers)
`x ≥ -2` → closed circle at -2, ray pointing right (toward larger numbers)

## 4. Compound inequalities

Sometimes `x` is bounded on both sides, like `-3 < x ≤ 4`. This means "`x` is greater than -3 **and** less than or equal to 4" — solve it by applying the same operation to *all three* parts at once.

**Example:** Solve `-3 < 2x - 1 ≤ 9`
- Add 1 to all three parts: `-2 < 2x ≤ 10`
- Divide all three parts by 2: `-1 < x ≤ 5`

## What's next

Once flipping the sign on negative multiplication/division feels automatic, move on to `04-functions`, which introduces a new way of thinking about relationships between numbers — but still leans on everything you've built so far.

See `worked-examples.md` for more step-by-step problems, and `common-mistakes.md` before starting the practice set.
