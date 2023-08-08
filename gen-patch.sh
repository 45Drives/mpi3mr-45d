#!/usr/bin/env bash

mkdir -p patches
git diff upstream patched -p > patches/45drives.patch
