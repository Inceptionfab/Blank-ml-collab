# Contributing

## Branches
| Branch | Created from | Merges into | Merge method |
|---|---|---|---|
| feat/<short-name> | dev | dev | Squash and merge |
| data/<short-name> | dev | dev | Squash and merge |
| exp/<member>-<idea> | dev | never (re-apply the winner on a new feat/ branch) | — |
| fix/<short-name> | main | main, then main → dev | Create a merge commit |
| dev → staging → main (releases) | — | — | Create a merge commit |

Names are lowercase and hyphenated: `feat/dvc-pipeline`, `data/drop-zero-tenure`, `exp/ahsan-logreg`.
Nobody pushes to dev, staging or main: every change is a PR with 1 approval and green CI.

## Merge strategy (team decision)
- PRs from feat/ and data/ branches into dev are **squash-merged**: one clean Conventional Commit
  per PR on dev, while the PR page keeps the detailed commits.
- Release PRs (dev → staging → main), fix/ PRs into main and the main → dev back-merge use
  **Create a merge commit**. Squashing them would give the long-lived branches different
  histories and cause conflicts at every release.
- We never use "Rebase and merge".
- To update your own feature branch: `git fetch origin && git rebase origin/dev`, then
  `git push --force-with-lease`. Never force-push anything else.

## Commit messages: Conventional Commits
`<type>: <imperative summary>`, type ∈ feat, fix, data, exp, refactor, test, docs, ci, build, chore, style.
Examples: `feat: add scaling step`, `data: remove duplicate rows`, `exp: try max_depth=8`.

## Pull requests
- Base branch is **dev** (change it: GitHub defaults to main).
- Fill in the template. Metrics table: `git fetch origin && uv run dvc metrics diff origin/dev --md`.
- Assign one teammate as reviewer. Reviewers check out the branch whenever the PR touches data
  or the pipeline, and paste the ticked checklist into their review.
- The author merges after approval; the branch is deleted automatically.

## Data and models (DVC)
- Only `.dvc` pointers, `dvc.yaml`, `dvc.lock`, `params.yaml` and `metrics.json` go into Git.
- Always `uv run dvc push` **before** `git push`. After `git pull`, run `uv run dvc pull`.
- Credentials only via `dvc remote modify storage --local ...` (stored in `.dvc/config.local`).

## Experiments
- Commit first; never run experiments on uncommitted code.
- Run: `uv run dvc exp run --temp -n <member>-<idea> -S train.<param>=<value>`.
- Every hyperparameter, split ratio and the seed live in `params.yaml`.

## Reported metric
ROC-AUC on the fixed 20% stratified test split (seed 42); secondary metric and tie-break:
F1 of the churn class (Churn = Yes). All metrics are rounded to 4 decimals by `src/evaluate.py`.

## Environment
- Python 3.12 + uv. Run `uv sync` after every pull that changes `uv.lock`; add packages with `uv add`.
- Run `uv run pre-commit install` once in every clone.

## Notebooks
- Paired with jupytext (`.ipynb` + `.py` percent script); outputs stripped by nbstripout.
- Restart and run all cells before opening a PR.
- Reusable logic moves to `src/` with a unit test and is imported back into the notebook.

## Lessons learned (v1.0 retrospective)
1. **Check the PR base before you click "Create pull request".** Every PR targets `dev`, except release PRs,
   `fix/` PRs and the `main` → `dev` back-merge, which name their own base. GitHub defaults to `main`: #6 and #9
   targeted `main` by mistake, and #9 had to be reverted in #10.
2. **Use the right merge button, and never rewrite a reviewed branch.** Squash for `feat/` and `data/` into `dev`;
   "Create a merge commit" for everything into `staging` or `main` and for the back-merge (check the dropdown: #11
   went in unsquashed). Once review is requested, add commits instead of amending and force-pushing (#5).
3. **The winner rule is exact.** Highest ROC-AUC; runs within 0.001 ROC-AUC count as tied, and the higher F1 wins.
   "Tie-break" alone was read two ways during the experiment decision (#7).
4. **Runs must be reproducible from a fresh clone.** Commit before `dvc repro` or an experiment, and reviewers reject
   `code_uncommitted: true`; write generated text files with `newline="\n"` so hashes match on every OS; list every
   imported `src/` module as a dependency in `dvc.yaml`. All three were caught in the review of #5.
5. **Set up DVC remote access in every clone.** DagsHub needs an account even for a public repo, so run the three
   `uv run dvc remote modify storage --local ...` lines (see README) in each new clone, and `uv run dvc status -c`
   before `git push` to confirm the remote has your data. On Windows `dvc exp push` can't authenticate; push the
   experiment refs with `git push origin "refs/exps/*:refs/exps/*"` instead.
