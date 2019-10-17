# !/usr/bin/python3
# -*- coding: utf-8 -*-

# ALS - Astro Live Stacker
# Copyright (C) 2019  Sébastien Durand (Dragonlost) - Gilles Le Maréchal (Gehelem)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
Module holding all application logic
"""
import gettext
import logging
import os
import shutil
from datetime import datetime
from pathlib import Path

from als import config
from als.code_utilities import log
from als.io.input import InputScanner, ScannerStartError
from als.io.output import ImageSaver
from als.model import DYNAMIC_DATA, Image, SignalingQueue, Session, STACKING_MODE_MEAN
from als.processing import PreProcessPipeline, PostProcessPipeline
from als.stack import Stacker

gettext.install('als', 'locale')

_LOGGER = logging.getLogger(__name__)


class SessionError(Exception):
    """
    Class for all errors related to session management
    """
    def __init__(self, message, error):
        Exception.__init__(self)
        self.message = message
        self.error = error


class CriticalFolderMissing(SessionError):
    """Raised when a critical folder is missing"""


class Controller:
    """
    The application controller, in charge of implementing application logic
    """
    @log
    def __init__(self):

        DYNAMIC_DATA.session.set_status(Session.stopped)
        DYNAMIC_DATA.web_server_is_running = False
        DYNAMIC_DATA.stacking_mode = STACKING_MODE_MEAN

        self._input_scanner: InputScanner = InputScanner.create_scanner()

        self._pre_process_queue: SignalingQueue = DYNAMIC_DATA.pre_process_queue
        self._pre_process_pipeline: PreProcessPipeline = PreProcessPipeline(DYNAMIC_DATA.pre_process_queue)
        self._pre_process_pipeline.start()

        self._stacker_queue: SignalingQueue = DYNAMIC_DATA.stack_queue
        self._stacker: Stacker = Stacker(DYNAMIC_DATA.stack_queue)
        self._stacker.start()

        self._post_process_pipeline = PostProcessPipeline(DYNAMIC_DATA.process_queue)
        self._post_process_pipeline.start()

        self._image_saver = ImageSaver(DYNAMIC_DATA.save_queue)
        self._image_saver.start()

        self._input_scanner.new_image_signal[Image].connect(self.on_new_image_read)
        self._pre_process_pipeline.new_result_signal[Image].connect(self.on_new_pre_processed_image)
        self._stacker.stack_size_changed_signal[int].connect(DYNAMIC_DATA.set_stack_size)
        self._stacker.new_stack_result_signal[Image].connect(self.on_new_stack_result)
        self._post_process_pipeline.new_processing_result_signal[Image].connect(self.on_new_process_result)

        DYNAMIC_DATA.pre_process_queue.size_changed_signal[int].connect(self.on_pre_process_queue_size_changed)
        DYNAMIC_DATA.stack_queue.size_changed_signal[int].connect(self.on_stack_queue_size_changed)
        DYNAMIC_DATA.process_queue.size_changed_signal[int].connect(self.on_process_queue_size_changed)
        DYNAMIC_DATA.save_queue.size_changed_signal[int].connect(self.on_save_queue_size_changed)

    @log
    def on_new_process_result(self, image: Image):
        """
        A new image processing result is here

        :param image: the new processing result
        :type image: Image
        """
        DYNAMIC_DATA.process_result = image
        self.save_process_result()

    @log
    def on_new_stack_result(self, image: Image):
        """
        A new image has been stacked

        :param image: the result of the stack
        :type image: Image
        """
        DYNAMIC_DATA.process_queue.put(image)

    @log
    def on_new_image_read(self, image: Image):
        """
        A new image as been read by input scanner

        :param image: the new image
        :type image: Image
        """
        self._pre_process_queue.put(image)

    @log
    def on_new_pre_processed_image(self, image: Image):
        """
        A new image as been pre-processed

        :param image: the image
        :type image: Image
        """
        self._stacker_queue.put(image)

    @log
    def on_pre_process_queue_size_changed(self, new_size):
        """
        Qt slot executed when an item has just been pushed to the pre-process queue

        :param new_size: new queue size
        :type new_size: int
        """
        _LOGGER.debug(f"New image added to the pre-process queue. Pre-process queue size : {new_size}")
        DYNAMIC_DATA.pre_process_queue_size = new_size

    @log
    def on_pre_process_queue_popped(self, new_size):
        """
        Qt slot executed when an item has just been popped from the pre-process queue

        :param new_size: new queue size
        :type new_size: int
        """
        _LOGGER.debug(f"Image taken from input queue. Input queue size : {new_size}")
        DYNAMIC_DATA.pre_process_queue_size = new_size

    @log
    def on_stack_queue_size_changed(self, new_size):
        """
        Qt slot executed when an item has just been pushed to the stack queue

        :param new_size: new queue size
        :type new_size: int
        """
        _LOGGER.debug(f"New image added to the stack queue. Stack queue size : {new_size}")
        DYNAMIC_DATA.stack_queue_size = new_size

    @log
    def on_stack_queue_popped(self, new_size):
        """
        Qt slot executed when an item has just been popped from the stack queue

        :param new_size: new queue size
        :type new_size: int
        """
        _LOGGER.debug(f"Image taken from stack queue. Stack queue size : {new_size}")
        DYNAMIC_DATA.stack_queue_size = new_size

    @log
    def on_process_queue_size_changed(self, new_size):
        """
        Qt slot executed when an item has just been pushed to the process queue

        :param new_size: new queue size
        :type new_size: int
        """
        _LOGGER.debug(f"New image added to the process queue. Process queue size : {new_size}")
        DYNAMIC_DATA.process_queue_size = new_size

    @log
    def on_process_queue_popped(self, new_size):
        """
        Qt slot executed when an item has just been popped from the process queue

        :param new_size: new queue size
        :type new_size: int
        """
        _LOGGER.debug(f"Image taken from process queue. Process queue size : {new_size}")
        DYNAMIC_DATA.process_queue_size = new_size

    @log
    def on_save_queue_size_changed(self, new_size):
        """
        Qt slot executed when an item has just been pushed to the save queue

        :param new_size: new queue size
        :type new_size: int
        """
        _LOGGER.debug(f"New image added to the save queue. Save queue size : {new_size}")
        DYNAMIC_DATA.save_queue_size = new_size

    @log
    def on_save_queue_popped(self, new_size):
        """
        Qt slot executed when an item has just been popped from the save queue

        :param new_size: new queue size
        :type new_size: int
        """
        _LOGGER.debug(f"Image taken from save queue. Save queue size : {new_size}")
        DYNAMIC_DATA.save_queue_size = new_size

    @log
    def start_session(self):
        """
        Starts session
        """
        try:
            if DYNAMIC_DATA.session.is_stopped():

                _LOGGER.info("Starting new session...")

                self._stacker.reset()

                folders_dict = {
                    "scan": config.get_scan_folder_path(),
                    "work": config.get_work_folder_path()
                }

                # checking presence of both scan & work folders
                #
                # for each of those, if folder is missing, ask user if she wants to access the preferences box
                # if user refuses, we simply fail the session startup
                for role, path in folders_dict.items():
                    if not Path(path).is_dir():
                        title = "Missing critical folder"
                        message = f"Your currently configured {role} folder '{path}' is missing."
                        raise CriticalFolderMissing(title, message)

                # setup work folder
                try:
                    self.setup_work_folder()
                except OSError as os_error:
                    raise SessionError("Work folder could not be prepared", os_error)

            else:
                # session was paused when this start was ordered. No need for checks & setup
                _LOGGER.info("Restarting input scanner ...")

            # start input scanner
            try:
                self._input_scanner.start()
                _LOGGER.info("Input scanner started")
            except ScannerStartError as scanner_start_error:
                raise SessionError("Input scanner could not start", scanner_start_error)

            running_mode = f"{DYNAMIC_DATA.stacking_mode}"
            running_mode += " with alignment" if DYNAMIC_DATA.align_before_stacking else " without alignment"
            _LOGGER.info(f"Session running in mode {running_mode}")
            DYNAMIC_DATA.session.set_status(Session.running)

        except SessionError as session_error:
            _LOGGER.error(f"Session error. {session_error.message} : {session_error.error}")
            raise

    @log
    def stop_session(self):
        """
        Stops session : stop input scanner and purge input queue
        """
        if not DYNAMIC_DATA.session.is_stopped():
            self._stop_input_scanner()
            self.purge_pre_process_queue()
            _LOGGER.info("Session stopped")
            DYNAMIC_DATA.session.set_status(Session.stopped)

    @log
    def pause_session(self):
        """
        Pauses session : just stop input scanner
        """
        if DYNAMIC_DATA.session.is_running():
            self._stop_input_scanner()
        _LOGGER.info("Session paused")
        DYNAMIC_DATA.session.set_status(Session.paused)

    @log
    def purge_pre_process_queue(self):
        """
        Purge the pre-process queue

        """
        while not DYNAMIC_DATA.pre_process_queue.empty():
            DYNAMIC_DATA.pre_process_queue.get()
        _LOGGER.info("Pre-process queue purged")

    @log
    def purge_stack_queue(self):
        """
        Purge the stack queue

        """
        while not DYNAMIC_DATA.stack_queue.empty():
            DYNAMIC_DATA.stack_queue.get()
        _LOGGER.info("Stack queue purged")

    @log
    def setup_work_folder(self):
        """Prepares the work folder."""

        work_dir_path = config.get_work_folder_path()
        resources_dir_path = os.path.dirname(os.path.realpath(__file__)) + "/../resources"

        shutil.copy(resources_dir_path + "/index.html", work_dir_path)

        standby_image_path = work_dir_path + "/" + config.WEB_SERVED_IMAGE_FILE_NAME_BASE + '.' + config.IMAGE_SAVE_JPEG
        shutil.copy(resources_dir_path + "/waiting.jpg", standby_image_path)

    @log
    def save_process_result(self):
        """
        Saves stacking result image to disk
        """

        # we save the image no matter what, then save a jpg for the web server if it is running
        image = DYNAMIC_DATA.process_result

        self.save_image(image,
                        config.get_image_save_format(),
                        config.get_work_folder_path(),
                        config.STACKED_IMAGE_FILE_NAME_BASE)

        if DYNAMIC_DATA.web_server_is_running:
            self.save_image(image,
                            config.IMAGE_SAVE_JPEG,
                            config.get_work_folder_path(),
                            config.WEB_SERVED_IMAGE_FILE_NAME_BASE)

        if DYNAMIC_DATA.save_every_image:
            self.save_image(image,
                            config.get_image_save_format(),
                            config.get_work_folder_path(),
                            config.STACKED_IMAGE_FILE_NAME_BASE,
                            add_timestamp=True)

    @log
    def save_image(self, image: Image,
                   file_extension: str,
                   dest_folder_path: str,
                   filename_base: str,
                   add_timestamp: bool = False):
        """
        Save an image to disk.

        :param image: the image to save
        :type image: Image
        :param file_extension: The image save file format extension
        :type file_extension: str
        :param dest_folder_path: The path of the folder image will be saved to
        :type dest_folder_path: str
        :param filename_base: The name of the file to save to (without extension)
        :type filename_base: str
        :param add_timestamp: Do we add a timestamp to image name
        :type add_timestamp: bool
        """
        filename_base = filename_base

        if add_timestamp:
            filename_base += '-' + Controller.get_timestamp()

        image_to_save = image.clone()
        image_to_save.destination = dest_folder_path + "/" + filename_base + '.' + file_extension
        DYNAMIC_DATA.save_queue.put(image_to_save)

    @log
    def shutdown(self):
        """
        Proper shutdown of all app components
        """
        if not DYNAMIC_DATA.session.is_stopped():
            self.stop_session()

        self._pre_process_pipeline.stop()
        self._stacker.stop()
        self._post_process_pipeline.stop()
        self._image_saver.stop()
        self._image_saver.wait()

    @staticmethod
    @log
    def get_timestamp():
        """
        Return a timestamp build from current date and time

        :return: the timestamp
        :rtype: str
        """
        timestamp = str(datetime.fromtimestamp(datetime.timestamp(datetime.now())))
        timestamp = timestamp.replace(' ', "-").replace(":", '-').replace('.', '-')
        return timestamp

    @log
    def _stop_input_scanner(self):
        self._input_scanner.stop()
        _LOGGER.info("Input scanner stopped")