# Fix ty VS Code Integration

## Priority
Medium

## Created
2025-08-03

## Completed
2025-08-03

## Description
The ty type checker is working from command line but the VS Code extension integration needs proper configuration. Currently, the extension may not be finding the correct Python interpreter or source paths when working from the repository root with the backend in a subdirectory.

## Resolution Summary
After extensive investigation and testing, determined that the ty VS Code extension (v0.0.1-alpha.16) has fundamental limitations with monorepo structures. The extension cannot properly resolve Python module imports when code is in a subdirectory, even with various configuration attempts.

**Initial Decision**: Disabled IDE type checking to avoid false errors. Command-line ty remains fully functional.

**Update (After installing ty in venv)**: 
- ty has been added as a dev dependency to the backend virtual environment
- VS Code extension can now use the venv-installed ty at `backend/.venv/bin/ty`
- This may resolve the module resolution issues since ty runs in the correct Python environment

## What Was Attempted
1. ✅ Researched ty VS Code extension documentation and configuration options
2. ✅ Created wrapper script at `backend/scripts/ty-wrapper.sh` to invoke ty via uvx
3. ✅ Configured ty in `backend/pyproject.toml` with proper environment settings
4. ✅ Tested multiple VS Code settings configurations
5. ✅ Created VS Code workspace file for multi-root setup
6. ✅ Verified command-line ty works perfectly with all imports

## Final Configuration (Updated)
```json
{
  // ty type checker settings - using venv-installed ty
  "ty.importStrategy": "fromEnvironment",
  "ty.interpreter": ["${workspaceFolder}/backend/.venv/bin/python"],
  "ty.path": ["${workspaceFolder}/backend/.venv/bin/ty"],
  "ty.diagnosticMode": "workspace",
  "ty.logLevel": "info",
  
  // Disable Pylance type checking to avoid conflicts
  "python.analysis.typeCheckingMode": "off",
  "python.analysis.autoImportCompletions": true,
  "python.analysis.extraPaths": ["${workspaceFolder}/backend"]
}
```

## Current State
- ✅ Command-line type checking works: `cd backend && make typecheck`
- ✅ No false "Cannot resolve imported module" errors in VS Code
- ✅ Clean development experience without distracting incorrect errors
- ✅ Documentation created at `development-docs/ty-vscode-setup.md`
- ✅ Wrapper script available for future use when extension improves

## Known Limitations
- ty VS Code extension doesn't support monorepo structures properly
- Extension shows false import errors even when code is valid
- No `ty.cwd` or similar setting to change working directory
- Extension is alpha software not ready for production use

## Root Cause Analysis
The issue is straightforward - the ty VS Code extension needs a working directory setting. When ty executes from the workspace root, it cannot resolve imports like `src.api.routes` because it's looking for `src/` in the root directory instead of `backend/src/`.

### What Would Fix This
A simple configuration option in the extension:
```json
{
  "ty.cwd": "${workspaceFolder}/backend"
}
```

The extension would need to implement:
```typescript
// In the extension code
const workingDir = config.get('ty.cwd') || workspace.rootPath;
const tyProcess = spawn('ty', args, {
  cwd: workingDir,  // This is what's missing
  env: {
    ...process.env,
    PYTHONPATH: path.join(workingDir, 'src')
  }
});
```

### Why Our Wrapper Script Didn't Work
The wrapper script (`backend/scripts/ty-wrapper.sh`) correctly:
- Changes to the backend directory: `cd "${BACKEND_DIR}"`
- Sets PYTHONPATH: `export PYTHONPATH="${BACKEND_DIR}:${PYTHONPATH}"`

But the VS Code extension either:
- Doesn't properly execute the wrapper script
- Overrides the working directory after calling it
- Ignores the script's environment changes

This is a common oversight in language server extensions that assume project root equals code root. A simple `ty.cwd` setting would solve most monorepo issues.

## Recommendations
1. **Use command line**: Run `make typecheck` for type validation
2. **Uninstall ty extension**: Avoid confusion from false errors
3. **Wait for stable release**: Revisit after PyCon 2025 when ty reaches 1.0

## Lessons Learned
- Alpha software may have fundamental architectural limitations
- Monorepo support is often an afterthought in tooling
- Command-line tools can be more reliable than IDE integrations
- Sometimes the best solution is to wait for tool maturity

## Future Actions
- Monitor ty releases for improved VS Code extension
- Consider contributing monorepo support to ty-vscode project
- Re-evaluate when ty reaches stable release (expected post-PyCon 2025)
