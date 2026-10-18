# Contributing to Algebra Mastery

Thanks for wanting to help build this. Here's how to do it well.

## Ground rules

1. **Accuracy over speed.** A wrong solution merged in silently hurts every learner who trusts this repo. Double-check your math before opening a PR.
2. **Plain language first.** Explain the *why* before the formal notation. Assume the reader has never seen this concept.
3. **Follow the existing template.** Every topic folder has the same five files (`README.md`, `worked-examples.md`, `practice-problems.md`, `solutions.md`, `common-mistakes.md`). Match the style of what's already there.
4. **One concept per PR.** Easier to review, easier to merge.

## Ways to contribute (pick your comfort level)

| Contribution type | Difficulty | Good for |
|---|---|---|
| Fix a typo or unclear sentence | 🟢 Easy | First-time contributors |
| Add practice problems to an existing topic | 🟢 Easy–Medium | Anyone who knows the topic |
| Write a "common mistakes" entry | 🟡 Medium | People who've tutored or been confused themselves |
| Write a full topic module from the template | 🔴 Involved | Confident with the topic, has time |
| Build tooling (CI, quiz generator, etc.) | 🔴 Involved | Developers |

Check the [Issues tab](../../issues) for tasks labeled `good-first-issue`.

## Adding a practice problem

1. Open `curriculum/0X-topic/practice-problems.md`
2. Add your problem under the correct difficulty tier (Easy / Medium / Hard)
3. Add the matching, fully-worked solution to `solutions.md` — use the same problem number in both files
4. Keep problems original — don't copy verbatim from textbooks or paid courses

Example format:

```markdown
### Easy
**P1.** Solve for x: 2x + 3 = 11
```

```markdown
### Solution to P1
2x + 3 = 11
2x = 8
x = 4
```

## Writing an explanation (README.md for a topic)

- Start with a real-world or intuitive framing before introducing notation
- Include at least one fully worked example inline
- Keep paragraphs short — this is a reference people scan, not a novel

## Submitting a pull request

1. Fork the repo, create a branch (`add-linear-equations-practice-problems`)
2. Make your changes following the template
3. Open a PR with a short description of what you added/changed
4. A maintainer or experienced contributor will review for accuracy and clarity before merging

## Reporting an error

Found a wrong answer or confusing explanation? Open an issue using the "Fix error in solution" or "Improve explanation clarity" template — even if you don't want to fix it yourself, flagging it helps a lot.

## Code of Conduct

Be kind, be patient, assume good faith. This project exists to help people learn — that includes contributors who are still learning too.
