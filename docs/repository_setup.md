# Working with this repository

How to update the repository, keep its history clean, and store large artifacts.

## Uploading an updated package

The preferred path is Git on the command line, because the GitHub web uploader and some file browsers silently skip files whose names start with a dot (`.gitignore`, `.gitattributes`, `.github/`).

```bash
git clone https://github.com/AlexSun0401/engineloop-hil.git
cd engineloop-hil
# copy the extracted package contents over the clone, keeping .git
git status --short          # check that .gitignore, .gitattributes, .github/ appear
git add -A
git diff --cached --stat
git commit -m "docs: align repository with plan revision 2"
git push
```

If you must use the web uploader:

- **macOS Finder:** press `Cmd + Shift + .` to show hidden files before selecting them.
- **Windows Explorer:** View → Show → Hidden items.
- Or create each dot-file with **Add file → Create new file**, type the name (e.g. `.github/workflows/checks.yml`), and paste its contents.

After pushing, check that the **Actions** tab shows the `checks` workflow and that it passes.

## Day-to-day workflow

1. One focused branch per task, e.g. `p0/spark-table`, `p2/crank-gen`.
2. Put the implementation in its module directory; update any affected contract (`docs/interface_spec.md`, `docs/register_map.md`, `interfaces/engineloop.dbc`) in the same commit.
3. Run `python tools/check_md_links.py` (and `tools/check_dbc.py` if the DBC changed) plus the module's own checks.
4. Add a [progress.md](progress.md) entry; tick only the [roadmap](roadmap.md) items the change supports.
5. Open a pull request; the template lists the checks.

## Large and generated files

- Bitstreams (`.bit.bin`), overlays (`.dtbo`), firmware binaries, and large logic-analyzer captures are build outputs. Attach them to a **GitHub Release** for a tagged evidence set and record their SHA-256 in the run manifest; they are ignored by `.gitignore`.
- Raw EPA downloads stay out of the repository; `data/` scripts fetch them and verify checksums.
- A deliberately committed evidence capture uses `git add -f <file>` after review.

## Tags

Tag each evidence set, e.g. `evidence-p2-trigger-2026-12`, so a report's `repo_commit` can be found again.

## Keeping the project plan in sync

The agreed plan lives outside the repository. When a decision here changes the plan (scope, model inputs, tools, data rule), record it in [progress.md](progress.md) and update the plan document too.

See [CONTRIBUTING.md](../CONTRIBUTING.md) for evidence and data-handling rules.
