# Team Roles and Git Workflow

## M01-03: Define Team Roles and Git Workflow

**Project:** RetailAI
**Milestone:** M01 Project Foundation & Control
**Issue ID:** M01-03
**Repository:** Retail-X-AI/Retail-work

## 1. Team Roles

The RetailAI project team will use defined roles to make responsibilities clear and ensure that each part of the project is properly managed.

### Project Manager

The Project Manager coordinates the overall project and monitors progress.

Responsibilities:

* Assign tasks to team members.
* Monitor milestones and deadlines.
* Manage GitHub Issues.
* Coordinate team communication.
* Monitor the completion of project documentation.
* Make sure project work follows the agreed Git workflow.

### Backend Developer

The Backend Developer is responsible for the server side of the RetailAI application.

Responsibilities:

* Develop the Python backend.
* Implement application logic.
* Connect the application to the database.
* Develop backend functionality required by the system.
* Fix backend errors and bugs.
* Test backend functionality.

### AI / Machine Learning Developer

The AI / Machine Learning Developer is responsible for the artificial intelligence functionality of RetailAI.

Responsibilities:

* Prepare and process the dataset.
* Develop the demand forecasting functionality.
* Develop stock related predictions.
* Implement AI functionality into the application.
* Test the AI models.
* Document the AI components.

### Frontend Developer

The Frontend Developer is responsible for the user interface.

Responsibilities:

* Develop the application interface.
* Create dashboards and forms.
* Implement HTML, CSS and JavaScript where required.
* Make the interface clear and easy to use.
* Test the user interface.

### Database Developer

The Database Developer manages the project's data storage.

Responsibilities:

* Design the database structure.
* Create and maintain database tables.
* Manage database connections.
* Ensure data is stored correctly.
* Test database operations.
* Support backend integration with the database.

### Testing and Documentation

The Testing and Documentation role is responsible for verifying the system and maintaining project documentation.

Responsibilities:

* Test completed features.
* Identify and report bugs.
* Verify that fixes work correctly.
* Maintain project documentation.
* Record evidence of completed work.
* Check that documentation is kept up to date.

## 2. Git Workflow

The team will use Git and GitHub to manage the project source code and documentation.

The agreed workflow is:

```text
Issue
→ Branch
→ Work
→ Test
→ Commit
→ Push
→ Pull Request
→ Review
→ Merge
→ Close Issue
```

### Step 1: Issue

Each task must have a GitHub Issue.

The issue identifies the work that needs to be completed, the responsible team member, priority, status and deadline.

### Step 2: Branch

The assigned team member creates a separate branch for the issue.

Branch names should clearly identify the work being completed.

Example:

```text
feature/M01-03-team-roles-git-workflow
```

### Step 3: Work

The team member completes the assigned work on the branch without directly modifying the `main` branch.

### Step 4: Test

The completed work must be checked before it is committed.

For documentation, this includes checking:

* File location
* Formatting
* Spelling
* Required information
* Markdown formatting
* Repository structure

### Step 5: Commit

The completed work is committed with a message containing the issue ID.

Example:

```text
M01-03 Define team roles and Git workflow
```

### Step 6: Push

The branch is pushed to the GitHub repository.

Example:

```bash
git push origin feature/M01-03-team-roles-git-workflow
```

### Step 7: Pull Request

A Pull Request is created from the working branch into `main`.

The Pull Request must reference the relevant GitHub Issue.

For M01-03, the Pull Request should reference:

```text
#3
```

### Step 8: Review

Another team member reviews the Pull Request.

The reviewer checks that:

* The required work has been completed.
* The document is stored in the correct location.
* The work follows the project requirements.
* No unnecessary changes have been introduced.
* The work is ready to be merged.

### Step 9: Merge

After the review is completed and the work is approved, the Pull Request can be merged into `main`.

### Step 10: Close Issue

After the Pull Request has been successfully merged, the M01-03 issue is marked as **Done** or closed.

## 3. Branching Rules

The `main` branch will contain the approved project version.

Team members should not use `main` for unfinished work.

Each task should normally use its own branch based on the relevant issue.

Example:

```text
main
│
├── feature/M01-01-project-setup
├── feature/M01-02-repository-setup
└── feature/M01-03-team-roles-git-workflow
```

This allows team members to work independently while keeping the main project version stable.

## 4. Commit Rules

Commit messages should clearly describe the completed change and include the issue ID.

Examples:

```text
M01-03 Define team roles and Git workflow
M01-04 Update project documentation
M02-01 Add product dataset
```

Small, related changes should be committed together rather than creating many unrelated commits.

## 5. Pull Request Rules

Each Pull Request should:

* Reference the relevant GitHub Issue.
* Explain what was completed.
* Be tested before submission.
* Be reviewed by another team member.
* Have any identified problems corrected before merging.

## 6. Evidence of Completion

For M01-03, the required evidence is the completed role and workflow document.

The document will be stored at:

```text
documentation/00-project/team-roles-and-git-workflow.md
```

The GitHub Issue will provide the record of the task, while the repository file provides the completed work.

## 7. M01-03 Completion Checklist

* [x] Define team roles.
* [x] Define Git workflow.
* [x] Save the document in `documentation/00-project/`.
* [ ] Test or verify the document.
* [ ] Commit using issue ID `M01-03`.
* [ ] Push the branch to GitHub.
* [ ] Create Pull Request linked to issue `#3`.
* [ ] Obtain review.
* [ ] Merge Pull Request.
* [ ] Mark issue `#3` as Done.
