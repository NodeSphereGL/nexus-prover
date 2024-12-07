import os
import re

def update_proxy_env():
    base_dir = os.path.abspath("../")
    proxy_list_path = os.path.join(base_dir, "proxy", "list.txt")
    wallet_dir = os.path.join(base_dir, "wallet")
    env_file_path = os.path.join(base_dir, "nexus_docker", ".env")
    output_file_path = os.path.join(base_dir, "output", "proxy.txt")

    # --- Step 1: Read and validate proxy list ---
    try:
        with open(proxy_list_path, 'r') as proxy_file:
            proxy_lines = proxy_file.readlines()
    except FileNotFoundError:
        print(f"Error: Proxy list file not found at {proxy_list_path}")
        return False  # Indicate failure

    formatted_proxies = []
    for i, line in enumerate(proxy_lines):
        line = line.strip()
        if line:
            parts = line.split(':')
            if len(parts) == 4:
                try:
                    ip, port, user, password = parts
                    formatted_proxy = f"http://{user}:{password}@{ip}:{port}"
                    formatted_proxies.append(formatted_proxy)
                except ValueError:
                    print(f"Error: Invalid proxy format in line {i+1}: {line}")
                    return False # Indicate failure
            else:
                print(f"Error: Invalid proxy format in line {i+1}: {line}")
                return False # Indicate failure

    if not formatted_proxies:
        print("Error: No valid proxies found.")
        return False  # Indicate failure


    # --- Step 2: Get wallet numbers ---
    wallet_numbers = []
    try:
        for subdir in os.listdir(wallet_dir):
            if os.path.isdir(os.path.join(wallet_dir, subdir)):
                match = re.match(r"n(\d{3})", subdir)
                if match:
                    wallet_number = int(match.group(1))
                    wallet_numbers.append(wallet_number)
    except FileNotFoundError:
        print(f"Error: Wallet directory not found at {wallet_dir}")
        return False # Indicate failure

    if not wallet_numbers:
        print("Error: No wallet directories found.")
        return False  # Indicate failure
    
    # sort wallet number
    wallet_numbers.sort()

    # --- Step 3: Assign proxies based on wallet number ---
    proxy_assignments = []
    new_env_lines = []
    for wallet_number in wallet_numbers:
        proxy_index = wallet_number - 1
        if 0 <= proxy_index < len(formatted_proxies):
            proxy = formatted_proxies[proxy_index]
            formatted_wallet_number = "{:03d}".format(wallet_number) #format to 3 digits with leading zeros

            new_env_lines.append(f"PROXY_{formatted_wallet_number}={proxy}\n")
            proxy_assignments.append(f"PROXY_{formatted_wallet_number}|{proxy}")
            print(f"Added/Updated: PROXY_{formatted_wallet_number}={proxy}")
        else:
            print(f"Warning: No proxy found for wallet number {formatted_wallet_number}.")

    # --- Step 4: Sort proxy assignments by wallet number ---
    proxy_assignments.sort(key=lambda x: int(re.search(r"(\d+)", x.split('|')[0]).group(1)))

    # --- Step 5: Read and update .env file ---
    try:
        if os.path.exists(env_file_path):
            with open(env_file_path, 'r') as env_file:
                env_lines = env_file.readlines()
                #Remove existing proxy lines
                existing_proxy_lines = [line for line in env_lines if re.match(r"PROXY_\d{3}=", line)]
                for line in existing_proxy_lines:
                    if line in env_lines:
                        env_lines.remove(line)

        with open(env_file_path, 'w') as env_file:
            env_file.writelines(env_lines + new_env_lines)
        print(f".env file updated successfully.")
    except Exception as e:
        print(f"Error: Unable to write to .env file: {e}")
        return False # Indicate failure


    # --- Step 6: Write proxy assignments to proxy.txt ---
    try:
        os.makedirs(os.path.join(base_dir, "output"), exist_ok=True)
        with open(output_file_path, 'w') as output_file:
            output_file.write("\n".join(proxy_assignments) + "\n")
        print(f"Proxy assignments written to {output_file_path}.")
    except Exception as e:
        print(f"Error: Unable to write to {output_file_path}: {e}")
        return False  # Indicate failure

    return True  # Indicate success


if __name__ == "__main__":
    if update_proxy_env():
        print("Proxy configuration completed successfully.")
    else:
        print("Proxy configuration failed.")