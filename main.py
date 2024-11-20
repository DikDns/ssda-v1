from src.utils import Logger
from src.scraper import SpotScraper
from src.processor import DataProcessor
from src.merger import DataMerger


def main():
    try:
        # Initialize components
        scraper = SpotScraper()
        processor = DataProcessor()
        merger = DataMerger()

        # Scrape class data
        Logger.info("Starting class data scraping...")
        df = scraper.scrape_classes()

        # Get and apply filters
        scraper.display_filter_options(df)
        column, value = scraper.get_user_filter()

        # Apply filter if specified
        if column and value:
            Logger.info(f"Filtering data where {column} = {value}...")
            filtered_df = df[df[column].astype(
                str).str.contains(value, case=False, na=False)]
        else:
            Logger.info("No filtering applied...")
            filtered_df = df

        # Save filtered data
        filtered_df.to_csv('filtered_data.csv', index=False)
        Logger.info(f"Saved filtered data. Total rows: {len(filtered_df)}")

        # Process user links
        Logger.info("Starting user data processing...")
        processor.process_user_links(filtered_df)

        # Merge data by angkatan
        Logger.info("Starting data merging by angkatan...")
        merger.merge_by_angkatan()

        Logger.success("All operations completed successfully!")

    except Exception as e:
        Logger.error(f"Error in main process: {str(e)}")


if __name__ == "__main__":
    main()
