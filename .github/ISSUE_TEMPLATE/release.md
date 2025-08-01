<!-- 
    Template for official release tracking (new /release branches)
    Required for each version before merging to main
-->

## Ancestors
<!-- Usually `dev/<global_version>` -->

## Description
Release of version `vX.Y.Z` from current development state.

## Checklist
- [ ] Create branch: `release/vX.Y.Z` from `dev`
- [ ] QA and manual testing
- [ ] Empty commit to mark the release:
    ```bash
    git commit --allow-empty -m "Release vX.Y.Z"
    ```
- [ ] Tag the release:
    ```bash
    git tag -a vX.Y.Z -m "Release vX.Y.Z"
    git push origin release/vX.Y.Z
    ```
- [ ] Generate and commit `CHANGELOG.md`
<!-- If not automated yet, you can manually generate with: -->
<!-- git log release/vA.B.C..release/vX.Y.Z --pretty=format:"- %s" -->
- [ ] Open PR: `release/vX.Y.Z → main`
- [ ] Merge PR using **squash**
