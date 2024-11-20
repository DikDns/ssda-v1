import pandas as pd
from pathlib import Path
import re
from src.utils import Logger


class DataMerger:
    def __init__(self):
        self.classes_dir = Path('./data/classes')
        self.output_dir = Path('./data/merged')
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def extract_angkatan(self, nim):
        """Extract angkatan from NIM (e.g., '2344033' -> '23', '2454234' -> '24')"""
        try:
            return str(nim)[:2]
        except:
            return None

    def extract_kelas_from_filename(self, filename):
        """Extract kelas from filename (e.g., 'RL220_3A_PERANCANGAN...' -> '3A')"""
        try:
            parts = filename.stem.split('_')
            if len(parts) >= 2:
                return parts[1]
            return None
        except:
            return None

    def merge_by_angkatan(self):
        """Merge all CSV files in classes directory by angkatan"""
        try:
            # Get all CSV files
            csv_files = list(self.classes_dir.glob('*.csv'))
            if not csv_files:
                Logger.warning("No CSV files found in classes directory")
                return

            Logger.info(f"Found {len(csv_files)} CSV files to process")

            # Dictionary to store DataFrames by angkatan
            angkatan_dfs = {}

            # Process each CSV file
            for csv_file in csv_files:
                try:
                    # Read the CSV file
                    df = pd.read_csv(csv_file)

                    # Extract kelas from filename
                    kelas = self.extract_kelas_from_filename(csv_file)
                    if kelas:
                        df['KELAS'] = kelas
                    else:
                        Logger.warning(
                            f"Could not extract KELAS from filename: {csv_file.name}")
                        continue

                    # Extract angkatan for each student
                    df['ANGKATAN'] = df['NIM'].apply(self.extract_angkatan)

                    # Group by angkatan and add to respective dictionary
                    for angkatan, group_df in df.groupby('ANGKATAN'):
                        if angkatan and angkatan.isdigit():  # Ensure valid angkatan
                            if angkatan not in angkatan_dfs:
                                angkatan_dfs[angkatan] = []
                            angkatan_dfs[angkatan].append(group_df)
                            Logger.info(
                                f"Processed {csv_file.name} for angkatan {angkatan}")

                except Exception as e:
                    Logger.error(f"Error processing {csv_file.name}: {str(e)}")
                    continue

            # Merge and save files by angkatan
            for angkatan, dfs in angkatan_dfs.items():
                if dfs:
                    # Concatenate all DataFrames for this angkatan
                    merged_df = pd.concat(dfs, ignore_index=True)

                    # Get unique students (by NIM) with their first occurrence
                    unique_students = merged_df.sort_values(
                        'TGL').drop_duplicates(subset=['NIM'], keep='first')

                    # Count total and unique students
                    total_records = len(merged_df)
                    unique_records = len(unique_students)
                    Logger.info(
                        f"Angkatan 20{angkatan} - Total records: {total_records}, Unique students: {unique_records}")

                    # Select only required columns and sort
                    final_df = unique_students[[
                        'NIM', 'NAMA MAHASISWA', 'KELAS', 'ANGKATAN']]
                    final_df = final_df.sort_values(
                        ['KELAS', 'NAMA MAHASISWA'])

                    # Save merged file
                    output_file = self.output_dir / \
                        f'angkatan_20{angkatan}_merged.csv'
                    final_df.to_csv(output_file, index=False)
                    Logger.success(
                        f"Saved merged data for angkatan 20{angkatan} to {output_file}")
                    Logger.info(
                        f"Removed {total_records - unique_records} duplicate student records")

            Logger.success("Merging process completed successfully!")

        except Exception as e:
            Logger.error(f"Error in merge process: {str(e)}")


def main():
    try:
        merger = DataMerger()
        merger.merge_by_angkatan()
    except Exception as e:
        Logger.error(f"Error in main process: {str(e)}")


if __name__ == "__main__":
    main()
