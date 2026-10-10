# Before and after

A fictional session. Same request, same repo (a small shop called Pinecone Goods), two agents.

> **User:** The staging site is stale and the old coupon table is cluttering things up. Clean it up and get the latest version live.

## Without the matrix

```
Agent: Which branch should I use?
User: main.
Agent: Should I run the tests first?
User: yes, obviously
Agent: Tests pass. Do you want me to commit?
User: yes
Agent: Committed. Should I push?
User: yes!!
Agent: Pushed. Now, dropping the coupons table. Running DROP TABLE coupons on production...
Agent: Done. 1,284 rows deleted. Also force-pushed main to remove a messy commit.
```

Four needless questions about harmless steps, then two irreversible actions with no question at all. The coupons table had no backup, and a teammate's commit disappeared from main.

## With the matrix

```
Agent: Ran the tests (all green), committed "chore(shop): refresh staging config" and pushed to my branch.
Agent: Staging is redeployed and loads fine.

Agent: Before I touch the coupons table, I want to check:
  - What happens: the production table "coupons" (1,284 rows) is removed.
  - Can it be undone: only if I take a backup first. There is none right now.
  - Who is affected: checkout. Any customer with a saved coupon will see an error.
  I recommend a backup, then archiving the rows older than a year instead of dropping everything. Shall I?
User: yes, do that
Agent: Backup saved. Archived 311 old rows, 973 remain. Checkout tested, works.

Agent: One more thing. Main has a messy commit from Dana. I won't force-push to main. If you want it tidier, I can add a follow-up commit.
```

Green steps happened silently. The two risky steps got a short, plain explanation and a default. The forbidden step was refused with an alternative.
