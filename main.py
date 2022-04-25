#!/usr/bin/env python3

# from arlo_filename_test import PASSWORD
from arlo import Arlo

import datetime
import logging
import logging.config
import os
import yaml

from time import localtime, strftime

import config
import arlo_download

config = config.get_config()

SCRIPT_ROOT = config['paths']['script_root']
MOUNT_PATH = config['paths']['mount_path']

# PASSWORD = str(base64.b64encode(pw.encode("utf-8")), "utf-8")
logger = logging.getLogger(__name__)

def set_logger():
    """
    Setup logging configuration
    """
    path = os.path.join(SCRIPT_ROOT, 'logging.yaml')

    with open(path, 'rt') as f:
        config = yaml.safe_load(f.read())

    # get the file name from the handlers, append the date to the filename. 
        for i in (config["handlers"].keys()):
            local_datetime = str(strftime('%A, %d. %B %Y %I:%M%p', localtime()))
            print(local_datetime)

            if 'filename' in config['handlers'][i]:
                log_filename = config["handlers"][i]["filename"]
                base, extension = os.path.splitext(log_filename)
                today = datetime.date.today()
                
                log_filename = "{}_{}{}".format(base,
                                                today.strftime("%Y%m%d"),
                                                extension)
                config["handlers"][i]["filename"] = log_filename
            else:
                print("=========== ERROR STARTING LOG FILE, {} ===========",format(local_datetime))
        logger = logging.config.dictConfig(config)

    return logger


def main():
    """
    Script will check is the destination volume is mounted.
    Then connect to the Arlo API and begin downloading all new .MP4 files recorded
    within the last 30 days. 
    """

    date_start = str(strftime('%A, %d. %B %Y %I:%M%p', localtime()))

    start_msg = "\n\
    ================================================================\n\
                ARLO Download Script - Start\n\
                    {}\n\
    ================================================================\n\
    ".format(date_start)

    logger.info(start_msg) 

    try:
        mounted = os.path.ismount(MOUNT_PATH)
        if mounted is not False: 
            arlo_download.download_mp4s()
        else: 
            mount_err_msg = "Destination volume is not mounted."
            logger.error(mount_err_msg)

        date_end = str(strftime('%A, %d. %B %Y %I:%M%p', localtime()))

        complete_msg = "\n\
        ================================================================\n\
                    ARLO Download - Complete\n\
                        {}\n\
        ================================================================\n\
        ".format(date_end)
        logger.info(complete_msg)

    except Exception as e:
        logger.exception(e)


if __name__ == '__main__':
    set_logger()
    main()
