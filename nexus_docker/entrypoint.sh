#!/bin/bash
# Entry point script to run prover with an endpoint URL

# Check if /root/.nexus directory exists
if [ -d "/root/.nexus" ]; then
    cp /wallet/prover-id /root/.nexus/
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

# Start the application
/app/prover "$ENDPOINT_URL"
