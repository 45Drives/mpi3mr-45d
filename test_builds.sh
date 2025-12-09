#!/usr/bin/env bash

set -euo pipefail

exec > >(sed -e 's/\bPASSED\b/\x1b[1;32m&\x1b[0m/g' -e 's/\bFAILED\b/\x1b[1;31m&\x1b[0m/g')

SCRIPT_DIR="$(dirname -- "$(readlink -f -- "${BASH_SOURCE[0]}")")"
if [ -z "$SCRIPT_DIR" ]; then
    echo "Failed to get SCRIPT_DIR" >&2
    exit 1
fi
cd "$SCRIPT_DIR"

if command -v podman >/dev/null 2>&1; then
    CONTAINER_ENGINE=podman
elif command -v docker >/dev/null 2>&1; then
    CONTAINER_ENGINE=docker
else
    echo "podman or docker required!" >&2
    exit 1
fi
docker() {
    "$CONTAINER_ENGINE" "$@"
}

IMAGES=()

cat <<EOF
################################
# BUILDING IMAGES
################################
EOF

build_pids=()

for dockerfile in ./docker/*.dockerfile; do
    IMAGE="${dockerfile#./docker/}"
    IMAGE="${IMAGE%.dockerfile}"
    IMAGE="mpi3mr-builder-$IMAGE"
    (
    echo "building $IMAGE..."
    docker build --pull -t "$IMAGE" --file "$dockerfile" . >/dev/null 2>&1
    echo "$IMAGE done"
    ) &
    build_pids+=($!)

    IMAGES+=("$IMAGE")
done

for pid in "${build_pids[@]}"; do
    if ! wait "$pid"; then
        exit $?
    fi
done

cat <<EOF
################################
# TESTING BUILDS
################################
EOF

RESULT=0

for image in "${IMAGES[@]}"; do
    OS_NAME=${image#mpi3mr-builder-}
    mkdir -p "$SCRIPT_DIR/test_builds_out/$OS_NAME"
    echo "$OS_NAME: {"
    if docker run --rm --volume "$SCRIPT_DIR":/src:ro --volume "$SCRIPT_DIR/test_builds_out/$OS_NAME:/out" "$image" | sed 's/^/  /'; then
        echo "} PASSED"
    else
        RESULT=$?
        echo "} FAILED"
    fi
done

exit $RESULT
