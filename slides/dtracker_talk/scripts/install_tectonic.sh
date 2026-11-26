#!/usr/bin/env bash
# Download a project-local Tectonic binary without touching system directories.
set -euo pipefail

VERSION="${TECTONIC_VERSION:-0.15.0}"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DEST="$ROOT/.tools/tectonic"

if [[ -x "$DEST" ]]; then
  "$DEST" --version
  exit 0
fi

case "$(uname -s)-$(uname -m)" in
  Linux-x86_64) TARGET="x86_64-unknown-linux-musl" ;;
  Linux-aarch64|Linux-arm64) TARGET="aarch64-unknown-linux-musl" ;;
  Darwin-x86_64) TARGET="x86_64-apple-darwin" ;;
  Darwin-arm64) TARGET="aarch64-apple-darwin" ;;
  *)
    echo "Unsupported platform: $(uname -s) $(uname -m). Install Tectonic and put it on PATH." >&2
    exit 1
    ;;
esac

ARCHIVE="tectonic-${VERSION}-${TARGET}.tar.gz"
URL="https://github.com/tectonic-typesetting/tectonic/releases/download/tectonic%40${VERSION}/${ARCHIVE}"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

echo "Downloading Tectonic ${VERSION} for ${TARGET}..."
curl -fL --retry 3 --output "$TMP/$ARCHIVE" "$URL"
tar -xzf "$TMP/$ARCHIVE" -C "$TMP"
mkdir -p "$ROOT/.tools"
install -m 0755 "$TMP/tectonic" "$DEST"
"$DEST" --version
