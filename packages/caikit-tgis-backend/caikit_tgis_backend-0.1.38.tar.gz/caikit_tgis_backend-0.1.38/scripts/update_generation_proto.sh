#!/usr/bin/env bash

# Run from the base
cd $(dirname ${BASH_SOURCE[0]})/..

TGIS_BACKEND_DIR="caikit_tgis_backend"

# pull the latest generation.proto file from the vllm repo that needs to be followed
curl https://raw.githubusercontent.com/IBM/vllm/main/proto/generation.proto > $TGIS_BACKEND_DIR/generation.proto
# generate the p2b files based on the latest proto
./scripts/gen_tgis_protos.sh
