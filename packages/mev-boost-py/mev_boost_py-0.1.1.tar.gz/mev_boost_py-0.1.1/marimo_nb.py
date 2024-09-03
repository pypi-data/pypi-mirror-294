import marimo

__generated_with = "0.8.7"
app = marimo.App(width="medium")


@app.cell
def __():
    import requests
    import json
    import os
    import concurrent.futures
    from threading import Lock, Semaphore
    import time


    def fetch_proposer_payloads(slot, rate_limiter):
        """
        Fetch proposer payloads for a specific slot.

        Args:
            slot (int): The slot number to fetch data for.
            rate_limiter (Semaphore): Semaphore to control the rate limit.

        Returns:
            dict: Dictionary containing the slot and its corresponding proposer payloads or None if no data or error.
        """
        with rate_limiter:
            url = f"https://boost-relay-holesky.flashbots.net/relay/v1/data/bidtraces/proposer_payload_delivered?slot={slot}"

            try:
                response = requests.get(url)
                if response.status_code == 200:
                    payloads = response.json()
                    return payloads if payloads else None
                else:
                    print(
                        f"Failed to fetch proposer payloads for slot {slot}. Status code: {response.status_code}"
                    )
                    return None
            except Exception as e:
                print(f"An error occurred while fetching slot {slot}: {e}")
                return None


    def save_payloads_to_file(payloads, filename="block_payloads.json", lock=None):
        """
        Save proposer payloads to a .json file in a list format.

        Args:
            payloads (list): List of payload entries.
            filename (str): The filename to save the payloads to.
            lock (Lock): A threading lock to synchronize file access.
        """
        if lock:
            lock.acquire()

        try:
            with open(filename, "w") as f:
                json.dump(payloads, f, indent=2)
            print(f"Payloads saved to {filename}")
        except Exception as e:
            print(f"An error occurred while saving to file: {e}")
        finally:
            if lock:
                lock.release()


    def main():
        end_slot = 2448969  # Ending slot
        start_slot = end_slot - 15000  # Starting slot
        payloads_list = []  # List to store payloads
        lock = Lock()  # Lock to ensure thread-safe file access

        rate_limiter = Semaphore(100)  # Semaphore to allow 100 requests per second

        null_entry_template = {
            "slot": None,
            "parent_hash": None,
            "block_hash": None,
            "builder_pubkey": None,
            "proposer_pubkey": None,
            "proposer_fee_recipient": None,
            "gas_limit": None,
            "gas_used": None,
            "value": None,
            "num_tx": None,
            "block_number": None,
        }

        with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
            future_to_slot = {
                executor.submit(fetch_proposer_payloads, slot, rate_limiter): slot
                for slot in range(start_slot, end_slot)
            }

            for future in concurrent.futures.as_completed(future_to_slot):
                slot = future_to_slot[future]
                slot_data = future.result()

                if slot_data is not None:
                    print(f"Fetched payloads for slot {slot}")
                    payloads_list.extend(slot_data)
                else:
                    print(f"No data for slot {slot}, adding null entry.")
                    null_entry = null_entry_template.copy()
                    null_entry["slot"] = str(slot)
                    payloads_list.append(null_entry)

                # Sleep briefly to maintain rate limit
                time.sleep(
                    0.05
                )  # 10 milliseconds between each request batch to achieve 100 requests per second

        save_payloads_to_file(payloads_list, lock=lock)


    if __name__ == "__main__":
        main()
    return (
        Lock,
        Semaphore,
        concurrent,
        fetch_proposer_payloads,
        json,
        main,
        os,
        requests,
        save_payloads_to_file,
        time,
    )


@app.cell
def __():
    import polars as pl
    return pl,


@app.cell
def __(pl):
    df = pl.read_json("block_payloads.json").sort(by="slot", descending=True)
    return df,


@app.cell
def __(df):
    df
    return


@app.cell
def __():
    return


if __name__ == "__main__":
    app.run()
