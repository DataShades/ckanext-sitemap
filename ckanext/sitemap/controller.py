import ckan.plugins as p
from ckan.lib.base import BaseController, config
from ckan.common import OrderedDict, _, json, request, c, g, response
from ckan.controllers.package import PackageController
import ckan.logic as logic
import ckan.model as model

import ckan.lib.base as base
NotFound = logic.NotFound
NotAuthorized = logic.NotAuthorized
ValidationError = logic.ValidationError
import sqlalchemy
_select = sqlalchemy.sql.select
_and_ = sqlalchemy.and_

class SitemapController(base.BaseController):

    def sitemap(self):

        response.headers['Content-Type'] = 'application/xml'
        response.charset = 'UTF-8'
        sitemap = '<?xml version="1.0" encoding="UTF-8"?> \n'
        sitemap += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"> \n'
        package_revision_table = model.package_revision_table
        query = _select([package_revision_table.c.name, package_revision_table.c.revision_timestamp])
        query = query.where(_and_(
            package_revision_table.c.state == 'active',
            package_revision_table.c.current == True,
            package_revision_table.c.private == False,
            ))
        query = query.order_by(package_revision_table.c.name)
        for package in query.execute():
            sitemap += '<url><loc>' + request.host_url.replace('http:','https:') + '/data/dataset/' + package.name + '</loc><lastmod>' + package.revision_timestamp.strftime('%Y-%m-%d') + '</lastmod></url> \n'
        for group in model.Group.all():
            sitemap += '<url><loc>' + request.host_url.replace('http:','https:') + '/data/group/' + group.name + '</loc></url> \n'
        sitemap += '</urlset> \n'
        return sitemap
