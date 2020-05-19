from gpsaddresser.location import Location

class Track:
    class NotSupportedFormat(Exception):
        """Raised when non-supported file format is given."""
        pass

    def __init__(self, filename: str):
        self.filename = filename
        self.track = None

        if filename.lower().endswith('.fit'):
            from gpsaddresser.trackfit import TrackFit

            self.track = TrackFit(filename)
        else:
            raise self.NotSupportedFormat("The given file format is not supported: {0}".format(filename))

    def start_location(self):
        """Returns the location coordinates of the first record with coordinates in a FIT file."""
        return self.track.start_location()

    def end_location(self):
        """Returns the location coordinates of the last record with coordinates in a FIT file."""
        return self.track.end_location()

    def location_on_track(self, location: Location, max_distance: float) -> bool:
        for loc in self.track.next_location():
            d = location_distance_meters(location, loc)
            print(d)
            if d <= max_distance:
                return True

        return False
