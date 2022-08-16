'''
Sitemap plugin for CKAN
'''

import ckan.plugins as p

from ckan.plugins.toolkit import config, url_for
from ckan.model import Session, Package, PackageExtra
from flask import Blueprint, make_response

from lxml import etree
from datetime import date
import logging


SITEMAP_NS = "http://www.sitemaps.org/schemas/sitemap/0.9"

XHTML_NS = "http://www.w3.org/1999/xhtml"

log = logging.getLogger(__file__)


def render_sitemap(country):
    site_url = config.get('ckan.site_url')
    pkgs = Session.query(Package).filter(Package.type == 'dataset').filter(Package.private != True). \
        filter(Package.state == 'active').all()
    log.debug(pkgs)
    root = etree.Element("urlset", nsmap={None: SITEMAP_NS, 'xhtml': XHTML_NS})
    for pkg in pkgs:
        pkg_countries: list = Session.query(PackageExtra).filter(PackageExtra.package_id == pkg.id). \
            filter(PackageExtra.key == 'member_countries').first()
        if country.upper() in pkg_countries.value or (country.upper() == 'ALL'):
            url = etree.SubElement(root, 'url')
            loc = etree.SubElement(url, 'loc')
            pkg_url = url_for('dataset.read', id=pkg.name)
            loc.text = site_url + pkg_url
            lastmod = etree.SubElement(url, 'lastmod')
            lastmod.text = pkg.metadata_modified.strftime('%Y-%m-%d')

    # Add XML header
    content = etree.tostring(root, pretty_print=True, encoding='unicode')
    content = '<?xml version="1.0" encoding="UTF-8"?>\n' + content
    headers = {'Content-Type': 'application/xml; charset=utf-8'}
    return make_response((content, 200, headers))


def testme():
    content = 'Test Me'
    headers = {'Content-Type': 'text/html; charset=utf-8'}
    return make_response((content, 200, headers))


class SitemapPlugin(p.SingletonPlugin):
    p.implements(p.IBlueprint)

    def get_blueprint(self):
        blueprint = Blueprint("sitemap", self.__module__, url_prefix='/sitemap/<path:country>')
        blueprint.add_url_rule("/sitemap.xml", view_func=render_sitemap)        
        
        # Use this to debug routes
        #blueprint.add_url_rule("/testme", view_func=testme)       
        return blueprint  
        
