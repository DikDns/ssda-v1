# Scraper for SPOT-UPI Data Account

A Python-based tool for scraping and processing class data from SPOT UPI

## Features

- Scrapes class data from SPOT UPI
- Filters data based on user-defined criteria
- Processes student lists from each class
- Merges student data by angkatan (year)
- Removes duplicate student entries
- Colored logging for better visibility

## Project Structure

```bash
.
├── data/
│ ├── classes/ # Individual class CSV files
│ └── merged/ # Merged data by angkatan
├── src/
│ ├── init.py
│ ├── scraper.py # Class data scraping functionality
│ ├── processor.py # Student data processing
│ ├── merger.py # Data merging utilities
│ └── utils.py # Common utilities and logging
├── .env # Environment variables (not in repo)
├── .gitignore
├── requirements.txt
├── README.md
└── main.py # Main execution script
```

## Prerequisites

- Python 3.8 or higher
- SPOT UPI account credentials

## Installation

1. Clone the repository:

```bash
git clone https://github.com/DikDns/ssda-v1.git # HTTPS
# or
git clone git@github.com:DikDns/ssda-v1.git # SSH
cd ssda-v1
```

2. Create a virtual environment (recommended):

```bash
python -m venv venv
source venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory with your SPOT UPI credentials:

```
CAS_AUTH=your_cas_auth_token
LARAVEL_SESSION=your_laravel_session_token
XSRF_TOKEN=your_xsrf_token
```

## Usage

1. Run the main script:

```bash
python main.py
```

2. The script will:
   - Scrape class data from SPOT UPI
   - Display available filtering options
   - Ask for filtering preferences
   - Process student data for each class
   - Merge data by angkatan
   - Save results in the `data` directory

## Data Structure

### Class Data Columns

- KODE (Course Code)
- MATAKULIAH (Course Name)
- KELAS (Class)
- PRODI (Study Program)
- SEMESTER
- LINKS (URLs to student lists and BAP)

### Student Data Columns

- NIM (Student ID)
- NAMA MAHASISWA (Student Name)
- KELAS (Class)
- ANGKATAN (Year)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## Security Notes

- Never commit the `.env` file containing your credentials
- Keep your SPOT UPI cookies secure
- Update cookies when they expire

## License

MIT License
