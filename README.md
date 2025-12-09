# mpi3mr-dkms (45Drives patch)
Build test status: ![Tests](https://github.com/45Drives/mpi3mr-45d/actions/workflows/tests.yml/badge.svg?branch=main)

DKMS package of the mpi3mr driver, patched to expose slot number for array devices.

## Development

- Upstream copy of driver is kept in the `upstream` branch. When a new driver is released, update the source code here.
- Patched version lives in `patched` branch. Merge any changes from `upstream` into `patched`.
  - make sure to update `MPI3MR_DRIVER_VERSION` in mpi3mr.h properly for build version.
- After modifying `patched` branch, checkout to `main` and run `./gen-patch.sh`. This creates the `patches/45drives.patch` file used by `dkms`.
- The `main` branch should only contain untouched upstream source code, the patch file created by `./gen-patch.sh`, and files necessary for packaging.
- To deploy new release, commit the new `patches/45drives.patch` to `main` and tag it.

## Steps to update upstream
1. `git checkout upstream`
2. Download latest driver version from broadcom
3. Navigate through nested archives and open `mpi3mr-<driver version>-src.tar.gz`
4. Extract contents and copy files to repo in `upstream` branch and commit them
5. `git checkout patched`
6. `git merge upstream` and handle conflicts
   1. make sure to update `MPI3MR_DRIVER_VERSION` in mpi3mr.h properly
7. `git checkout main`
8. `git merge upstream` (should *not* have any conflicts)
9.  `./gen-patch.sh`
10. ~~Update `PACKAGE_VERSION` in dkms.conf~~ done by `./gen-patch.sh`
11. ~~`manup` update the version/build~~ done by `./gen-patch.sh`
