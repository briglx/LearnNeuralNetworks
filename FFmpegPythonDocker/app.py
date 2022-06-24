#!/usr/bin/env python3
import subprocess
import sys
import os
import pathlib
import glob
from azure.storage.blob import BlockBlobService
from requests.exceptions import ReadTimeout
from azure.common import AzureMissingResourceHttpError, AzureException


HOME = '.'
VIDEO_PATH = os.path.join(HOME, "pipeline", "1_videos")
FRAME_PATH = os.path.join(HOME, "pipeline", "2_frames")

ACCOUNT_NAME = os.environ.get("RAW_VIDEO_STORAGE_ACCOUNT_NAME") 
ACCOUNT_KEY =  os.environ.get("RAW_VIDEO_STORAGE_ACCOUNT_KEY")
CONTAINER_VIDEOS = 'pipeline-1-video'
CONTAINER_FRAMES = 'pipeline-2-frames'

FFMPEG_BINARY = '/usr/local/bin/ffmpeg'

ERR_MSG = "'{} Count' doesn't match '{} Count'. Check if all files were {}."
ERR_COUNT_MSG = ERR_MSG.format("Frame", "Saved File", "saved")
ERR_REMOVE_MSG = ERR_MSG.format("Save File", "Removed", "removed")


def split_frames_from_video(src, dest):
    print("Getting frames from ", src)

    videoName = os.path.split(src)[1]
    pathlib.Path(dest).mkdir(parents=True, exist_ok=True)

    command = [FFMPEG_BINARY,
               '-i', src,
               '-r', '1/1',
               dest + '/' + videoName + '.frame-%03d.png']
    proc = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        bufsize=10**8
        )
    proc.stderr.read()

    file_count = len(glob.glob1(dest, videoName + "*.png"))
    print("Split {} frames from {}".format(file_count, videoName))
    return file_count


def split_frames_from_video_job(src, dest):
    frame_count = 0

    for filename in glob.iglob(os.path.join(src, '**/*.mp4'), recursive=True):

        frame_count += split_frames_from_video(filename, dest)

    print("Split {} frames from {}".format(frame_count, src))
    return frame_count


def save_frames_to_blob(src, container_name):
    print("Saving blobs to ", container_name)

    file_count = 0
    blob_service = BlockBlobService(ACCOUNT_NAME, ACCOUNT_KEY)
    blob_service.create_container(container_name)

    src_path = os.path.join(src, '**/*.png')
    for full_path_to_file in glob.iglob(src_path, recursive=True):

        file_name = os.path.split(full_path_to_file)[1]
        blob_service.create_blob_from_path(
            container_name, file_name,
            full_path_to_file
            )
        file_count += 1

    print("Saved {} frames to {}".format(file_count, container_name))
    return file_count


def remove_local_files(src):
    print("Removing local files from ", src)
    file_count = 0
    src_path = os.path.join(src, '**/*.png')
    for full_path_to_file in glob.iglob(src_path, recursive=True):
        os.remove(full_path_to_file)
        file_count += 1

    print("Removed {} frames from {}".format(file_count, src_path))
    return file_count


def main():
    """Run the script."""
    print("Starting...")
    # Create Local folders
    pathlib.Path(VIDEO_PATH).mkdir(parents=True, exist_ok=True)
    pathlib.Path(FRAME_PATH).mkdir(parents=True, exist_ok=True)

    try:
        blob_service = BlockBlobService(ACCOUNT_NAME, ACCOUNT_KEY)
        blobs = blob_service.list_blobs(CONTAINER_VIDEOS)

        for blob in blobs:

            print("Getting file ", blob)
            dest_filename = os.path.join(VIDEO_PATH, blob.name)
            blob_service.get_blob_to_path(
                CONTAINER_VIDEOS,
                blob.name,
                dest_filename
                )

            frame_count = split_frames_from_video_job(
                VIDEO_PATH, FRAME_PATH)

            saved_file_count = save_frames_to_blob(
                FRAME_PATH, CONTAINER_FRAMES)

            assert frame_count == saved_file_count, ERR_COUNT_MSG

            removed_frame_count = remove_local_files(FRAME_PATH)

            assert saved_file_count == removed_frame_count, ERR_REMOVE_MSG

            print("Remove local file ", dest_filename)
            os.remove(dest_filename)

            print("Remove remote file ", CONTAINER_VIDEOS, blob.name)
            blob_service.delete_blob(CONTAINER_VIDEOS, blob.name)

    except AzureMissingResourceHttpError:
        print("Skipping file ", blob)
    except ReadTimeout:
        print(('Fatal Error: Unable to create process blob '
               'in container {} ').format(CONTAINER_VIDEOS))
        sys.exit(1)
    except AzureException as ex:
        print(('Fatal Error: Unable to create process blob '
               'in container {}, {} ').format(CONTAINER_VIDEOS, ex))
        sys.exit(1)

    print("Finished")
    return 0


if __name__ == '__main__':
    sys.exit(main())
