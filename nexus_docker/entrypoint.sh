#!/bin/bash
# Entry point script to run prover with an endpoint URL

# Set default value for ENDPOINT_URL if not provided
: "${ENDPOINT_URL:=beta.orchestrator.nexus.xyz}"

echo "Running prover with ENDPOINT_URL: $ENDPOINT_URL"

# Run the prover binary with the endpoint URL
/usr/local/bin/prover "$ENDPOINT_URL"
