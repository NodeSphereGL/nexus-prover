# Base Install

    sudo apt update && apt upgrade -y
    sudo apt install vim zip unzip git curl wget -y && git config --global core.editor "vim" && sudo apt install make clang pkg-config libssl-dev build-essential python3-pip -y
    sudo apt install tar wget clang gcc tmux libleveldb-dev jq bsdmainutils git make ncdu htop lz4 screen bc fail2ban -y

    sudo apt-get install ca-certificates curl gnupg -y
    sudo install -m 0755 -d /etc/apt/keyrings
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
    sudo chmod a+r /etc/apt/keyrings/docker.gpg

    # Add the repository to Apt sources:
    echo \
    "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
    "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | \
    sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    sudo apt-get update

    sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin -y

    echo "Docker Installed Successfully!"
    echo "Check Docker: docker ps "

    docker pull toanbk/nexus-prover

# Config docker

    echo '{
    "dns": ["8.8.8.8", "8.8.4.4", "1.1.1.1"],
    "dns-opts": ["timeout:5", "attempts:5"],
    "max-concurrent-downloads": 10,
    "max-concurrent-uploads": 5,
    "default-address-pools": [
        {
        "base": "172.1.0.0/16",
        "size": 20
        },
        {
        "base": "172.2.0.0/16",
        "size": 20
        },
        {
        "base": "172.3.0.0/16",
        "size": 20
        },
        {
        "base": "172.4.0.0/16",
        "size": 20
        }
    ]
    }' | sudo tee /etc/docker/daemon.json > /dev/null

# Config file system

    echo '*        soft    nofile      865535' | sudo tee -a /etc/security/limits.conf > /dev/null
    echo '*        hard    nofile      865535' | sudo tee -a /etc/security/limits.conf > /dev/null
    echo 'root     soft    nofile      865535' | sudo tee -a /etc/security/limits.conf > /dev/null
    echo 'root     hard    nofile      865535' | sudo tee -a /etc/security/limits.conf > /dev/null

    echo 'session required pam_limits.so' | sudo tee -a /etc/pam.d/common-session > /dev/null
