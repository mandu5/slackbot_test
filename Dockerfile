# Minimal Dockerfile for CI/CD testing
# This is a lightweight image for testing Docker builds in GitHub Actions
FROM alpine:latest

# Install basic utilities for testing
RUN apk add --no-cache bash curl

# Create a simple healthcheck
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD echo "OK" || exit 1

# Default command
CMD ["echo", "Docker image built successfully!"]


