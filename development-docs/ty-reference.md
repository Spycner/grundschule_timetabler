# ty Type Checker Reference

## Overview
ty is an extremely fast Python type checker written in Rust by Astral (same team behind Ruff and uv). It's currently in alpha/preview stage but already provides useful type checking capabilities.

## Installation & Usage

### Running ty
Since ty is in alpha, it's best run via uvx:

```bash
# Basic type checking
uvx --native-tls ty check

# Check specific directory
uvx --native-tls ty check src/

# Check specific file
uvx --native-tls ty check src/main.py

# Get version
uvx --native-tls ty --version
```

Note: The `--native-tls` flag is needed to handle certificate issues.

## Configuration

### pyproject.toml
ty reads configuration from `[tool.ty]` table in `pyproject.toml`:

```toml
[tool.ty]
# Basic configuration (limited in alpha)

[tool.ty.rules]
# Configure specific rules
# deprecated = "ignore"  # Example: ignore deprecation warnings
```

### Available Configuration
As of alpha version, configuration is minimal. The main options are:
- Rule severity levels: "error", "warning", "ignore"
- Python version settings (auto-detected from project)

## Common Warnings/Errors

### Deprecation Warnings
ty detects deprecated functions and suggests replacements:
```python
# Bad - ty will warn
datetime.utcnow()

# Good - timezone-aware
datetime.now(timezone.utc)
```

### Type Issues
ty performs standard type checking similar to mypy but faster:
- Missing type annotations
- Type mismatches
- Undefined variables
- Import errors

## Integration with Project

### Makefile Commands
```makefile
typecheck: ## Run type checker
	uvx --native-tls ty check

check: ## Run all checks
	uv run ruff check .
	uv run ruff format --check .
	uvx --native-tls ty check
```

### VS Code Integration
ty provides a language server, but VS Code integration is still in development. For now, run ty via terminal or Makefile commands.

### CI/CD Integration
```yaml
# GitHub Actions example
- name: Type check with ty
  run: uvx --native-tls ty check
```

## Comparison with mypy

### Advantages of ty
- **Speed**: 10-100x faster than mypy
- **Rust-based**: Better performance and memory usage
- **Integrated with Astral ecosystem**: Works seamlessly with ruff and uv
- **Modern**: Built from ground up with latest Python features in mind

### Current Limitations (Alpha)
- Limited configuration options
- Some advanced type features not yet supported
- Missing some mypy plugins compatibility
- Documentation still evolving

## Best Practices

1. **Run regularly**: Include in your check workflow
2. **Fix warnings**: Even in alpha, ty catches real issues
3. **Report bugs**: Help improve ty by reporting issues to Astral
4. **Stay updated**: ty is rapidly evolving, update frequently

## Troubleshooting

### Certificate Issues
If you see SSL/TLS errors:
```bash
uvx --native-tls ty check
```

### No Python Files Found
Ensure you're in the correct directory or specify path:
```bash
cd backend && uvx --native-tls ty check
```

### Configuration Not Working
- Check for typos in `[tool.ty]` section
- Verify you're using supported configuration options
- Remember ty is in alpha - not all features are available

## Future Features (Planned)
- Full mypy compatibility
- More configuration options
- Better IDE integration
- Plugin system
- Performance profiling
- Incremental checking

## Resources
- [GitHub Repository](https://github.com/astral-sh/ty)
- [Documentation](https://docs.astral.sh/ty/)
- [Astral Discord](https://discord.gg/astral)

## Notes
- ty is pre-release software - expect breaking changes
- Not recommended for production CI/CD yet
- Excellent for development and catching issues early
- Complements ruff for a complete Python toolchain
