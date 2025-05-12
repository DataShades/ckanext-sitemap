from ckanext.sitemap.views.admin import sitemap_admin
from ckanext.sitemap.views.sitemap import sitemap


def get_blueprints():
    return [sitemap, sitemap_admin]
