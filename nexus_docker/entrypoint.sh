#!/bin/bash
# Entry point script to run prover with an endpoint URL

# Check if /root/.nexus directory exists
if [ -d "/root/.nexus" ]; then
    cp /wallet/node-id /root/.nexus/
else
    echo "/root/.nexus directory does not exist."
    # If /root/.nexus does not exist, check for node-id in /wallet
    if [ -f "/wallet/node-id" ]; then
        echo "Found /wallet/node-id. Copying to /root/.nexus."
        mkdir -p /root/.nexus
        cp /wallet/node-id /root/.nexus/
    else
        echo "No node-id found in /wallet or /root/.nexus."
    fi
fi

# Set default value for ENDPOINT_URL if not provided
: "${ENDPOINT_URL:=beta.orchestrator.nexus.xyz}"

echo "Running prover with ENDPOINT_URL: $ENDPOINT_URL"

# Start the application
echo "2" | /app/nexus-network start --env beta
