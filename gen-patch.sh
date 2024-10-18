#!/usr/bin/env bash

set -Eeuo pipefail

mkdir -p patches

echo Generating patch...

git diff upstream patched -p | tee patches/45drives.patch

echo Updating dkms.conf...

DRIVER_VERSION=$(awk '/^#define MPI3MR_DRIVER_VERSION/{ print $3 }' <(git show patched:mpi3mr.h))
if [ -z "$DRIVER_VERSION" ]; then
  echo "Failed to extract driver version from mpi3mr.h" >&2
  exit 1
fi

sed -i 's/PACKAGE_VERSION=.*/PACKAGE_VERSION='"$DRIVER_VERSION"'/' dkms.conf

read -rp "Auto run manup now? [y/N] " yn
if [[ "$yn" == [Yy] ]]; then
  PKG_VERSION="$(echo "$DRIVER_VERSION" | tr -d '"' | cut -d '-' -f 1)"
  BUILD_NUMBER="$(echo "$DRIVER_VERSION" | tr -d '"' | cut -d '-' -f 2)"

  CHANGE_NOTES=("Update upstream driver to $PKG_VERSION")

  tmpfile=$(mktemp)
  cat <<EOF > "$tmpfile"
$(printf "%s\n" "${CHANGE_NOTES[@]}")
# Changelog text, one bullet point per line
EOF
  ${VISUAL:-${EDITOR:-nano}} "$tmpfile"
  mapfile -t CHANGE_NOTES < <(awk '/^[^#]/{print $0}' "$tmpfile")
  rm -f "$tmpfile" > /dev/null
  manup -u -v "$PKG_VERSION" -b "$BUILD_NUMBER" "${CHANGE_NOTES[@]}"
  manup -p
fi

echo Done :3
