#!/bin/bash
cybergis-script-stretch.py original.img bps_1.txt imagery_1.img 64
cybergis-script-stretch.py imagery_1.img bps_2.txt imagery_2.img 64
gdalwarp -r bilinear -of HFA imagery_2.img imagery_3.img
