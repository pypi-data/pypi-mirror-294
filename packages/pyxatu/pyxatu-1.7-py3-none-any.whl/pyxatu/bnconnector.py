import os
import pandas as pd
import requests
from io import BytesIO
from datetime import datetime, timedelta
import logging
from pathlib import Path

class BnConnector:

    def download_mempool_data(self, date_string: str, buffer: int = 2, local_storage: bool = True) -> pd.DataFrame:
        # Parse the input date string
        dt = datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S')

        # Generate the required date strings for the current hour and the previous three hours
        date_list = [(dt - timedelta(hours=i)).strftime('%Y%m%d/%H.csv.gz') for i in range(buffer)]

        # Base URL
        base_url = 'https://archive.blocknative.com/'

        storage_dir = os.path.join(Path.home(), f"mempooldata/blocknative/")
        os.makedirs(storage_dir, exist_ok=True)

        # List to hold the dataframes
        dfs = []

        # Download each file and append to the list of dataframes
        for date in date_list:
            local_file_path = os.path.join(storage_dir, date.replace('/', '_'))  # Replace '/' with '_' for local file naming

            if local_storage and os.path.exists(local_file_path):
                # Load the file from local storage
                df = pd.read_csv(local_file_path, compression='gzip')
                print(f"Loaded {local_file_path} from local storage.")
            else:
                # Download from the server
                url = base_url + date
                logging.info(f"Downloading from {url}, This can take a few minutes...")
                response = requests.get(url)

                if response.status_code == 200:
                    # Load the CSV into a dataframe
                    df = pd.read_csv(BytesIO(response.content), compression='gzip', delimiter='\t')
                    dfs.append(df)

                    # Save to local storage if the flag is enabled
                    if local_storage:
                        df.to_csv(local_file_path, compression='gzip', index=False)
                        print(f"Saved {local_file_path} to local storage.")
                else:
                    print(f"Failed to download {url}")
                    continue

            dfs.append(df)

        # Concatenate all dataframes
        if dfs:
            combined_df = pd.concat(dfs, ignore_index=True)
            return combined_df
        else:
            return pd.DataFrame()