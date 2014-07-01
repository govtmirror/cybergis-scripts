cybergis-scripts
================

## Description

This repository contains scripts used in the CyberGIS.  The scripts contained herein are written in BASH and python.  They have been developed on and for Ubuntu; however, they may work on other systems.  The bin folder includes all the scripts that will be added to the path.  The lib folder includes scripts that are not designed to be called directly off the command line.

See the guides in the cybergis-guides repo at [https://github.com/state-hiu/cybergis-guides/](https://github.com/state-hiu/cybergis-guides), for examples on using the scripts.

### CyberGIS
The Humanitarian Information Unit has been developing a sophisticated geographic computing infrastructure referred to as the CyberGIS. The CyberGIS provides highly available, scalable, reliable, and timely geospatial services capable of supporting multiple concurrent projects.  The CyberGIS relies on primarily open source projects, such as PostGIS, GeoServer, GDAL, OGR, and OpenLayers.  The name CyberGIS is derived from the term geospatial cyberinfrastructure.

## Installation

These installation instructions are subject to change.  Right now, since there are non-debian package dependencies, you can really extract the scripts to whatever directory you want.  The instructions below are suggested as they mirror Linux best practices for external packages.  Please be careful when installing gdal-bin and python-gdal packages as they may require different version of some packages than other programs, such as the OpenGeo Suite.  It is recommended to test this and other GDAL scripts within a vagrant environment first.

As root, execute the following commands:
```
apt-get update
apt-get install -y curl vim git
#Only install gdal and numpy if it is needed and won't conflict with a different installation.
#gdal and numpy are only needed for cybergis-script-stretch.py, cybergis-script-burn-alpha.py, cybergis-script-hide-no-data.py, cybergis-script-pull-wfs.sh, cybergis-script-pull-arcgis.sh, and cybergis-script-pull-shapefile.sh
apt-get install -y gdal-bin python-gdal python-numpy
#==#
cd /opt
git clone https://github.com/state-hiu/cybergis-scripts.git cybergis-scripts.git
cp cybergis-scripts.git/profile/cybergis-scripts.sh /etc/profile.d/
```
Logout and Login

## Usage

### EC2

```
cybergis-script-ec2.sh [prod|dev] [resize]

    cybergis-script-postgis.sh prod resize <dev>
    
```

### Imagery Processing

```
cybergis-script-stretch.py <input_file> <breakpoints_file> <output_file> <rows>
```
```
cybergis-script-burn-alpha.py <input_file> <alpha_file> <alpha_band_index> <output_file>
```
```
cybergis-script-hide-no-data.py <input_file> <output_file>
```

### ROGUE

```
cybergis-script-init-rogue.sh [prod|dev] [use|rvm|gems|geonode|server|remote|remote2|aws|sns]
    
    cybergis-script-init-rogue.sh prod server [tms|geonode] <name> <url>
    cybergis-script-init-rogue.sh prod remote <user:password> <localRepoName> <localGeonodeURL> <remoteName> <remoteRepoName> <remoteGeoNodeURL> <remoteUser> <remotePassword>
    cybergis-script-init-rogue.sh prod remote2 <user:password> <repoURL> <remoteName> <remoteURL> <remoteUser> <remotePassword>
    cybergis-script-init-rogue.sh prod cron <direction> <user> <password> <localRepoName> <remoteName> <authorname> <authoremail> [hourly|daily|weekly|monthly]
    cybergis-script-init-rogue.sh prod cron2 <direction> <user> <password> <localRepoName> <remoteName> <authorname> <authoremail> <frequency>
```

To manually execute the post_commit_hook.py script that automates notification of GeoGit commits, you need to use GeoNode's pyton interpreter and not the system default.  This script requires that the AWS tools are installed and SNS is configured.  As root (`sudo su -`) run:
```
export DJANGO_SETTINGS_MODULE=rogue_geonode.settings
/var/lib/geonode/bin/python /opt/cybergis-scripts.git/lib/rogue/post_commit_hook.py "test now"
```

### PostGIS

```
cybergis-script-postgis.sh [prod|dev] [install]

    cybergis-script-postgis.sh prod install [rds|local] <host> <port> <user> <password> <database> <template>
    
```

### Replication

```
cybergis-script-pull-wfs.sh <wfs> <namespace> <featuretype> <dbname> <dbuser> <dbpass> <table>
```
```
cybergis-script-pull-arcgis.sh <service> <field> <dbname> <dbuser> <dbpass> <table>
```
```
cybergis-script-pull-shapefile.sh <url> <shapefile> <dbname> <dbuser> <dbpass> <table>
```



## Contributing

HIU is currently not accepting pull requests for this repository.

## License
This project constitutes a work of the United States Government and is not subject to domestic copyright protection under 17 USC § 105.

However, because the project utilizes code licensed from contributors and other third parties, it therefore is licensed under the MIT License. http://opensource.org/licenses/mit-license.php. Under that license, permission is granted free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the conditions that any appropriate copyright notices and this permission notice are included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
