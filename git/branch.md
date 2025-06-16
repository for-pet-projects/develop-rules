# Branching policy
## 1. Branch Roles and Overview

- **`main/<global_version>`**
    
    Production-ready branch matching with **dev/<global_version>**
    - If you do not use “global versions” (e.g. server vs desktop), simply use `main`
    - Otherwise, use `main/server`, `main/workstation`, `main/v2.X.X`, etc
- **`dev/<global_version>`**
    
    Main development branch (everything except hotfix merges here)
    - If you do not use global versions, simply `dev`
    - Otherwise, use `dev/server`, `dev/workstation`, `dev/v2.X.X`, etc
- **`epic/<short-description>-#<issue-number>`**
    
    Branch for a large-scale or multi-part feature (epic)
    - Acts as a “dev” for its child feature/bugfix/refactor/chore branches
- **`feature/<short-description>-#<issue-number>`**
    
    New functionality or enhancement (create from **dev** or **epic**)
- **`bugfix/<short-description>-#<issue-number>`**
    
    Non-release bug fix (create from **dev** or **epic**)
- **`hotfix/<short-description>-#<issue-number>`**
    
    Release bug fix requiring immediate attention (create from **main**)
- **`refactor/<short-description>-#<issue-number>`**
    
    Architectural or major code-structure change (create from **dev** or **epic**)
- **`chore/<short-description>-#<issue-number>`**
    
    Non-functional tweaks (code style, docs, small edits) (create from **dev** or **epic**)
- **`experimental/<short-description>-#<issue-number>`**
    
    Branch for quick test new tech or solutions. **Never merge** with anything else (create from **dev** or **epic**)
    - If the experiment is successful, create a new feature branch for updates

## 2. Naming Conventions
1. Use **kebab-case**
    - only lowercase English letters, digits, and `-` or `/`
    - The `#` symbol remains to clearly identify the issue number (e.g. `-#123`)
    - No spaces, no underscores, no uppercase letters
    - `global_version` and `version` can contain `.`
2. Maximum length for any branch name: **60 characters**
    - This limit includes prefix (`feature/`), suffix (`-#<digits>`), and any `<global_version>`
3. Format examples:
    - `main/v2.x.x`
    - `dev/legacy`
    - `epic/ios-support-#1232`
    - `feature/add-login-page-#193`
    - `bugfix/fix-null-pointer-exception-#174`
    - `hotfix/critical-db-leak-#125`
    - `refactor/extract-user-service-#126`
    - `chore/update-readme-#127`
    - `experimental/fft-integrate-#448`

## 3. Branch Lifecycle
1. **Create a branch**
    - All branches (except `dev` and `hotfix`) must be created from `dev` or `epic`
    - You **must** create a corresponding issue before creating any branch other than `dev` or `main`
    - One branch should address exactly one issue/task (one task = one branch)
    - If you are working on an epic’s sub-task, set “Ancestors: epic/<…>” in your issue (see above)
2. **Daily Workflow**
    - At the start of each workday **merge the parent branch into your branch**
3. **Push Commits**
    - Write meaningful commit messages; each commit should represent one logical change
    - Do not push directly to `dev` or `main`. Enable branch protection if possible
4. **Pull Request (PR)**
    - Always target `dev` or `epic` (unless it’s a hotfix branch, see below)
    - Follow the `git/Templates/PR_template.md`
    - Require at least **2 approvals** before merging (could be any team members, including administrators)
    - All status checks (linters, tests, build) must pass
    - Merge using **`--squash`** only. Do not use fast-forward or rebase-merge
5. **Release Branches**
    - Before merging into `main` branch, perform deep QA and testing in `dev`
    - When ready to release new version:
        1. In `dev` create empty commit "Release vX.Y.Z"
        2. Squash merge into `main` with -m "Release vX.Y.Z"
        3. Tag the release in `main` with an annotated tag "Release vX.Y.Z"
    - Ensure `dev` and `main` are protected, if possible:
        - No direct pushes allowed
        - Require at least 2 approved reviews
        - Require all status checks to pass
6. **Hotfix Branches**
    - Create `hotfix/<short-description>-#<issue-number>` from `main`
    - Apply the fix, then open an PR from your branch into `main`
    - Require same process, but instead of "Release vX.Y.Z" use "Hotfix vX.Y.Z <short description>"
    - After this, creating `bugfix` issue to fix this problem in `dev`
7. **Cleanup**
    - **Within 24 hours** after merge: locally delete branch
    - **Within 7 days** after merge: delete remote branch

## 4. Merge Rules
1. **Only `--squash` merges**
2. **Do not rebase** or fast-forward-merge after PR is opened (rebase is only used locally before opening or updating PR)
3. **Approvals:** Minimum **2** reviewers (including administrators if necessary)
4. **Status checks:** All must pass (CI pipeline, tests, linters, etc.)
5. **One PR = one logical change.**
6. **PR title format:** `[<branch-name>]`
7. **PR description:** Follow the PR template exactly

> **Reminder:** These rules apply to everyone (developers, administrators, integrators) without exception