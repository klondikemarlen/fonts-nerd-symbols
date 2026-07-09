# Feature Workflow

Use this for repo changes requested as feature work.

1. Create or confirm the GitHub issue before coding.
2. Create a feature branch named `<issue-number>-<short-slug>` from the target base branch.
3. Keep commits atomic: one logical change per commit, with imperative subjects.
4. Push the branch and open a draft pull request linked to the issue.
5. Run the smallest QA checks that cover the changed behavior and record exact results in the PR.
6. Review the diff before marking the PR ready. Fix blockers with additional atomic commits.
7. Merge the PR through GitHub after checks/review are satisfactory.
8. Return the issue, branch, commits, PR, QA evidence, and merge result.
