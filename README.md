# Llama Release Watcher

A specialized GitHub Actions pipeline that monitors the official [llama.cpp](https://github.com/ggerganov/llama.cpp) repository for new releases and automatically builds and publishes optimized CUDA Docker images to the GitHub Container Registry (GHCR).

## Overview

This project solves the need for automated, consistent Docker images of `llama.cpp` specifically tailored for CUDA environments without needing to maintain a full fork of the upstream repository.

### Key Features
- **Automated Polling:** Checks for new `llama.cpp` releases every hour.
- **Targeted Builds:** Focuses specifically on **CUDA 12** and **CUDA 13** for Linux `amd64`.
- **Multi-Variant Support:** Builds `full`, `light`, and `server` image targets.
- **Upstream Integrity:** Instead of mirroring code, the workflow clones the upstream repository at the specific release tag during the build process, ensuring 100% parity with official releases.
- **Smart Tagging:** Automatically creates multi-arch manifest tags and version-specific tags.

## Architecture

The workflow follows a 5-stage pipeline:

1. **Check:** A Python script queries the GitHub API. If the latest release tag differs from the one stored in `last_release_version.txt`, the pipeline proceeds.
2. **Prepare Matrices:** Generates a build matrix for the requested CUDA versions and image targets.
3. **Push to Registry:** 
   - Clones `llama.cpp` at the release tag.
   - Builds images using the official `.devops/cuda.Dockerfile`.
   - Pushes images by digest to GHCR.
4. **Merge Tags:** Uses `docker buildx imagetools` to create human-readable tags (e.g., `full-cuda12`) from the uploaded digests.
5. **Update State:** Commits the new release tag back to the repository to prevent redundant builds.

## Setup & Configuration

### Permissions
The workflow requires the following GitHub Action permissions:
- `contents: write` (to update the version file)
- `packages: write` (to push images to GHCR)

### Registry Configuration
By default, the project pushes to **GHCR**. No manual secrets are required if pushing to the same account/org as the repository, as it uses the built-in `GITHUB_TOKEN`.

**Optional Repository Variables:**
| Variable | Description | Default |
| :--- | :--- | :--- |
| `DOCKER_REGISTRY` | The container registry URL | `ghcr.io` |
| `DOCKER_IMAGE_REPO` | The destination image path | `ghcr.io/<owner>/llama-cpp` |

## Image Tagging Convention

Images are published with the following naming scheme:

| Image Type | CUDA Version | General Tag | Versioned Tag |
| :--- | :--- | :--- | :--- |
| **Server** | 12 | `server-cuda` / `server-cuda12` | `server-cuda12-<tag>` |
| **Server** | 13 | `server-cuda13` | `server-cuda13-<tag>` |
