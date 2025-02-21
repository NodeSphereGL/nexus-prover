#!/bin/bash
set -e  # Exit immediately if any command fails
set -u  # Treat unset variables as errors
set -o pipefail  # Ensure errors in piped commands cause script failure

# Log function for better debugging
log() {
    echo "[INFO] $1"
}

error_exit() {
    echo "[ERROR] $1" >&2
    exit 1
}

NODE_ID_PATH="/root/.nexus/node-id"
WALLET_NODE_ID="/wallet/node-id"

# Ensure /root/.nexus exists
if [ ! -d "/root/.nexus" ]; then
    log "Creating /root/.nexus directory..."
    mkdir -p /root/.nexus || error_exit "Failed to create /root/.nexus"
fi

# Ensure node-id file exists
if [ ! -f "$NODE_ID_PATH" ]; then
    if [ -f "$WALLET_NODE_ID" ]; then
        log "Copying node-id from /wallet to /root/.nexus..."
        cp "$WALLET_NODE_ID" "$NODE_ID_PATH" || error_exit "Failed to copy node-id file"
        chmod 600 "$NODE_ID_PATH" || error_exit "Failed to set permissions on node-id"
    else
        error_exit "No node-id found in /wallet or /root/.nexus. Aborting."
    fi
else
    log "node-id file already exists in /root/.nexus"
fi

# Ensure ENDPOINT_URL has a default value
: "${ENDPOINT_URL:=beta.orchestrator.nexus.xyz}"
log "Running prover with ENDPOINT_URL: $ENDPOINT_URL"

# Start the application
exec /app/nexus-network start --env beta
