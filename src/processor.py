import pandas as pd
from bs4 import BeautifulSoup
import requests
import ast
from io import StringIO
from pathlib import Path
from .utils import Logger, HEADERS, COOKIES


class DataProcessor:
    def __init__(self):
        self.output_dir = Path('./data/classes')
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def extract_student_data(self, html_content, kode, matakuliah, kelas):
        soup = BeautifulSoup(html_content, 'html.parser')
        table = soup.find('table')

        if table is None:
            raise ValueError("Student table not found in the HTML content")

        html_io = StringIO(str(table))
        df = pd.read_html(html_io)[0]
        num_columns = len(df.columns)

        Logger.info(
            f"Found {num_columns} columns in the table: {df.columns.tolist()}")

        if num_columns == 7:
            df.columns = ['NO', 'NIM', 'NAMA MAHASISWA',
                          'NAMA MK', 'NAMA DOSEN', 'TGL', 'STATUS']
        else:
            df.columns = ['NO', 'NIM', 'NAMA MAHASISWA',
                          'NAMA MK', 'NAMA DOSEN', 'TGL']

        # Add KELAS, KODE, and MATAKULIAH information
        df['KELAS'] = kelas
        df['KODE'] = kode
        df['MATAKULIAH'] = matakuliah

        return df

    def process_user_links(self, filtered_df):
        for index, row in filtered_df.iterrows():
            kode = row['KODE']
            matakuliah = row['MATAKULIAH']
            kelas = row['KELAS']

            try:
                # Safely evaluate the string representation of the links list
                if isinstance(row['LINKS'], str):
                    links = ast.literal_eval(row['LINKS'])
                else:
                    links = row['LINKS']

                user_links = [link['url']
                              for link in links if link['type'] == 'User List']

                if not user_links:
                    Logger.warning(
                        f"No user links found for {kode} {matakuliah} {kelas}")
                    continue

                for user_link in user_links:
                    Logger.info(
                        f"Processing {kode} {matakuliah} {kelas} from {user_link}")
                    response = requests.get(
                        user_link, headers=HEADERS, cookies=COOKIES, timeout=10)
                    response.raise_for_status()

                    # Pass class information to extract_student_data
                    students_df = self.extract_student_data(
                        response.text, kode, matakuliah, kelas)
                    filename = f"{kode}_{kelas}_{matakuliah.replace(' ', '_')}.csv"
                    filepath = self.output_dir / filename
                    students_df.to_csv(filepath, index=False)
                    Logger.success(f"Saved data to {filepath}")

            except Exception as e:
                Logger.error(
                    f"Error processing {kode} {matakuliah} {kelas}: {str(e)}")
