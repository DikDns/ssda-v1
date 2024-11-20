import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Logger:
    # ANSI color codes
    BLUE = '\033[94m'      # Info
    RED = '\033[91m'       # Error
    YELLOW = '\033[93m'    # Warning
    GREEN = '\033[92m'     # Success
    RESET = '\033[0m'      # Reset color

    @staticmethod
    def info(message):
        """Log info message in blue"""
        print(f"{Logger.BLUE}[INFO] {message}{Logger.RESET}\n")

    @staticmethod
    def error(message):
        """Log error message in red"""
        print(f"{Logger.RED}[ERROR] {message}{Logger.RESET}\n")

    @staticmethod
    def warning(message):
        """Log warning message in yellow"""
        print(f"{Logger.YELLOW}[WARNING] {message}{Logger.RESET}\n")

    @staticmethod
    def success(message):
        """Log success message in green"""
        print(f"{Logger.GREEN}[SUCCESS] {message}{Logger.RESET}\n")


# Common configuration
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Connection': 'keep-alive',
}

COOKIES = {
    'CASAuth': os.getenv('CAS_AUTH'),
    'laravel_session': os.getenv('LARAVEL_SESSION'),
    'XSRF-TOKEN': os.getenv('XSRF_TOKEN')
}
