# gpsaddresser

A Python module/tool for querying and sorting GPS track files according to addresses.

Batch sorts GPS track files which start in, end in, or go via an address within the distance.

No need to upload private track with location information to a 3rd party services. Only the given address is queried online and converted to location coordinates with geopy library.

## Requirements

* [geopy](https://github.com/geopy/geopy/)
* FIT file support: [python-fitparse](https://github.com/dtcooper/python-fitparse)

## Example

Copies files (from year 2019) into `tokyo` directory which start within 30000 meters of address `Tokyo, Japan`:

```
$ venv/Scripts/python -m gpsaddresser --start-address "Tokyo, Japan" --distance 30000 --copy tokyo Moves/Move_2019_*_Running.fit
Got location coordinates (35.6828387, 139.7594549) for --start-address: Tokyo, Japan
Copying matching files to tokyo
Copying Moves/Move_2019_11_14_12_26_15_Running.fit to tokyo
Copying Moves/Move_2019_11_15_16_12_58_Running.fit to tokyo
Copying Moves/Move_2019_11_17_21_25_07_Running.fit to tokyo
Copying Moves/Move_2019_11_19_16_17_30_Running.fit to tokyo
Copying Moves/Move_2019_11_20_12_02_54_Running.fit to tokyo
Copying Moves/Move_2019_11_22_11_42_34_Running.fit to tokyo
```
