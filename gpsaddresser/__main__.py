import argparse
import logging
import os
import shutil
import sys

import multiprocessing

from gpsaddresser import GpsAddresser
from gpsaddresser import location


class destination_directory(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        path = values
        if not os.path.isdir(path):
            os.mkdir(path)
        if os.access(path, os.W_OK):
            setattr(namespace, self.dest, path)
        else:
            raise argparse.ArgumentTypeError("destination_directory:{0} is not a writable dir".format(path))


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description="GPS Track Addresser")

    address_group = ap.add_argument_group('address')
    address_group.add_argument('-s', '--start-address', type=str, help='Starting street address')
    address_group.add_argument('-e', '--end-address', type=str, help='Ending street address')
    address_group.add_argument('-E', action="store_true", help='Ending address is the same as --start-address')
    address_group.add_argument('--via-address', type=str, help='Track goes via this street address')

    distance_group = ap.add_argument_group('distance')
    distance_group.add_argument('-d', '--distance', type=float, default=200.0,
                    help='Distance in meters to --start-address and --end-address')
    distance_group.add_argument('-V', '--via-distance', type=float, default=200.0, help='Distance in meters to --via-address')

    action_group = ap.add_argument_group('action')
    action_group.add_argument('-c', '--copy', action=destination_directory)
    action_group.add_argument('-m', '--move', action=destination_directory)

    ap.add_argument('files', type=str, nargs='+')

    # Parse the given arguments and output an error and exit, if invalid arguments were given.
    args = ap.parse_args()

    # Set up logger for outputting.
    logger = logging.getLogger('gpsaddresser')
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    logger.addHandler(ch)

    if not args.start_address and not args.end_address and not args.via_address:
        logger.error("--start-address, --end-address, or --via-address must be given.")
        sys.exit(2)

    if args.start_address and args.end_address and args.E:
        logger.error("Can't set -E if --start-address and --end-address are be given.")
        sys.exit(2)

    if args.copy and args.move:
        logger.error("Can't specify --copy and --move destinations at once.")
        sys.exit(2)

    start_location = None
    end_location = None
    via_location = None

    search_error = False

    g = GpsAddresser()

    if args.start_address:
        start_location = location.address_to_location(args.start_address)
        if not start_location:
            logger.error("Searching location coordinates for --start-address \"{}\" failed.".format(args.start_address))
            search_error = True
        else:
            logger.debug("Got location coordinates %s for --start-address: %s" % (
                start_location.get_coordinates(), args.start_address))
        if args.E:
            end_location = start_location

    if args.end_address:
        end_location = location.address_to_location(args.end_address)
        if not end_location:
            logger.error("Searching location coordinates for --end-address \"%s\" failed." % args.end_address)
            search_error = True
        else:
            logger.debug("Got location coordinates %s for --end-address: %s" % (
                end_location.get_coordinates(), args.end_address))

    if args.via_address:
        via_location = location.address_to_location(args.via_address)
        if not via_location:
            logger.error("Searching location coordinates for --via-address \"%s\" failed." % args.via_address)
            search_error = True
        else:
            logger.debug("Got location coordinates %s for --via-address: %s" % (
                via_location.get_coordinates(), args.via_address))

    if not start_location and not end_location and not via_location:
        logger.error("No location to analyze with.")
        sys.exit(3)

    if search_error:
        logger.error("A query to convert an address to location coordinates failed.")
        sys.exit(3)

    multiprocessing.set_start_method('spawn')
    manager = multiprocessing.Manager()
    matches = manager.list()
    with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
        from gpsaddresser.worker import worker
        [pool.apply_async(worker, (g, matches, file, start_location, end_location, args.distance, via_location, args.via_distance)) for file in args.files]
        pool.close()
        pool.join()

    if not matches:
        logger.warning("No matches")
        sys.exit(1)

    [print("Matches: {0}".format(file)) for file in matches]

    if args.copy:
        logger.debug("Copying matching files to {0}".format(args.copy))
        for f in matches:
            logger.info("Copying {0} to {1}".format(f, args.copy))
            shutil.copy2(f, args.copy)

    if args.move:
        logger.debug("Moving matching files to {0}".format(args.copy))
        for f in matches:
            logger.info("Moving {0} to {1}".format(f, args.copy))
            shutil.move(f, args.copy)

