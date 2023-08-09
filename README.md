# mpi3mr-dkms (45Drives patch)

DKMS package of the mpi3mr driver, patched to expose slot number for array devices.

## Development

- Upstream copy of driver is kept in the `upstream` branch. When a new driver is released, update the source code here.
- Patched version lives in `patched` branch. Merge any changes from `upstream` into `patched`.
- After modifying `patched` branch, checkout to `main` and run `./gen-patch.sh`. This creates the `patches/45drives.patch` file used by `dkms`.
- The `main` branch should only contain untouched upstream source code, the patch file created by `./gen-patch.sh`, and files necessary for packaing.
- To deploy new release, commit the new `patches/45drives.patch` to `main` and tag it.
