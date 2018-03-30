#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
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


import omero
from omero.gateway import BlitzGateway
from omero.model.enums import UnitsTime
from omero.model import PlaneInfoI
from omero.rtypes import rint, unwrap


for i in range(2, 41):

    username = "user-%s" % i
    password = "password"
    host = "outreach.openmicroscopy.org"
    conn = BlitzGateway(username, password, host=host, port=4064)
    conn.connect()

    params = omero.sys.ParametersI()
    params.addString('username', username)
    query = "from Dataset where name='Condensation' \
             AND details.owner.omeName=:username"
    query_service = conn.getQueryService()
    dataset = query_service.findAllByQuery(query, params, conn.SERVICE_OPTS)

    dataset_id = dataset[0].getId().getValue()

    print 'dataset', dataset_id
    params2 = omero.sys.ParametersI()
    params2.addId(dataset_id)
    query = "select l.child.id from DatasetImageLink l where l.parent.id = :id"
    images = query_service.projection(query, params2, conn.SERVICE_OPTS)

    for k in range(0, len(images)):

        image_id = images[k][0].getValue()
        delta_t = 300

        image = conn.getObject("Image", image_id)

        params = omero.sys.ParametersI()
        params.addLong('pid', image.getPixelsId())
        query = "from PlaneInfo as Info where"\
                " Info.theZ=0 and Info.theC=0 and pixels.id=:pid"
        info_list = query_service.findAllByQuery(query, params,
                                                 conn.SERVICE_OPTS)

        print 'info_list', len(info_list)

        if len(info_list) == 0:
            print "Creating info...", image.getSizeT()
            info_list = []
            for t_index in range(image.getSizeT()):
                print '  t', t_index
                info = PlaneInfoI()
                info.theT = rint(t_index)
                info.theZ = rint(0)
                info.theC = rint(0)
                info.pixels = omero.model.PixelsI(image.getPixelsId(), False)
                dt = t_index * delta_t
                u = omero.model.TimeI(dt, UnitsTime.SECOND)
                info.deltaT = u
                info_list.append(info)

        else:
            for info in info_list:
                unwrap_t = unwrap(info.theT)
                unwrap_z = unwrap(info.theZ)
                print 'theT %s, theZ %s' % (unwrap_t, unwrap_z)
                t_index = info.theT.getValue()

                dt = t_index * delta_t
                u = omero.model.TimeI(dt, UnitsTime.SECOND)
                info.deltaT = u

        print "Saving info_list", len(info_list)
        conn.getUpdateService().saveArray(info_list)

    conn.close()
