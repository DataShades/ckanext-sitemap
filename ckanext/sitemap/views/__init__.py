from ckanext.sitemap.views.admin import sitemap_admin
from ckanext.sitemap.views.sitemap import sitemap
from ckanext.sitemap.views.robots import robots


def get_blueprints():
    return [sitemap, sitemap_admin, robots]
