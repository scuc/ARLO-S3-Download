from arlo import Arlo
from datetime import timedelta, date, datetime
import logging
# from pathlib import Path

import config
import check_subdirs as chksub

config = config.get_config()

USERNAME = config['creds']['username']
PASSWORD = config['creds']['password']

logger = logging.getLogger(__name__)

ROOTPATH = config['paths']['root_path']

def download_mp4s(): 
    """
    Iterate over the videos in the arlo S3 bucket, compare against videos stored locally, dowload 
    all new files, rename downloaded files with a datetime, skip those that have already been downloaded. 
    """
    # Instantiating the Arlo object automatically calls Login(), which returns an oAuth token that gets cached.
    # Subsequent successful calls to login will update the oAuth token.
    try: 
        arlo = Arlo(USERNAME, PASSWORD)
        logger.info("Sucessfully logged into Arlo account")

        today = (date.today()-timedelta(days=0)).strftime("%Y%m%d")
        start_date = (date.today()-timedelta(days=30)).strftime("%Y%m%d")

        # Get all of the recordings for a date range.
        library = arlo.GetLibrary(start_date, today)
        print("GOT LIBRARY")
        devices = arlo.GetDevices()
        print("GOT DEVICES")

        device_list = []

        for device in devices:
            deviceId = device["deviceId"]
            deviceName = device["deviceName"]
            device_dict = {device["deviceId"]: device["deviceName"]}
            device_list.append(device_dict)

        # Iterate through the recordings in the library.
        for recording in library:

            deviceId = recording["deviceId"]

            deviceNum = next(i for i,d in enumerate(device_list) if deviceId in d)

            deviceName = device_list[deviceNum][deviceId]

            videofilename = datetime.fromtimestamp(int(recording['name'])//1000).strftime('%Y-%m-%d_%H-%M-%S') + '_' + recording['uniqueId'] + '.mp4'

            ###################
            # The videos produced by Arlo are pretty small, even in their longest, best quality settings,
            # but you should probably prefer the chunked stream (see below).
            ##################
            #    # Download the whole video into memory as a single chunk.
            #    video = arlo.GetRecording(recording['presignedContentUrl'])
            #	 with open('videos/'+videofilename, 'wb') as f:
            #        f.write(video)
            #        f.close()
            ################33

            root_dir = (ROOTPATH + deviceName + '/')
            mp4_path = chksub.check_subdirs(root_dir, deviceName, videofilename)

            if mp4_path.is_file() is not True:
                stream = arlo.StreamRecording(recording['presignedContentUrl'])
                with open(str(mp4_path), 'wb') as f:
                    for chunk in stream: 
                        f.write(chunk)
                    f.close()
                    download_msg = 'Downloaded '+ videofilename+' from '+ recording['createdDate']+'.'
                    dowload_path_msg = "Download path: " + str(mp4_path)
                    logger.info(download_msg)
                    logger.info(dowload_path_msg)
            else:
                # Get video as a chunked stream; this function returns a generator.
                skip_msg = "Skipping: " + str(videofilename)
                logger.info(skip_msg)
                continue

        # Delete all of the videos you just downloaded from the Arlo library.
        # Notice that you can pass the "library" object we got back from the GetLibrary() call.
        # result = arlo.BatchDeleteRecordings(library)

        # If we made it here without an exception, then the videos were successfully deleted.
        # print('Batch deletion of videos completed successfully.')
        print("Completed.")
        return

    except Exception as e:
        logger.exception(e)
        


if __name__ == '__main__':
    download_mp4s()