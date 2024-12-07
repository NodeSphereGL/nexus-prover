import os
import re

def update_proxy_env():
    base_dir = os.path.abspath("../")
    proxy_list_path = os.path.join(base_dir, "proxy", "list.txt")
    wallet_dir = os.path.join(base_dir, "wallet")
    env_file_path = os.path.join(base_dir, "nexus_docker", ".env")
    output_file_path = os.path.join(base_dir, "output", "proxy.txt")

    # Step 1: Read proxy list from list.txt
    try:
        with open(proxy_list_path, 'r') as proxy_file:
            proxy_lines = proxy_file.readlines()
    except FileNotFoundError:
        print(f"Error: Proxy list file not found at {proxy_list_path}")
        return

    formatted_proxies = []

    # Step 2: Format the proxy lines (unchanged)
    for line in proxy_lines:
        line = line.strip()
        if line:
            parts = line.split(':')
            if len(parts) == 4:
                ip, port, user, password = parts
                formatted_proxy = f"http://{user}:{password}@{ip}:{port}"
                formatted_proxies.append(formatted_proxy)
            else:
                print(f"Error: Invalid proxy format in line: {line}")

    if not formatted_proxies:
        print("Error: No valid proxies found.")
        return

    # Step 3 & 4: Get wallet numbers and handle insufficient proxies (modified)
    wallet_numbers = []
    for subdir in os.listdir(wallet_dir):
        if os.path.isdir(os.path.join(wallet_dir, subdir)):
            match = re.match(r"n(\d{3})", subdir)
            if match:
                wallet_number = int(match.group(1)) # Convert to integer for indexing
                wallet_numbers.append(wallet_number)

    if not wallet_numbers:
        print("Error: No wallet directories found.")
        return

    # Assign proxies based on wallet number, handling out-of-bounds indices
    proxy_assignments = []
    for wallet_number in wallet_numbers:
        proxy_index = wallet_number -1 # Adjust for 0-based indexing
        if 0 <= proxy_index < len(formatted_proxies):
            proxy = formatted_proxies[proxy_index]
            new_env_lines.append(f"PROXY_{wallet_number}={proxy}\n")
            proxy_assignments.append(f"PROXY_{wallet_number}|{proxy}")
            print(f"Added/Updated: PROXY_{wallet_number}={proxy}")
        else:
            print(f"Warning: No proxy found for wallet number {wallet_number}.")


    # Steps 5-9 (unchanged):  Read, modify, and write .env and proxy.txt files.  (These sections remain the same)

    # Step 6: Read current .env file and remove old PROXY_xxx entries (unchanged)
    if os.path.exists(env_file_path):
        with open(env_file_path, 'r') as env_file:
            env_lines = env_file.readlines()
    else:
        env_lines = []

    new_env_lines = [line for line in env_lines if not re.match(r"PROXY_\d{3}=", line)]


    # Step 7: Add new PROXY_xxx entries for each wallet (modified - uses wallet_number directly)

    # Step 8: Write updated .env file (unchanged)
    try:
        with open(env_file_path, 'w') as env_file:
            env_file.writelines(new_env_lines)
        print(f".env file updated successfully.")
    except Exception as e:
        print(f"Error: Unable to write to .env file: {e}")

    # Step 9: Write proxy assignments to proxy.txt (unchanged)
    try:
        os.makedirs(os.path.join(base_dir, "output"), exist_ok=True)
        with open(output_file_path, 'w') as output_file:
            output_file.write("\n".join(proxy_assignments) + "\n")
        print(f"Proxy assignments written to {output_file_path}.")
    except Exception as e:
        print(f"Error: Unable to write to {output_file_path}: {e}")

if __name__ == "__main__":
    update_proxy_env()