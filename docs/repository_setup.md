# Repository setup and future updates

This package contains the initial English documentation and source-directory scaffold for **EngineLoop — FPGA-Based Engine HIL Testbench**. It contains no executable engine model, FPGA design, or ECU firmware yet.

## Initial upload

1. Extract the ZIP into a temporary folder.
2. Upload or copy the extracted **contents** into the root of your existing GitHub repository. `README.md`, `CONTRIBUTING.md`, `docs/`, `fpga/`, and the other module directories belong directly at the repository root.
3. Preserve all subdirectories and packaged configuration/template files. The archive includes repository configuration and GitHub templates, which some file browsers hide by default.
4. Review the changes before committing. If your repository already has a README or other files, reconcile them with this scaffold rather than removing unrelated content.
5. Use an initial commit message such as `docs: add EngineLoop architecture and implementation roadmap`.

Upload the extracted files, not the ZIP archive itself. The ZIP has no extra enclosing project directory and includes no `.git` directory, credentials, raw datasets, generated builds, or measured results.

## Optional local Git workflow

These are example publishing commands, not hardware build or test commands. Replace `YOUR_REPOSITORY_URL` with the URL of the repository you already created.

```bash
git clone YOUR_REPOSITORY_URL engineloop-hil
cd engineloop-hil
```

Copy the extracted package contents into that cloned directory, keeping its existing `.git` directory. Include the archive's configuration files and `.github` templates when copying. Then inspect and commit:

```bash
git status --short
git diff
git add .
git diff --cached --check
git diff --cached --stat
git diff --cached
git commit -m "docs: add EngineLoop architecture and implementation roadmap"
git push
```

Cloning the existing repository first preserves any initial README, license, or other commit history. Review all staged changes before the commit, especially if the repository contains files beyond this scaffold.

## After uploading

- Confirm that GitHub displays the project README at the repository root.
- Open the architecture, roadmap, and validation links from the README.
- Check that all planned modules and implementation checklists remain marked as unimplemented.
- Start with P0 interface conventions and the public-data baseline.

## Future updates

Use one focused branch or commit per task. Add the implementation to its module directory, document the checks actually run, update [progress.md](progress.md), and check off only completed items in [roadmap.md](roadmap.md). Update the interface specification whenever an agreed convention changes.

See [CONTRIBUTING.md](../CONTRIBUTING.md) for evidence and data-handling conventions.
