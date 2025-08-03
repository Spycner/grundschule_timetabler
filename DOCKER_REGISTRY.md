# Docker Registry & Image Usage

## GitHub Container Registry

The project automatically builds and publishes Docker images to GitHub Container Registry (ghcr.io) for easy deployment.

## Available Images

Images are published at: `ghcr.io/spycner/grundschule_timetabler`

### Tags

- `latest` - Latest stable build from main branch
- `main` - Latest build from main branch
- `develop` - Latest build from develop branch (if exists)
- `v1.0.0` - Specific version releases
- `main-sha-abc123` - Specific commit builds

## Using Published Images

### Pull the Image

```bash
# Pull latest version
docker pull ghcr.io/spycner/grundschule_timetabler:latest

# Pull specific version
docker pull ghcr.io/spycner/grundschule_timetabler:v1.0.0
```

### Run with Docker

```bash
# Run the container
docker run -d \
  --name grundschule-backend \
  -p 8000:8000 \
  -e DATABASE_URL=postgresql://user:pass@host/db \
  -e SECRET_KEY=your-secret-key \
  ghcr.io/spycner/grundschule_timetabler:latest
```

### Use in Docker Compose

Update your `docker-compose.yml`:

```yaml
services:
  backend:
    image: ghcr.io/spycner/grundschule_timetabler:latest
    # Remove build section when using pre-built image
    # build:
    #   context: ./backend
    #   dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://postgres:postgres@db:5432/grundschule_timetabler
    # ... rest of configuration
```

## Authentication for Private Repos

If the repository is private, you'll need to authenticate:

```bash
# Login to GitHub Container Registry
echo $GITHUB_TOKEN | docker login ghcr.io -u USERNAME --password-stdin

# Or use GitHub CLI
gh auth token | docker login ghcr.io -u USERNAME --password-stdin
```

## Multi-Platform Support

Images are built for both AMD64 and ARM64 architectures, so they work on:
- Intel/AMD machines (x86_64)
- Apple Silicon Macs (M1/M2/M3)
- ARM servers
- Raspberry Pi 4 (64-bit OS)

Docker automatically pulls the correct architecture.

## Image Security

### Signed Images

Production images are signed with cosign for verification:

```bash
# Install cosign
brew install cosign

# Verify image signature
cosign verify ghcr.io/spycner/grundschule_timetabler:latest \
  --certificate-identity-regexp "https://github.com/Spycner/grundschule_timetabler/*" \
  --certificate-oidc-issuer https://token.actions.githubusercontent.com
```

### SBOM (Software Bill of Materials)

Each image includes an SBOM for security scanning:

```bash
# Download SBOM
cosign download sbom ghcr.io/spycner/grundschule_timetabler:latest

# Scan for vulnerabilities
cosign download sbom ghcr.io/spycner/grundschule_timetabler:latest | \
  grype --add-cpes-if-none -
```

## CI/CD Pipeline

### Automatic Builds

Images are automatically built and pushed on:
- Push to `main` branch → `latest` and `main` tags
- Push to `develop` branch → `develop` tag
- Creating a release tag `v*` → Version tags (v1.0.0, v1.0, v1)
- Pull requests → Build only (no push)

### Build Status

Check the Actions tab in GitHub repository for build status.

## Local Development vs Production

### Development (local build)
```yaml
# docker-compose.yml
services:
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
```

### Production (pre-built image)
```yaml
# docker-compose.prod.yml
services:
  backend:
    image: ghcr.io/spycner/grundschule_timetabler:latest
```

## Troubleshooting

### Rate Limiting

GitHub has generous rate limits for ghcr.io:
- Authenticated: No practical limits
- Unauthenticated: Limited pulls per hour

### Image Not Found

1. Check if the repository is public/private
2. Verify you're authenticated if private
3. Check the correct image name and tag
4. Ensure the CI pipeline has completed successfully

### Wrong Architecture

Docker should automatically select the right architecture, but you can force it:

```bash
# Force AMD64
docker pull --platform linux/amd64 ghcr.io/spycner/grundschule_timetabler:latest

# Force ARM64
docker pull --platform linux/arm64 ghcr.io/spycner/grundschule_timetabler:latest
```

## Package Visibility

The packages appear in your GitHub repository under the "Packages" section on the right sidebar.

To make packages public (if repo is private):
1. Go to Package settings
2. Change visibility to Public
3. This allows unauthenticated pulls
