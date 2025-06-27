# Issue Policy
## 1. General Rules

- **One task = one issue**
- **Title length:** maximum **40 characters**
- **Title format:** `<type>/<short-description>` in [kebab-case](https://en.wikipedia.org/wiki/Naming_convention_(programming)) — only lowercase English letters, digits, `-` and `/`
- **No renaming:** close & reopen to correct titles, rather than renaming
- **Prevent duplicates:** search existing issues carefully before creating a new one
- Follow the `.github/ISSUE_TEMPLATE/<template-type>.md`

## 2. Mandatory Labels

### Type (one per issue)

| Name              | Description                                           |
| -                 | -                                                     |
| **epic**          | Large-scale or multi-part feature                     |
| **feature**       | New functionality or enhancement                      |
| **bugfix**        | Non-release bug fix                                   |
| **hotfix**        | Release bug fix requiring immediate attention         |
| **refactor**      | Architectural or major code-structure change          |
| **chore**         | Non-functional tweaks (code style, docs, small edits) |
| **experimental**  | Quick test new tech or solutions                      |

### Priority (one per issue)

| Name      | Description                       |
| -         | -                                 |
| **P0**    | ASAP must-fix immediately         |
| **P1**    | High priority / next in roadmap   |
| **P2**    | Medium priority / desirable       |
| **P3**    | Backlog task                      |

Only Product Owner or Tech Lead may update `P0–P3` with a comment explaining the change

### Ancestors (one per issue)

Parent `dev/<global_version>` or `epic/<short-description>-#<issue-number>`

## 3. Milestones

- **Versions** (e.g. `v1.5`) are preferred
- Alternatively, use a “big-feature” milestone (e.g. `v1.4-new-ui`)
- **One milestone per issue** only