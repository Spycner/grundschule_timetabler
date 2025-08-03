#!/usr/bin/env python
"""Command-line script to run database seeders."""

import argparse
import logging
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.config import get_settings
from src.models.database import SessionLocal
from src.seeders import DatabaseSeeder

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    """Main function to run seeders."""
    parser = argparse.ArgumentParser(description="Database seeder for development data")
    parser.add_argument(
        "--clear",
        action="store_true",
        help="Clear all data before seeding",
    )
    parser.add_argument(
        "--clear-only",
        action="store_true",
        help="Only clear data, don't seed",
    )
    args = parser.parse_args()

    settings = get_settings()
    logger.info(f"Using database: {settings.database_url}")

    # Create database session
    db = SessionLocal()
    seeder = DatabaseSeeder(db)

    try:
        if args.clear_only:
            logger.info("Clearing all data...")
            stats = seeder.clear_all()
            logger.info(f"Cleared data: {stats}")
        else:
            if args.clear:
                logger.info("Clearing existing data...")
                stats = seeder.clear_all()
                logger.info(f"Cleared data: {stats}")

            logger.info("Seeding database...")
            stats = seeder.seed_all()
            logger.info(f"Seeding completed: {stats}")

    except Exception as e:
        logger.error(f"Error: {e}")
        sys.exit(1)
    finally:
        db.close()


if __name__ == "__main__":
    main()
