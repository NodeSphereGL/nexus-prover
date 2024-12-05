#!/bin/bash
# Entry point script to run prover with an endpoint URL

# Set default value for ENDPOINT_URL if not provided
: "${ENDPOINT_URL:=beta.orchestrator.nexus.xyz}"

echo "Running prover with ENDPOINT_URL: $ENDPOINT_URL"

ls -l /root/.nexus

# Run the prover binary with the endpoint URL
/root/.nexus/prover "$ENDPOINT_URL"
