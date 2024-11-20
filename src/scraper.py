from src.utils import Logger, HEADERS, COOKIES
import pandas as pd
from bs4 import BeautifulSoup
import requests
from io import StringIO
from pathlib import Path
import sys
sys.path.append('.')  # Add the project root to Python path


class SpotScraper:
    def __init__(self):
        self.url = "https://spot.upi.edu/adm/kelas"

    def extract_links(self, td_element):
        links = []
        if td_element:
            a_tags = td_element.find_all('a')
            for a in a_tags:
                href = a.get('href', '')
                icon_type = 'User List' if 'fa-user' in str(a) else 'BAP'
                links.append({'url': href, 'type': icon_type})
        return links

    def format_prodi_values(self, values):
        """Format PRODI values in a more readable way"""
        formatted_values = []
        for value in sorted(values):
            if pd.isna(value):
                continue
            # Add numbering and proper spacing
            formatted_values.append(f"    - {value}")
        return formatted_values

    def display_filter_options(self, df):
        Logger.info("Available columns for filtering:")
        for idx, column in enumerate(df.columns[:-1], 1):
            print(f"{idx}. {column}")
            if column == 'PRODI':
                unique_values = df[column].unique()
                Logger.info("Available PRODI values:")
                for value in self.format_prodi_values(unique_values):
                    print(value)
                print()  # Add empty line for better readability
            elif column == 'SEMESTER':
                unique_values = sorted(df[column].unique())
                print(
                    f"   Available values: {', '.join(map(str, unique_values))}\n")

    def get_user_filter(self):
        column = input(
            "\nEnter the column name to filter (or 'none' to skip filtering): ").strip()
        if column.lower() == 'none':
            return None, None
        value = input(f"Enter the value to filter for {column}: ").strip()
        return column, value

    def scrape_classes(self):
        try:
            Logger.info("Fetching data from SPOT UPI...")
            response = requests.get(
                self.url, cookies=COOKIES, headers=HEADERS, timeout=10)
            response.raise_for_status()

            Logger.info("Saving raw HTML response...")
            with open('./data/mata_kuliah.html', 'w', encoding='utf-8') as f:
                f.write(response.text)

            soup = BeautifulSoup(response.text, 'html.parser')
            table = soup.find('table')

            if table is None:
                Logger.error("Table not found in the HTML content")
                raise ValueError("Table not found in the HTML content")

            rows = table.find_all('tr')
            data = []
            headers = [th.text.strip()
                       for th in rows[0].find_all(['th', 'td'])[:-1]]
            headers.append('LINKS')

            for row in rows[1:]:
                cols = row.find_all('td')
                if len(cols) >= 1:
                    row_data = [col.text.strip() for col in cols[:-1]]
                    links = self.extract_links(cols[-1])
                    row_data.append(links)
                    data.append(row_data)

            df = pd.DataFrame(data, columns=headers)
            return df

        except Exception as e:
            Logger.error(f"Error in scrape_classes: {str(e)}")
            raise
