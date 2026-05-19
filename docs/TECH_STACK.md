# Minimum Tools and Software

## Required Now

- Java 21
- Maven Wrapper included in the repo
- GitHub repository
- GitHub Actions
- Python 3 for report summarization
- JUnit 5
- JaCoCo
- Dry-run AI agent script with no LLM API dependency

## Required Later

- OpenAI API key or AWS Bedrock model access
- GitHub token with pull request permissions
- S3 bucket for report files
- Aurora MySQL-compatible RDS for report metadata
- Spring Boot backend API for dashboard data
- Angular UI

## Recommended MVP Order

1. Make baseline coverage work locally.
2. Push sample microservice to GitHub.
3. Confirm GitHub Actions uploads the baseline report.
4. Add AI agent in dry-run/manual mode.
5. Add OpenAI or Bedrock provider.
6. Add automatic PR creation.
7. Add dashboard backend and Angular UI.
