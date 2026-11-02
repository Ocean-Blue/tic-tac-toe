# Tic-Tac-Toe – Python & DevSecOps Learning Project

A small Python-based Tic-Tac-Toe game developed as a hands-on learning project to explore Python development, GitHub, and DevSecOps practices.

## Project Goals

The main purpose of this project is to gain practical experience with:

- **Python:** Application development and automated testing with pytest.
- **Git & GitHub:** Source control and repository management.
- **GitHub Actions:** Building an automated CI workflow.
- **Code Quality:** Using Ruff for linting and code formatting.
- **Security Scanning:** Integrating Bandit to identify potential security issues in Python code.
- **CI/CD:** Automating code quality checks, security scanning, and tests whenever code is pushed to GitHub.

## CI Pipeline

The GitHub Actions workflow currently performs the following steps:

1. Check out the repository.
2. Set up the Python environment.
3. Install project dependencies.
4. Run Ruff linting and formatting checks.
5. Run Bandit security scanning.
6. Execute automated tests with pytest.

## Purpose

This project serves as a practical exercise in understanding how code quality, automated testing, and security checks can be integrated into a development workflow.

It is a learning project, with additional DevSecOps practices to be explored and incorporated over time.