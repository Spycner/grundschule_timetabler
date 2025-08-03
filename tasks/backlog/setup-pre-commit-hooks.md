# Setup Pre-commit Hooks

## Priority
High

## Created
2025-08-03

## Description
Configure pre-commit hooks to ensure code quality and consistency before commits. This will automate code formatting, linting, and basic checks to maintain code standards across the project.

## Acceptance Criteria
- [ ] Install and configure pre-commit framework
- [ ] Setup Python hooks (ruff format, ruff check, ty type check)
- [ ] Setup general hooks (trailing whitespace, end of file, file size)
- [ ] Setup commit message validation
- [ ] Configure for both backend and future frontend
- [ ] Add pre-commit to developer documentation
- [ ] Test hooks with intentional violations
- [ ] Update Makefile with pre-commit commands
- [ ] Add .pre-commit-config.yaml to repository

## Technical Details
### Hooks to Include

#### Python (Backend)
- ruff format - Auto-format Python code
- ruff check - Lint Python code
- ty check - Type check (if possible via pre-commit)
- pytest (optional - for critical tests)

#### General
- trailing-whitespace - Remove trailing whitespace
- end-of-file-fixer - Ensure files end with newline
- check-yaml - Validate YAML files
- check-toml - Validate TOML files
- check-json - Validate JSON files
- check-merge-conflict - Check for merge conflict markers
- check-added-large-files - Prevent large files (>500KB)
- mixed-line-ending - Normalize line endings

#### Git/Commit
- commitizen or conventional-commits - Validate commit message format
- no-commit-to-branch - Prevent direct commits to main

#### Future Frontend Hooks (prepare configuration)
- eslint - JavaScript/TypeScript linting
- prettier - Code formatting
- typescript - Type checking

### Configuration Structure
```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    hooks:
      - id: ruff
      - id: ruff-format
  
  - repo: https://github.com/pre-commit/pre-commit-hooks
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      # ... etc
```

## Implementation Steps
1. Install pre-commit package
2. Create .pre-commit-config.yaml
3. Install git hooks
4. Test each hook type
5. Document usage in README
6. Add to developer onboarding

## Notes
- Pre-commit should be fast enough to not hinder development
- Consider stage-specific hooks (some only on push)
- Make sure VS Code save actions don't conflict
- Provide bypass instructions for emergencies (--no-verify)
- Consider adding to CI/CD pipeline as well

## Success Metrics
- Zero formatting issues reach repository
- Consistent code style across all commits
- Reduced PR review time for style issues
- All developers using hooks consistently

## Dependencies
- Backend setup complete
- Development environment established
- Team agreement on code standards

## References
- [pre-commit.com](https://pre-commit.com/)
- [Ruff pre-commit](https://github.com/astral-sh/ruff-pre-commit)
- [Conventional Commits](https://www.conventionalcommits.org/)