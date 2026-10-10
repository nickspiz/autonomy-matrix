# Autonomy rules (team, production)

Several people share this repo and something real runs in production. Mistakes here are expensive, so judge every action by **reversibility x blast radius**. If rules conflict, the stricter one wins.

## Matrix
| Undoable | Radius | Behavior |
|---|---|---|
| Yes | Local | Do it silently |
| Yes | One project | Do it, report in one sentence |
| Yes | Several projects or shared infra | Do it, always report |
| No | Local | Ask once per session |
| No | Shared or production | Ask every time |
| No | Money, users, data | Ask, explain consequences, offer cancel |

## Just do it
- Read, search, diff, log, read-only status commands (CI runs, container status, logs).
- Read-only SQL (`SELECT`).
- Edit files in the project, run tests and local builds.
- `git fetch`, `git pull --rebase` at session start and on push rejection.
- Commit specific files after a finished task. Conventional commit messages, small commits.
- Push what you just committed to your own branch.
- Resolve trivial merge conflicts (different functions or sections). Combine both sides.

## Do it, then report in one sentence
- Edits to shared config, shared agent rules, or shared docs. Say that it affects everyone.
- Adding a new secret to the shared secrets file.
- Pulling a teammate's commits that touch files you are editing.

## Ask first, every time
- Money: live payments, paid APIs over about 20 calls, bulk image or video generation.
- Users: email, SMS, push, anything reaching more than 10 people, deleting more than 10 production rows.
- Production data: schema changes, access policy changes, `DROP`, `TRUNCATE`, `DELETE` without a precise `WHERE`. Take a backup and show the SQL first.
- Destructive git: `reset --hard`, `clean -fd`, `branch -D`, force-push, interactive rebase that drops commits.
- Access: creating or removing users, collaborators, keys, rotating production credentials. Anything using `sudo`.
- Deploy to production, unless the user said "deploy" and the work is committed.

## Never
- Force-push to the main branch.
- `--no-verify` or `--no-gpg-sign`.
- Commit a secret. Stop and tell the user.
- Run an update or delete with no `WHERE` on a production table.
- Push to a repository outside this organization.
- Take down production infrastructure without explicit owner approval.

## Git habits
- Before starting, check who else committed in the last 24 hours. If a teammate touched the same area, warn the user and pull first.
- Never `git add .` or `git add -A` when there are unexpected changes. Add named paths. Look at `git status` for `.env`, keys, and debug leftovers.
- Never amend a pushed commit. A failed hook means a new commit.
- Real merge conflicts: describe both versions in plain words, propose a default (usually the incoming one, since it passed review), and let the user confirm.

## How to ask
Non-developers use this repo. Don't show diff markers. Answer three questions, then recommend:
- What will happen?
- Can it be undone, and how?
- Who is affected?

## Project context
When the user names a project, load that project's CLAUDE.md or README and notes without being told. Keep that context until they clearly switch ("now about X"). Sub-topics such as deploy or docs stack on top. If two projects fit, ask one short question. Loading is a seconds-level step: read at most two or three small files, print a 3 to 7 line summary, wait for the task. No sub-agents, no network, no builds, no sleeping.
