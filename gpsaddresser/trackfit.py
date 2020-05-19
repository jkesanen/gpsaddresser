from fitparse import FitFile
from fitparse import StandardUnitsDataProcessor

from gpsaddresser.trackinterface import TrackInterface
from gpsaddresser.location import Location


class TrackFit(TrackInterface):

    def __init__(self, filename):
        super()
        self.fitfile = FitFile(filename, data_processor=StandardUnitsDataProcessor())
        self.fitfile.parse()

    def start_location(self):
        """Searches for the first record with latitude and longitude coordinates.

        Returns:
            A Location object. None if latitude and longitude not found.
        """
        for record in self.fitfile.messages:
            if not record.name == 'record':
                continue

            location = record_location(record)

            if location:
                return location

        return None

    def end_location(self):
        """Searches for the last record with latitude and longitude coordinates.

        Returns:
            A Location object. None if latitude and longitude not found.
        """
        for record in reversed(self.fitfile.messages):
            if not record.name == 'record':
                continue

            location = record_location(record)

            if location:
                return location

        return None

    def next_location(self):
        for record in self.fitfile.messages:
            if not record.name == 'record':
                continue

            location = record_location(record)

            if location:
                print(location)
                yield location

        return None


def record_location(record):
    """Parses FIT record data for latitude, longitude and altitude

    Args:
        record: A record from fitparse.

    Returns:
        A Location object. None if latitude and longitude not found.
    """
    latitude = 0.0
    longitude = 0.0
    altitude = 0

    for record_data in record:
        if record_data.name == "position_lat":
            latitude = record_data.value
        if record_data.name == "position_long":
            longitude = record_data.value
        if record_data.name == "altitude":
            altitude = record_data.value

    if latitude and longitude:
        return Location(latitude, longitude, altitude)

    return None
