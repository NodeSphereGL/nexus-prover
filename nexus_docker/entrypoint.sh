#!/bin/bash
# Entry point script to run prover with an endpoint URL

# Check if /root/.nexus directory exists
if [ -d "/root/.nexus" ]; then
    # Check if /root/.nexus contains the file "prover-id"
    if [ -f "/root/.nexus/prover-id" ]; then
        echo "Found /root/.nexus/prover-id. Copying to /wallet."
        cp /root/.nexus/prover-id /wallet/
    elif [ -f "/wallet/prover-id" ]; then
        echo "/root/.nexus/prover-id not found. Checking /wallet."
        # If /wallet/prover-id exists, copy it to /root/.nexus
        mkdir -p /root/.nexus
        cp /wallet/prover-id /root/.nexus/
        echo "Copied /wallet/prover-id to /root/.nexus."
    else
        echo "No prover-id found in either /root/.nexus or /wallet."
        # Remove /root/.nexus if no prover-id is found in either location
        rm -rf /root/.nexus
        echo "Removed /root/.nexus directory."
    fi
else
    echo "/root/.nexus directory does not exist."
    # If /root/.nexus does not exist, check for prover-id in /wallet
    if [ -f "/wallet/prover-id" ]; then
        echo "Found /wallet/prover-id. Copying to /root/.nexus."
        mkdir -p /root/.nexus
        cp /wallet/prover-id /root/.nexus/
    else
        echo "No prover-id found in /wallet or /root/.nexus."
    fi
fi

# Set default value for ENDPOINT_URL if not provided
: "${ENDPOINT_URL:=beta.orchestrator.nexus.xyz}"

echo "Running prover with ENDPOINT_URL: $ENDPOINT_URL"

# Run the prover binary with the endpoint URL
/app/prover "$ENDPOINT_URL"
