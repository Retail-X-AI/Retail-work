# M01-02 — GitHub Project Control Structure

## 1. Project Control Structure

**Project:** RetailAI
**GitHub Organization:** Retail-X-AI
**Repository:** Retail-work
**GitHub Project:** Retail-X
**Project Number:** 2
**Project Visibility:** Private
**Project URL:** https://github.com/orgs/Retail-X-AI/projects/2

This document records the GitHub Project control structure used to manage the RetailAI project. The configuration was verified directly from GitHub Project #2 using GitHub CLI.

## 2. Purpose

The GitHub Project provides a central control area for tracking project issues, assignments, priorities, milestones, pull requests, reviews, dates, and progress.

The project supports the team's required workflow:

Issue → Branch → Work → Test → Commit → Push → Pull Request → Review → Merge → Close Issue

## 3. Verified Project Fields

The following fields are currently available in GitHub Project #2:

| Field                | Type            | Purpose                                        |
| -------------------- | --------------- | ---------------------------------------------- |
| Title                | Project field   | Identifies the project item                    |
| Assignees            | Project field   | Identifies the person responsible for the work |
| Status               | Single-select   | Tracks the current work status                 |
| Labels               | Project field   | Categorises project items                      |
| Linked pull requests | Project field   | Connects work items to pull requests           |
| Milestone            | Project field   | Connects issues to project milestones          |
| Repository           | Project field   | Identifies the repository containing the work  |
| Reviewers            | Project field   | Identifies reviewers                           |
| Parent issue         | Project field   | Connects related issues                        |
| Sub-issues progress  | Project field   | Tracks progress of sub-issues                  |
| Created              | Project field   | Records when the item was created              |
| Updated              | Project field   | Records the latest update                      |
| Closed               | Project field   | Records when the item was closed               |
| Priority             | Single-select   | Indicates the priority of the work             |
| Size                 | Single-select   | Indicates the estimated size of the work       |
| Estimate             | Project field   | Supports effort estimation                     |
| Iteration            | Iteration field | Supports iteration-based planning              |
| Start date           | Project field   | Records the planned start date                 |
| Target date          | Project field   | Records the planned target date                |

## 4. Project Control Areas

The verified configuration provides control over the following areas:

### Work Assignment

The **Assignees** field identifies the team member responsible for an issue.

The **Reviewers** field identifies the person responsible for reviewing completed work.

### Work Status

The **Status** field provides progress tracking for project items.

The project uses status tracking to distinguish work that has not started, work in progress, work under review, and completed work.

### Priority

The **Priority** field is used to identify the importance of project work and support work sequencing.

### Dates

The project contains both **Start date** and **Target date** fields.

These fields support scheduling and make planned work periods visible within the Project.

### Milestones

The **Milestone** field connects project issues to the relevant GitHub milestone.

This allows work to be grouped according to the project's milestone structure.

### Evidence and Review

Pull requests are connected through the **Linked pull requests** field.

The **Reviewers** field supports the required review process before work is merged.

### Issue Relationships

The **Parent issue** and **Sub-issues progress** fields support the organisation of related work and tracking of larger activities.

## 5. Project Workflow

Each project activity follows the team's controlled Git workflow:

1. GitHub Issue identifies the required work.
2. A dedicated branch is created for the issue.
3. The assigned team member completes the work.
4. The work is tested or verified where applicable.
5. Changes are committed using the issue ID.
6. The branch is pushed to GitHub.
7. A pull request is created and linked to the issue.
8. The assigned reviewer reviews the work.
9. Required changes are completed if requested.
10. Approved work is merged into the main branch.
11. Final verification is performed.
12. The GitHub issue is marked as Done/closed.

## 6. Evidence Verification

The project configuration was verified using GitHub CLI commands:

```text
gh project list --owner Retail-X-AI
gh project field-list 2 --owner Retail-X-AI
gh project view 2 --owner Retail-X-AI
```

The commands confirmed:

* GitHub Project #2 exists under the Retail-X-AI organisation.
* The project is named Retail-X.
* The project is open.
* The project is private.
* The project contains the verified control fields documented above.
* The project currently contains 99 items.

## 7. M01-02 Completion Evidence

**Issue:** M01-02 — Set up GitHub Project control structure
**Milestone:** M01 — Project Foundation & Control
**Repository:** Retail-work
**Repository location:** `planning/`
**Evidence file:** `planning/project-control-structure.md`

This file records the verified GitHub Project control structure used for managing the RetailAI project.

## 8. Control Structure Status

The GitHub Project control structure has been inspected and documented.

Further project management activities will continue through the GitHub Project, milestones, issues, branches, pull requests, reviews, and repository evidence.
