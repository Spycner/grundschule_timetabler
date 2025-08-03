# Fix ty VS Code Integration

## Priority
Medium

## Created
2025-08-03

## Description
The ty type checker is working from command line but the VS Code extension integration needs proper configuration. Currently, the extension may not be finding the correct Python interpreter or source paths when working from the repository root with the backend in a subdirectory.

## Acceptance Criteria
- [ ] VS Code ty extension properly configured
- [ ] Type checking works in VS Code editor
- [ ] Correct Python interpreter path set
- [ ] Source paths properly configured for backend/src
- [ ] Extension can find and use uvx with --native-tls flag
- [ ] Red squiggles appear for type errors in editor
- [ ] Hover shows type information
- [ ] Update documentation with VS Code setup

## Current Issues
- Extension may not be finding backend Python files
- Path configuration for monorepo structure unclear
- Need to specify uvx --native-tls for ty execution
- Python interpreter in backend/.venv not being used correctly

## Technical Details
### Settings to Configure
```json
{
  "ty.typeCheckingMode": "standard",
  "ty.path": ["uvx", "--native-tls", "ty"],
  "ty.interpreterPath": "${workspaceFolder}/backend/.venv/bin/python",
  "ty.extraPaths": ["${workspaceFolder}/backend/src"],
  "ty.workspaceRoot": "${workspaceFolder}/backend"
}
```

### Potential Solutions
1. Configure ty to run from backend directory
2. Set PYTHONPATH for ty extension
3. Create workspace file with multi-root setup
4. Use ty.extraPaths to add backend/src
5. Configure ty in backend/pyproject.toml properly

### Testing
- Open a Python file in backend/src
- Introduce a type error intentionally
- Verify red squiggle appears
- Check ty output panel in VS Code
- Ensure hover information works

## Notes
- ty is still in alpha, VS Code extension may have limitations
- May need to wait for updates from Astral
- Consider falling back to Pylance for now if ty extension not ready
- Document any workarounds needed

## Dependencies
- ty package installed and working from CLI
- VS Code ty extension installed
- Backend project structure established

## References
- [ty VS Code Extension](https://marketplace.visualstudio.com/items?itemName=astral.ty)
- [ty Documentation](https://docs.astral.sh/ty/)
- VS Code Python extension settings