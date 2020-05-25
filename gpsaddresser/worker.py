# The worker function is in a separate file instead of __main__.py to overcome:
#   AttributeError: Can't get attribute 'worker' on <module '__main__' (built-in)>

def worker(gps, matches, inputfile, start_location, end_location, distance, via_location, via_distance):
    if (gps.is_file_within_distance(inputfile,
                                    start_location,
                                    end_location,
                                    distance,
                                    via_location,
                                    via_distance)):
        matches.append(inputfile)
