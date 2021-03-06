#!/bin/bash
# -----------------------------------------------------------------------------
#   Copyright (C) 2017 University of Dundee. All rights reserved.
#
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 2 of the License, or
#   (at your option) any later version.
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License along
#   with this program; if not, write to the Free Software Foundation, Inc.,
#   51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# ------------------------------------------------------------------------------

## This script is DEPRECATED use in_place_import_as.sh instead


echo Starting
OMEROPATH=${OMEROPATH:-/opt/omero/server/OMERO.server/bin/omero}
PASSWORD=${PASSWORD:-ome}
HOST=${HOST:-outreach.openmicroscopy.org}
FOLDER=${FOLDER:-siRNAi-HeLa}
NUMBER=${NUMBER:-50}
OMEUSER=${OMEUSER:-user}
DATATYPE=${DATATYPE:-dataset}
for ((i=1;i<=$NUMBER;i++));
do  $OMEROPATH login -u $OMEUSER-$i -s $HOST -w $PASSWORD
    if [ "$DATATYPE" = "dataset" ]; then
        DatasetId=$($OMEROPATH obj new Dataset name=$FOLDER)
        $OMEROPATH import -d $DatasetId --transfer=ln_s "/OMERO/in-place-import/$FOLDER"
    elif [ "$DATATYPE" = "plate" ]; then
        $OMEROPATH import --transfer=ln_s "/OMERO/in-place-import/$FOLDER"
    fi
    $OMEROPATH logout
done
echo Finishing
