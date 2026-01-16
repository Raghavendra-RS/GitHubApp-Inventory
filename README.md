# GitHubApp Inventory

GitHubApp Inventory automatically audits GitHub App installations across your GitHub organization and generates a downloadable CSV report. It provides visibility into installed integrations for operational governance, security review, and compliance reporting.

This project is available as:

- ✅ A GitHub Action (Marketplace)
- 🐍 A standalone Python script (optional offline usage)

---

## 🚀 GitHub Action (Marketplace)

Run installation audits directly from GitHub Actions—no local setup required.


## How It Works

- Retrieves all installed GitHub Apps for the specified organization
- Collects installation metadata including:
    * App name & slug
    * Installation type (organization or user)
    * Target identifiers
    * Creation & update timestamps
    * Installation URLs
- Generates a structured CSV report
- Uploads it as a workflow artifact for download

##  Usage

```yml
- name: GitHubApp Inventory
  uses: org-name/githubapp-inventory@v1.0.0
  with:
    github_token: ${{ secrets.ORG_AUDIT_TOKEN }}
    org_name: acme


##  Upload Inventory Report
- uses: actions/upload-artifact@v4
  with:
    name: githubapp-inventory-report
    path: "*.csv"

```

> ⚠️ **Security Requirement:**
> 
> This action requires an authentication token with appropriate permissions.
> 
> You must define the token as a repository secret (for example, ORG_AUDIT_TOKEN) and explicitly provide it to the action as shown below:
>
> ```yml
> github_token: ${{ secrets.ORG_AUDIT_TOKEN }}
> ```


### Example workflow

```yml
name: GitHub-App Inventory Audit

on:
  schedule:
    - cron: "0 0 1 * *"
  workflow_dispatch:

jobs:
  audit:
    runs-on: ubuntu-latest
    steps:
      - name: GitHubApp Inventory
        uses: org-name/githubapp-inventory@v1.0.0
        with:
          github_token: ${{ secrets.ORG_AUDIT_TOKEN }}
          org_name: acme

      - name: Upload Report
        uses: actions/upload-artifact@v4
        with:
          name: githubapp-inventory-report
          path: "*.csv"

```


## 🔐 Required Token Permissions

The token used with this action must have the following scopes:

- `read:org – to list organization members`
- `repo - to analyze repository activity`
  


## 🔧 GitHub Action Inputs

| Name              | Required | Default           | Description                |
| ----------------- | -------- | ----------------- | -------------------------- |
| `github_token`    | Yes      | –                 | Token with read:org access |
| `org_name`        | Yes      | –                 | GitHub organization name   |
| `output_filename` | No       | `github_apps.csv` | Output CSV file name       |


## Sample Output

| App Name   | App ID | Target Type  |
| ---------- | ------ | ------------ |
| dependabot | 32542  | organization |
| sentry     | 11221  | organization |
| codecov    | 22198  | user         |


## 🐍 Standalone Python Script (Optional Local Usage)

## Overview

The standalone script allows local auditing without GitHub Actions. It retrieves:

- Installed GitHub Apps
- Installation targets & IDs
- Installation timestamps
- Installation URLs

## Prerequisites

Python 3.8+
- GitHub Personal Access Token with permissions:
  - `read:org` (read organization data)
  - `repo` (read repository data)


## Installation

Install required packages:

```bash
pip install requests python-dotenv
```

## Configuration

Create a `.env` file with your settings:

```env
GITHUB_TOKEN=ghp_xxxxx
ORG_NAME=acme

```


### Environment Variables

| Variable       | Description                                        | Default  | Example     |
| -------------- | -------------------------------------------------- | -------- | ----------- |
| `GITHUB_TOKEN` | GitHub Personal Access Token with `read:org` scope | Required | `ghp_xxxxx` |
| `ORG_NAME`     | GitHub organization to audit                       | Required | `acme-inc`  |


## Usage

Run the script:

```bash
python github_apps.py
```

## Output

### Console Progress

The script displays real-time progress:

```
🔍 Fetching installed GitHub Apps for organization: acme-inc
📦 Retrieved 12 installations
📄 Writing CSV -> github_apps_acme-inc_20250214_103455.csv
✅ Inventory complete

```

