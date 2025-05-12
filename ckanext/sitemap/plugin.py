import ckan.plugins as p
import ckan.plugins.toolkit as tk

from ckan import types
from ckan.common import CKANConfig

from ckanext.sitemap.middlewares import add_noindex_nofollow
from ckanext.sitemap.configs import sitemap_enable_indexing_block


@tk.blanket.blueprints
@tk.blanket.helpers
@tk.blanket.validators
class SitemapPlugin(p.SingletonPlugin):
    p.implements(p.IConfigurer)
    p.implements(p.IDomainObjectModification, inherit=True)
    p.implements(p.IMiddleware, inherit=True)

    # IConfigurer
    def update_config(self, config_):
        tk.add_template_directory(config_, "templates")
        tk.add_public_directory(config_, "public")
        tk.add_resource("assets", "sitemap")

    # IMiddleware
    def make_middleware(self, app: types.CKANApp, config: CKANConfig) -> types.CKANApp:
        if sitemap_enable_indexing_block():
            app.after_request(add_noindex_nofollow)
        return app
