# Conventional Commits Reference

## Commit Types

| Type | Description |
|------|------------|
| `feat` | A new feature |
| `fix` | A bug fix |
| `docs` | Documentation only changes |
| `style` | Changes that do not affect the meaning of the code (white-space, formatting, etc.) |
| `refactor` | A code change that neither fixes a bug nor adds a feature |
| `perf` | A code change that improves performance |
| `test` | Adding missing tests or correcting existing tests |
| `chore` | Changes to the build process or auxiliary tools |
| `ci` | Changes to CI configuration files and scripts |
| `build` | Changes that affect the build system or external dependencies |

## Commit Message Format

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

## Examples

```
feat(auth): add OAuth2 login support
fix(api): handle null response from user service
docs(readme): update installation instructions
refactor(db): extract connection pool to shared module
```
