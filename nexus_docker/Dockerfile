# Use the base image from Ubuntu
FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    vim\
    net-tools \
    wget \
    curl \
    tzdata \
    protobuf-compiler \
    && rm -rf /var/lib/apt/lists/*

ENV NEXUS_HOME=/root/.nexus
ENV RUST_BACKTRACE=full

ENV TZ=UTC
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN mkdir -p /wallet

WORKDIR /app

COPY ./bin/src ./src
COPY ./bin/prover ./

RUN chmod +x ./prover

# Copy the entrypoint script
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

# Use the entrypoint script to run the prover with the provided ENDPOINT_URL
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
