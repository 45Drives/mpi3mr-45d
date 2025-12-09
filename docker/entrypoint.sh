#!/usr/bin/env bash

set -euo pipefail

kernels=()

# RHEL/Rocky layout
if compgen -G "/usr/src/kernels/*" > /dev/null; then
    kernels+=(/usr/src/kernels/*)
fi

# Debian/Ubuntu layout
if compgen -G "/lib/modules/*/build" > /dev/null; then
    kernels+=(/lib/modules/*/build)
fi

if [[ "${#kernels[@]}" == 0 ]]; then
    echo "no kernel build trees found! FAILED"
    exit 1
fi

cp -apf /src/* /build

RESULT=0

test_build() {
    for KERNEL in "${kernels[@]}"; do
        KERNEL="$(realpath "$KERNEL")"
        KERNEL_NAME="$(basename "$KERNEL")"
        printf '%s: ' "$KERNEL_NAME"
        if make -j"$(nproc)" CONFIG_DEBUG_INFO=1 -C "$KERNEL" M=/build > "/out/$KERNEL_NAME.log" 2>&1; then
            echo PASSED
        else
            RESULT=$?
            echo "FAILED (see '$KERNEL_NAME.log')"
        fi
    done
    return $RESULT
}

echo "unpatched {"
if test_build | sed 's/^/  /'; then
    echo "} PASSED"
else
    echo "} FAILED"
fi

patch -p1 -d /build < /src/patches/* >/dev/null 2>&1
echo "patched {"
if test_build | sed 's/^/  /'; then
    echo "} PASSED"
else
    RESULT=$?
    echo "} FAILED"
fi

exit $RESULT
