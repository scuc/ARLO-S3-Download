from datetime import timedelta, date, datetime
import logging
from pathlib import Path

import config

config = config.get_config()

USERNAME = config['creds']['username']
PASSWORD = config['creds']['password']

logger = logging.getLogger(__name__)

ROOTPATH = config['paths']['root_path']

def check_subdirs(root_dir, deviceName, videofilename):
# def check_subdirs(dir_path, mp4, mp4_output_path, mp4_path): 
    """
    Check the subdir for existing year-month dirs, if they dont already
    exist, mkdir. 
    """
    try:
        # chk_subdir_msg = f"Checking sub-directories for {mp4_output_path}"
        mp4 = videofilename

        # chk_subdir_msg = "Checking sub-directories for {}".format(deviceName)
        # logger.info(chk_subdir_msg)

        year = mp4[:4]
        month = mp4[5:7]
        year_path = Path(root_dir, str(year))
        month_path = Path(year_path, str(month))
        file_path = Path(month_path, mp4)

        chk_path_msg = "Checking file path for MP4: ".format(file_path)
        logger.info(chk_path_msg)

        if not year_path.exists():
            year_path.mkdir()
            # year_msg = f"Creating new directory {year_path}"
            year_msg = "Creating new directory {}".format(year_path)
            logger.info(year_msg)
        # else: 
        #     # year_msg = f"Directory already exists for:  {year_path}"
        #     year_msg = "Directory already exists for: {}".format(year_path)

        if not month_path.exists(): 
            month_path.mkdir() 
            # month_msg = f"Creating new directory {month_path}"
            month_msg = "Creating new directory {}".format(month_path)
            logger.info(month_msg)
        # else:
        #     # month_msg = f"Directory already exists for: {month_path}"
        #     month_msg = "Directory already exists for: {}".format(month_path)


        if not file_path.exists(): 
            # file_msg = f"Confirmed - {mp4} does not exist in: {month_path}"
            file_msg = "Confirmed: {} does not exist in: {}".format(mp4, month_path)
        else:
            # file_msg = f"\n\
            #             {mp4} already exists in: {month_path}\n\
            #             Appending file name before move."
            file_msg = "\n\
                        {} already exists in: {}".format(mp4,month_path)

    except Exception as e:
        logger.exception(e)

    # logger.info(year_msg)
    # logger.info(month_msg)
    logger.info(file_msg)

    return file_path