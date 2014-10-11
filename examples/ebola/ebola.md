Ebola, Version 1.0
================

| Examples: | [Ebola](https://github.com/state-hiu/cybergis-scripts/blob/master/examples/ebola/) |
| ---- |  ---- | ---- | ---- |

## Description

This example demonstrates how to execute OpenStreetmap extractions.

### Cheat Sheet
TBD

### CyberGIS
The Humanitarian Information Unit has been developing a sophisticated geographic computing infrastructure referred to as the CyberGIS. The CyberGIS provides highly available, scalable, reliable, and timely geospatial services capable of supporting multiple concurrent projects.  The CyberGIS relies on primarily open source projects, such as PostGIS, GeoServer, GDAL, GeoGit, OGR, and OpenLayers.  The name CyberGIS is dervied from the term geospatial cyberinfrastructure.

### Bugs

If you find any bugs in the OpenGeo Suite, please submit them as issues to the respective component's GitHub repository or to the OpenGeo Suite GitHub repository at [https://github.com/boundlessgeo/suite](https://github.com/boundlessgeo/suite).  If you find any bugs with the guide itself, please submit them to this repo at [https://github.com/state-hiu/cybergis-guides/issues](https://github.com/state-hiu/cybergis-guides/issues).

## Provision

Before you begin the installation process, you'll need to provision a virtual or physical machine.  If you are provisioning an instance using Amazon Web Services, we recommend you use the baseline Ubuntu 12.04 LTS AMI managed by Ubuntu/Canonical.  You can lookup the most recent ami code on this page: [https://cloud-images.ubuntu.com/releases/precise/release/](https://cloud-images.ubuntu.com/releases/precise/release/).  Generally speaking, you should use the 64-bit EBS-SSD AMI for the OpenGeo Suite.

## Installation

Launching an OpenGeo Suite instance only requires a few simple steps.  The installation process is relatively painless on a clean build and can be completed in less than 30 minutes, usually 15 minutes.

These instructions were written for deployment on the Ubuntu operating system, but may work on other Linux variants.  The OpenGeo Suite will not install on Ubuntu 14.04 yet as a few dependencies have not been upgraded yet.  We recommend using Ubuntu 12.04.

You'll want to complete all the below steps as the root (with login shell and enviornment).  Therefore, use `sudo su -` to become the root user.  Do not use `sudo su root`, as that may not provide the environment necessary.

You can **rerun** most steps, but not all, if a network connection drops.

Installation only requires 5 simple steps.  Most steps only require executing one command on the command line.

1. Install CyberGIS scripts.  [[Jump]](#step-1)
2. Install CyberGIS OSM mappings. [[Jump]](#step-2)
3. Install CyberGIS styles [[Jump]](#step-3)

###Kown Issues

No known issues

###Step 1

The first step is install the CyberGIS scripts from the [cybergis-scripts](https://github.com/state-hiu/cybergis-scripts) repo.  As root (`sudo su -`) execute the following commands.

```
apt-get update
apt-get install -y curl vim git
cd /opt
git clone https://github.com/state-hiu/cybergis-scripts.git cybergis-scripts.git
cp cybergis-scripts.git/profile/cybergis-scripts.sh /etc/profile.d/
```

###Step 2

The second step is install the CyberGIS OpenStreetMap Mappings from the [cybergis-osm-mappings](https://github.com/state-hiu/cybergis-osm-mappings) repo.  As root (`sudo su -`) execute the following commands.

```
cd /opt
git clone https://github.com/state-hiu/cybergis-osm-mappings.git cybergis-osm-mappings.git
```

###Step 3

The third step is install the CyberGIS Styles from the [cybergis-styles](https://github.com/state-hiu/cybergis-styles) repo.  As root (`sudo su -`) execute the following commands.

```
cd /opt
git clone https://github.com/state-hiu/cybergis-styles.git cybergis-styles.git
```




