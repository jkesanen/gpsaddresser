from abc import ABCMeta, abstractmethod

from gpsaddresser.location import Location


class TrackInterface:
    __metaclass__ = ABCMeta

    def __init__(self, filename: str):
        self.filename = filename

    @abstractmethod
    def start_location(self) -> Location:
        raise NotImplementedError("This is an abc class.")

    @abstractmethod
    def end_location(self) -> Location:
        raise NotImplementedError("This is an abc class.")

    @abstractmethod
    def next_location(self) -> Location:
        raise NotImplementedError("This is an abc class.")

    @abstractmethod
    def location_on_track(self, location: Location, distance: int) -> bool:
        raise NotImplementedError("This is an abc class.")
