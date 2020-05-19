#!/usr/bin/env python
# -*- coding: utf-8 -*

import argparse
import logging
import os
import shutil
import sys

from gpsaddresser.track import Track
from gpsaddresser.location import *

__license__ = "MIT"
__version__ = "0.1"

__all__ = ["GpsAddresser"]

class GpsAddresser():

    def is_file_within_distance(self,
                                filename,
                                start_location=None,
                                end_location=None,
                                max_distance=None,
                                via_location=None,
                                max_via_distance=None):
        logger = logging.getLogger('gpsaddresser')

        try:
            track = Track(filename)
        except Track.NotSupportedFormat as e:
            logger.warning("File {0} is not supported: {1}".format(filename, e))
            return

        match = False

        if start_location:
            # The file starts within the maximum distance of the given start location?
            file_start = track.start_location()
            if not file_start:
                logger.warning("No start location in: {0}".format(filename))
                return False
            match = location_distance_meters(start_location, file_start) <= max_distance

        if end_location:
            # The file ends within the maximum distance of the given end location?
            file_end = track.end_location()
            if not file_end:
                logger.warning("No end location in: {0}".format(filename))
                return False

            match = location_distance_meters(end_location, file_end) <= max_distance

        if via_location:
            # The file's track goes past the given location within the maximum distance?
            match = track.location_on_track(via_location, max_via_distance)

        return match
