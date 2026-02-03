# Contributing

Thank you for contributing to **csvplus**!  
This project is developed collaboratively by **Group37** as part of a DSCI 524 course on package development project.

This document outlines how our team works together, including our workflow, contribution process, and coding standards.

---

## How We Work

We follow a **GitHub Flow–based workflow**:

- The `main` branch is always kept in a working state
- No direct commits are made to `main`
- All changes are made through feature branches and Pull Requests (PRs)
- Tasks are tracked using GitHub Issues and the Project Board
- Work is organized into milestones

---

## Types of Contributions

Team members may contribute by:

- Reporting or fixing bugs
- Implementing new features
- Improving documentation (README, docstrings, examples)
- Writing or updating tests
- Providing feedback through GitHub Issues

---

## Issues and Task Management

- Each task should be created as a **GitHub Issue**
- Issues should be assigned to one team member
- Issues should be linked to the appropriate **milestone**
- Progress is tracked on the GitHub Project Board

Before starting work on an issue, assign yourself to it and leave a short comment indicating you are working on it.

---

## Get Started!

Ready to contribute? Here's how to set up csvplus for
local development.

1. Clone the repository:

    ```shell
    git clone git@github.com:UBC-MDS/DSCI_524_group37_csvplus.git
    ```

2. Install dependencies using Hatch:

   ```shell
   pip install hatch
   ```

3. Create a new branch from main.
Use clear prefixes such as feat/, fix/, or docs/.

    ```shell
    git checkout main
    git pull
    git checkout -b feat-short-description

    ```

4. Make your changes locally.

## Coding and Documentation Standards

- Follow Python best practices (PEP8 where applicable)
- Use clear, descriptive variable and function names
- All public functions must include docstrings
- New functionality should include tests when appropriate
- Keep commits small and focused

## Running Tests

Before submitting a Pull Request, ensure all tests pass:

   ```shell
    hatch run test:run
   ```

## Commit Messages

We use semantic / conventional commit messages, for example:

- `feat: add csv column validation helper`
- `fix: handle empty csv files`
- `docs: update README with usage example`

## Pull Request Guidelines

When opening a Pull Request:

- Link the PR to the related GitHub Issue
- Clearly describe what was changed and why
- Ensure tests pass
- Ensure documentation is updated if functionality changes
- Request at least one team member review before merging
- Only merge after the PR has been reviewed and approved.

## Communication

- Major decisions are discussed during scheduled team meetings
- GitHub Issues are used for technical discussion, questions, and blockers
- The Project Board is the source of truth for task status

## Decision Making and Conflict Resolution

- Technical decisions are discussed during team meetings or in GitHub Issues
- If consensus cannot be reached, the team will vote
- Blocking issues should be raised as early as possible to avoid deadline risk

## Retrospective and Next Steps

Our group used the development tools introduced in DSCI 524, including Python Packages, PyTest, Continuous Integration
and Deployment, and publishing on PyPI. Flake8 linter was used to maintain code quality.

We followed a GitHub flow workflow, where we listed Issues and created a branch for each issue.
Each pull request addresses a specific issue and requires a review from at least one other group member before merging.

GitHub was our main form of organization, with Issues used to communicate, report bugs, and keep track of progress.
For timely responses, we also used Slack as a secondary means of communication.

If we were to scale up our project, we would still used Git version control and CI/CD with trunk-based development.
External software such as Jira can be used for task management and bug reporting.
In general, the tools used in this course are well-suited for adaptation at a larger scale.
