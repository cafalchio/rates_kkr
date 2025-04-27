import logging
from processor.pensford_processor import PensfordProcessor

logging.basicConfig(format='%(asctime)s -> %(message)s', datefmt='%d %b %Y %I:%M:%S %p', level=logging.INFO)

logger = logging.getLogger(__name__)

def main():
    logger.info("Running Pensford ETL")
    processor = PensfordProcessor()
    processor.save_data()

if __name__ == "__main__":
    main()
