from parser_api.config.browser import LOG_MAX_SIZE_MB
from datetime import datetime
from pathlib import Path
import logging
import sys

def setup_logging() -> logging.Logger:
    """Logging system setup"""
    log_dir = Path(__file__).parent.parent / "logs"
    log_dir.mkdir(exist_ok=True)

    clean_logs_if_needed(log_dir, max_size_mb=LOG_MAX_SIZE_MB)
    
    logging.basicConfig(
        level=logging.INFO,
        datefmt="%Y-%m-%d %H:%M:%S",
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_dir / f"lenta_parser_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"),
            logging.StreamHandler(sys.stdout)
        ]
    )
    return logging.getLogger("LentaParser")

def clean_logs_if_needed(log_dir: Path, max_size_mb: float):
    """Clearing logs if necessary"""
    try:
        total_size = sum(f.stat().st_size for f in log_dir.glob('*') if f.is_file())
        if total_size > max_size_mb * 1024 * 1024:
            for log_file in log_dir.glob('*'):
                try:
                    log_file.unlink()
                except Exception as e:
                    logging.warning(f"Failed to delete log file {log_file}: {str(e)}")
    except Exception as e:
        logging.error(f"Error during log cleanup: {str(e)}") 