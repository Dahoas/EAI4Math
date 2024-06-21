# Lean setup from https://github.com/trishullab/copra/blob/main/src/scripts/setup.sh

# We only setup lean4
lean_version="4.8.0"
lean_repo="leanprover/lean4"

echo "Installing dependencies..."
echo "Installing Elan (Lean version manager) ..."
# # For Lean:
# # https://leanprover-community.github.io/install/debian_details.html
curl https://raw.githubusercontent.com/leanprover/elan/master/elan-init.sh -sSf | sh
echo "Installed Elan (Lean version manager) successfully!"
source $HOME/.elan/env

echo "Installing $lean_type ($lean_repo:$lean_version)..."
elan toolchain install $lean_repo:$lean_version
elan override set $lean_repo:$lean_version
echo "Installed $lean_type ($lean_repo:$lean_version) successfully!"
export PATH=$PATH:$HOME/.elan/bin

echo "Building Lean 4's projects ..."
(
    # Build Lean 4's projects
    echo "Building Lean 4's Simple Benchmark..."
    pushd ./data/test/lean4_proj
    lake build lean4_proj
    popd
    echo "Building Lean 4's Simple Benchmark done!"
) || exit 1
echo "Building Lean 4's interface REPL..."
(
    # Build Lean 4's interface REPL
    pushd ./src/tools/repl
    lake build repl
    popd
    echo "Lean 4's interface REPL built successfully!"
) || exit 1
echo "Building Lean 4 MiniF2F"
(
    # Build Lean 4's interface REPL
    pushd ./data/miniF2F-lean4/
    lake exe cache get
    lake build
    popd
    echo "MiniF2F built successfully!"
) || exit 1

