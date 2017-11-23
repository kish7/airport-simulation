# SFO Data

## Source

- [overpass-turbo](http://overpass-turbo.eu/s/rFN)
- [Node-link Language](http://wiki.openstreetmap.org/wiki/Aeroways)
- Spot position are manually added on [Google Map](https://drive.google.com/open?id=1votbJbKKRUF5gDumno4GXOxVLAE&usp=sharing) (request for edit)

## Note

- `surface.json` is downloaded json data from [overpass-turbo](http://overpass-turbo.eu/s/rFN) (click on export and download GeoJSON file)

## Try

`play_ground.py` is for testing out different elements in the loaded from the
raw data. Install IPython for interactive supports.

    $ ipython play_ground.py

## Generate files for simulator

    $ python3 generate.py

## Reference

- https://github.com/whit537/gheat/blob/master/__/lib/python/gmerc.py