### CSV Report: ` github_apps_[ORG]_[TIMESTAMP].csv`


File generated:

```csv
App Name,App ID,Target Type
dependabot,32542,organization
sentry,11221,organization
codecov,22198,user
```

#### CSV Columns

| Column        | Description              | Values                 |
| ------------- | ------------------------ | ---------------------- |
| `App Name`    | GitHub App slug/name     | `dependabot`           |
| `App ID`      | Numeric App identifier   | `32542`                |
| `Target Type` | Installation target type | `organization`, `user` |


## Features

- ✅ Full organization-level GitHub App discovery
- 🔍 Identifies both organization-wide and user-installed Apps
- 📊 Exports structured CSV reports for audit & compliance
- 🔄 Built-in pagination handling
- 🛑 Automatic rate-limit detection + wait behavior
- 📈 Real-time console status output


## How It Works

1. **Load configuration**: Reads token & org from environment variables
2. **Fetch installations**: Uses GitHub REST API:
      - GET /orgs/{org}/installations
3. **Paginate through results**
4. **Extract installation metadata**
5. **Write CSV report**
6. **Print completion status**


## API Details

### Uses GitHub REST API (v3)
 Primary endpoint:
```
/orgs/{org}/installations
```

### Performance Considerations

Organizations with numerous installations may:

- Require multiple API pages
- Experience short rate-limit waits
- Produce larger CSVs


## Use Cases

- 📊 **Governance**: Visibility into external GitHub integrations
- 🔐 **Security Review**: Validate approved vs. unauthorized Apps
- 🧾 **Compliance**: Support SOC2 / ISO / SOX audits
- 🧱 **IT Operations**: Manage integration footprint & lifecycle
- 💼 **Enterprise Architecture**: Map external dependency patterns



 ## Troubleshooting

 ### 401 Unauthorized
     - Token missing or expired  
 ### 403 Forbidden
    - Token lacks read:org scope
 ### Rate limit exceeded
    - Script waits automatically — re-run if persistent   
 ### Empty Results
    - Organization may have no installed Apps or no visibility


## Interpreting Results

### A large number of installed Apps may indicate

- **High integration usage**: teams rely on many external tools to automate workflows or extend GitHub functionality
- **Decentralized procurement**: individual teams or developers can install Apps without centralized oversight
- **External system dependencies**: critical processes may depend on third-party services (CI/CD, security scans, analytics, etc.)

### A small number of installed Apps may indicate

- **Centralized security policies**: App install approvals are managed by a security or platform team
- **Restricted integration control**: only vetted or approved tools are allowed to integrate with the organization


## Best Practices

- 🗓  **Schedule Regular Audit**: run monthly or quarterly to maintain visibility into integrations
- 🔐 **Secure Report Storage**: treat exported data as sensitive organizational metadata
- 🕵️ **Review App Usage & Permissions**: ensure installed Apps still serve valid and authorized purposes
- 🗑  **Remove Stale Installations**: deauthorize Apps that are unused or no longer required


## Limitations

- **No Permission Scope Data**: App permission scopes are not currently retrieved or analyzed
- **No Repository Access Details**: Does not identify whether Apps target all repositories or selected ones
- **Single-Org Execution**: Only one organization can be audited per script execution
- **Token Visibility Boundaries**: Results are limited by what the provided token is authorized to view
- **No Enterprise Fleet Coverage**: Does not audit multiple organizations across an Enterprise account


## Additional Resources

- [GitHub REST API Documentation — GitHub Apps](https://docs.github.com/en/rest/apps/apps)
- [GitHub Organization Security Best Practices](https://docs.github.com/en/organizations/managing-security-for-organizations/security-best-practices-for-organizations)
- [GitHub Integration Governance Guidance](https://docs.github.com/en/enterprise-cloud@latest/admin/identity-and-access-management/third-party-application-restrictions/about-third-party-application-restrictions)
- [GitHub Enterprise Admin Documentation](https://docs.github.com/en/enterprise-cloud@latest/admin)




  
