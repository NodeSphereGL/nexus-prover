import os
import sys

def update_prover_id(prover_id, wallet_dir):
    """Creates or updates the node-id file in each subdirectory of the wallet directory."""
    try:
        for subdir in os.listdir(wallet_dir):
            subdir_path = os.path.join(wallet_dir, subdir)
            if os.path.isdir(subdir_path):
                prover_id_path = os.path.join(subdir_path, "node-id")
                try:
                    with open(prover_id_path, "w") as f:
                        f.write(prover_id)
                    print(f"Prover ID updated in: {prover_id_path}")
                except Exception as e:
                    print(f"Error writing prover ID to {prover_id_path}: {e}")
                    return False # Indicate failure
        return True # Indicate success
    except FileNotFoundError:
        print(f"Error: Wallet directory not found at {wallet_dir}")
        return False # Indicate failure
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False # Indicate failure


if __name__ == "__main__":
    base_dir = os.path.abspath("../")
    wallet_dir = os.path.join(base_dir, "wallet")

    while True:
        prover_id = input("Enter the prover ID: ")
        if prover_id:  # Check if the input is not empty
            break
        else:
            print("Prover ID cannot be empty. Please enter a valid ID.")

    if update_prover_id(prover_id, wallet_dir):
        print("Prover ID updated successfully in all wallet directories.")
    else:
        print("Failed to update prover ID.")
        sys.exit(1)