#!/usr/bin/env python
import os
import sys
import argparse
import logging
import subprocess
import signal
import time

import json


import optimor.core as core


SELENIUM_PATH = os.getenv(
    "SELENIUM_PATH",
    os.path.join(
        os.path.expanduser("~"),
        "selenium-server-standalone-2.28.0.jar"
    )
)


DESCRIPTION = """
Script for collecting the international landline tariffs from
mobile providers websites.
"""


def setup_logging():
    """Logging setup

    :returns: set logger object
    :rtype: logging.Logger
    """
    logger = logging.getLogger('')
    logger.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    ch.setFormatter(formatter)

    logger.addHandler(ch)

    return logger


logger = setup_logging()


def parse_args():
    """Parsing args from the terminal and check if they make any sense.

    :returns: args object
    :rtype: argparse.Namespace
    """
    parser = argparse.ArgumentParser(
        description=DESCRIPTION,
        formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument(
        'input_path',
        help='Path to json input file storing names of the countries.'
    )

    return parser.parse_args()


def run_selenium():
    """Method to kick off selenium in background

    :returns: Process pid
    :rtype: int
    """
    pid = subprocess.Popen(["java", "-jar", SELENIUM_PATH]).pid
    time.sleep(2)
    return pid


def kill_selenium(pid):
    """Kill selenium when done.
    :param pid: Pid of the selenium process.
    :type pid: int
    """
    os.kill(pid, signal.SIGTERM)


def main():
    logger.info("Running scraper for O2")
    args = parse_args()

    if not os.path.exists(args.input_path):
        logger.error("Input path doesn't exist! %s", args.input_path)
        sys.exit(1)

    if not os.path.exists(args.input_path):
        logger.error("Selenium path doesn't exist! %s", SELENIUM_PATH)
        sys.exit(1)

    logger.info("Loading coutries from file: %s", args.input_path)
    countries = json.load(open(args.input_path, 'r'))
    logger.info("Loaded following countries: %s", countries)

    pid = run_selenium()
    browser = core.O2Browser()

    try:
        for country in countries:
            logger.info("Scraping value for %s", country)
            browser.query_country(country)
            val = browser.get_land_line_value() or 'NA'
            print "%s => %s" % (country, val)
    except Exception:
        raise
    finally:
        browser.close()
        kill_selenium(pid)


if __name__ == '__main__':
    main()
