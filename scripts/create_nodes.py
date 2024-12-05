import os
import re
from datetime import datetime
import shutil

def get_highest_wallet_number(wallet_dir):
    """Gets the highest wallet number based on the subdirectory names inside the wallet directory."""
    max_number = 0
    for subdir in os.listdir(wallet_dir):
        match = re.match(r"n(\d{3})", subdir)
        if match:
            number = int(match.group(1))
            if number > max_number:
                max_number = number
    return max_number

def create_wallets(num_wallets):
    base_dir = os.path.abspath("../")
    wallet_base_dir = os.path.join(base_dir, "wallet")
    docker_dir = os.path.join(base_dir, "nexus_docker")
    docker_compose_path = os.path.join(docker_dir, "docker-compose.yml")

    # Step 1: Backup docker-compose.yml
    timestamp = datetime.now().strftime("%d%m%Y_%H%M%S")
    docker_compose_backup_path = f"{docker_compose_path}.bak.{timestamp}"

    shutil.copy(docker_compose_path, docker_compose_backup_path)
    print(f"Backup created: {docker_compose_backup_path}")

    # Step 2: Get the highest numbered wallet subdirectory
    highest_wallet_number = get_highest_wallet_number(wallet_base_dir)
    start_number = highest_wallet_number + 1

    # Step 3: Add a one-time comment to docker-compose.yml before adding new entries
    docker_comment = f"\n#\n# Create new {num_wallets} services starting from n{start_number:03d} on {timestamp}\n#\n"

    with open(docker_compose_path, 'a') as docker_compose_file:
        docker_compose_file.write(docker_comment)

    # Step 4: Create new wallet directories and update docker-compose.yml
    for i in range(start_number, start_number + num_wallets):
        wallet_filename = f"n{i:03d}"
        wallet_path = os.path.join(wallet_base_dir, wallet_filename)

        # Create new wallet directory
        if not os.path.exists(wallet_path):
            print(f"Creating wallet directory: {wallet_filename}")
            os.makedirs(wallet_path, exist_ok=True)
        else:
            print(f"Wallet {wallet_filename} already exists, skipping creation.")

        # Update docker-compose.yml with new service configuration
        docker_service_entry = f"""
  n{i:03d}:
    image: toanbk/nexus-prover:latest
    volumes:
      - ${{WALLET_DIR}}/{wallet_filename}:/wallet
    ulimits:
      nofile:
        soft: 65535
        hard: 65535
    environment:
      - ENDPOINT_URL=${{ENDPOINT_URL}}
      - http_proxy=${{PROXY_{i:03d}}}
      - HTTP_PROXY=${{PROXY_{i:03d}}}
      - https_proxy=${{PROXY_{i:03d}}}
      - HTTPS_PROXY=${{PROXY_{i:03d}}}
      - no_proxy=${{NO_PROXY}}
      - NO_PROXY=${{NO_PROXY}}
    restart: always
"""
        with open(docker_compose_path, 'a') as docker_compose_file:
            docker_compose_file.write(docker_service_entry)

if __name__ == "__main__":
    num_wallets = int(input("Enter the number of wallets to create: "))
    create_wallets(num_wallets)
