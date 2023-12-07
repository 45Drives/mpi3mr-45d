# mpi3mr-dkms (45Drives patch)

DKMS package of the mpi3mr driver, patched to expose slot number for array devices.

## Development

- Upstream copy of driver is kept in the `upstream` branch. When a new driver is released, update the source code here.
- Patched version lives in `patched` branch. Merge any changes from `upstream` into `patched`.
- After modifying `patched` branch, checkout to `main` and run `./gen-patch.sh`. This creates the `patches/45drives.patch` file used by `dkms`.
- The `main` branch should only contain untouched upstream source code, the patch file created by `./gen-patch.sh`, and files necessary for packaging.
- To deploy new release, commit the new `patches/45drives.patch` to `main` and tag it.

## Steps to update upstream
1. `git checkout upstream`
2. Download latest driver version from broadcom
3. Navigate through nested archives and open `mpi3mr-<driver version>-src.tar.gz`
4. Extract contents and copy files to repo in `upstream` branch
5. `git checkout patched`
6. `git merge upstream` and handle conflicts
7. `git checkout main`
8. `git merge upstream` (should *not* have any conflicts)
9. `./gen-patch.sh`
10. Update `PACKAGE_VERSION` in dkms.conf
