#!/usr/bin/env python3

import os
import time
import argparse
import tempfile
import zipfile
import shutil
from os import path
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler


def on_modified(event):
    if(args.verbose):
        if ".part" in event.src_path:
            pass
        print(f"{event.src_path} has been modified.")


def on_deleted(event):
    if(args.verbose):
        print(f"{event.src_path} has been deleted.")


def on_created(event):
    # Ignore .part files while downloading
    # As well as files with no dot -> Directory
    if ".part" in event.src_path or "." not in event.src_path:
        pass
    else:
        # Get the filename: path/to/dir/filename.pdf
        filename = event.src_path.split("/")[-1]
        if(args.verbose):
            print(f"{event.src_path} has been created.")
        # Works as well with zips
        if zipfile.is_zipfile(event.src_path):
            if(args.verbose):
                print("Archive detected.\nExtracting...")
                # Make a temporary directory to extract to
                dir_path = tempfile.mkdtemp()
                # Extract
                with zipfile.ZipFile(event.src_path, "r") as zip_ref:
                    zip_ref.extractall(dir_path)
                # Move the files
                shutil.move(dir_path, args.src_path)
                # Get path of the temp directory
                dir_path = dir_path.split("/")[-1]
                # make it accessable
                os.chmod(args.src_path + "/" + str(dir_path), 0o777)
                if(args.verbose):
                    print("Done.")
        # Move the files
        os.rename(event.src_path, args.dest_path + "/" + filename)


def on_moved(event):
    if(args.verbose):
        print(f"{event.src_path} moved to {event.dest_path}.")


if __name__ == "__main__":
    # God bless argparse
    parser = argparse.ArgumentParser(description='Automatic file mover' +
                                     '/zip archive extractor.',
                                     epilog='Made by Julian Hohenadel 2019')
    parser.add_argument('src_path', help='The src_path of the '
                        + 'dir_path you want to track')
    parser.add_argument('dest_path', help='The dest_path to move the file to.')
    parser.add_argument("-v", "--verbose", help="increase output verbosity",
                        action="store_true")
    args = parser.parse_args()
    # Check for valid paths
    if(not path.exists(args.src_path)):
        print("src_path needs to exist!\nExiting.")
        exit()
    if(not path.exists(args.dest_path)):
        print("dest_path needs to exist!\nExiting.")
        exit()

    if args.verbose:
        print("Verbose: " + str(args.verbose))
        print("src_path:\n" + args.src_path)
        print("dest_path:\n" + args.dest_path)

    # set up the event handler
    patterns = "*"
    my_event_handler = PatternMatchingEventHandler(patterns)

    # the other events were not needed but could be useful for other tasks
    # in the future
    my_event_handler.on_created = on_created
    # my_event_handler.on_deleted = on_deleted
    # my_event_handler.on_modified = on_modified
    # my_event_handler.on_moved = on_moved

    # Set up the observer
    my_observer = Observer()
    my_observer.schedule(my_event_handler, args.src_path, recursive=True)

    my_observer.start()
    if args.verbose:
        print("Observer initialization done.\nNow looking at: " + args.src_path)
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        my_observer.stop()
        my_observer.join()
        # Cleanup afterwards: Delete tmp directorys of zips recursivly
        for dir in os.listdir(args.src_path):
            if "tmp" in dir:
                if args.verbose:
                    print("Deleting temporary folder: " + args.src_path +
                          "/" + dir)
                shutil.rmtree(args.src_path + "/" + dir)
