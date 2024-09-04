==============
IndiCam Client
==============


.. image:: https://img.shields.io/pypi/v/indicam_client.svg
        :target: https://pypi.python.org/pypi/indicam_client


A thin Python client wrapping the IndiCam service API. The IndiCam service extracts measurements from images of
analog meters, notably oil tank gauges, for use in home or other automation.

* Free software: MIT license

Documentation
=============
The documentation can be viewed (here)[https://docs.hausnet.io/indicam/#client]

Developer notes
===============

In order to publish a package, update the version number in `indicam_client/__init__.py`. Then:

```
flit build
flit publish
```
