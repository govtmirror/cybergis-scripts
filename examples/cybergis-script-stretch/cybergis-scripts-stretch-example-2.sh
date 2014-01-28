#!/bin/bash
cybergis-script-stretch.py original.img style.qml imagery_1.img 64
gdalwarp -r bilinear -of HFA imagery_1.img imagery_2.img
