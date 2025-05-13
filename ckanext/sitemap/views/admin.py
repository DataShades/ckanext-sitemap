from __future__ import annotations

import json
import requests
from urllib.parse import urljoin

from flask import Blueprint, render_template
from flask.views import MethodView

from ckan.model.system_info import set_system_info, delete_system_info
from ckan.plugins import toolkit as tk

from ckanext.sitemap import configs, utils
from ckanext.sitemap.schemas.schema import sitemap_schema


sitemap_admin = Blueprint("sitemap_admin", __name__)

class SitemapAdminView(MethodView):
    """A MethodView for managing sitemap administration in a CKAN sitemap extension.
    
    This view provides endpoints for displaying, generating, and managing XML sitemaps
    through CKAN's admin interface. It handles both GET requests for viewing the current
    sitemap status and POST requests for triggering sitemap regeneration.

    Typical usage example:
        >>> view = SitemapAdminView.as_view('sitemap_admin')
        >>> app.add_url_rule('/ckan-admin/sitemap', view_func=view)

    Attributes:
        template (str): The path to the Jinja2 template for rendering the admin interface.
        sitemap_service (SitemapService): Service layer for sitemap generation operations.
    """
    def get(self):
        """Handle GET requests to display the sitemap admin interface.
        
        Retrieves the current sitemap status including last generation time,
        URL count, and any existing errors. Renders the admin template with this data.

        Returns:
            str: Rendered HTML template with sitemap status context.
            
        Raises:
            403 Forbidden: If the requesting user is not a CKAN sysadmin.
        """
        if tk.current_user.is_anonymous:
            return tk.abort(403, tk._("Need to be system administrator to administer"))
        data=utils.get_sitemap_settings()
        robots_txt = utils.get_sitemap_config("robots_txt")
        if not robots_txt:
            data["robots_txt"] = utils.get_default_robots_txt()

        return render_template("admin/sitemap_settings.html", data=data)


    def post(self):
        """Handle POST requests to regenerate the sitemap.
        
        Triggers a background job to regenerate the XML sitemap and returns a flash
        message indicating success or failure. Redirects back to the admin interface.

        Returns:
            werkzeug.wrappers.Response: Redirect response to GET view.
            
        Raises:
            403 Forbidden: If the requesting user is not a CKAN sysadmin.
        """
        if tk.current_user.is_anonymous:
            return tk.abort(403, tk._("Need to be system administrator to administer"))
        try:
            data = tk.request.form

            validated_data, errors = tk.navl_validate(data, sitemap_schema())
            if errors:
                raise tk.ValidationError(errors)

            set_system_info("sitemap", json.dumps(validated_data))

            tk.h.flash_success(tk._("Settings saved successfully"))
        except tk.ValidationError as err:
            for field, msg in err.error_summary.items():
                tk.h.flash_error(f"{field}: {msg}")

        return tk.redirect_to("sitemap_admin.settings")


    def reset_settings(self):
        """Reset all sitemap-related settings to their default values.

        The operation is performed within a try-except block to ensure proper error
        handling and user feedback. System administrators should have exclusive access
        to this functionality.

        Returns:
            werkzeug.wrappers.Response: 
                A redirect response to the sitemap settings page ('sitemap_admin.settings' route).
        """
        if tk.current_user.is_anonymous:
            return tk.abort(403, tk._("Need to be system administrator to administer"))
        try:
            delete_system_info("sitemap")
            tk.h.flash_success(tk._("All sitemap settings have been reset to defaults"))
        except Exception as e:
            tk.h.flash_error(tk._("Error resetting settings: %s") % str(e))
        
        return tk.redirect_to("sitemap_admin.settings")


    def ping_search_engines(self):
        """Ping configured search engines with the sitemap URL to prompt indexing.
        
        Notifies major search engines about updates to the sitemap by sending HTTP GET
        requests to their ping endpoints. This helps accelerate discovery and indexing
        of new content. Handles both success and error cases with appropriate user feedback.

        Configuration:
            Requires SEARCH_ENGINES dictionary in configs module with format:
                {'Engine Name': 'ping_url_template'}
            Example:
                {'Google': 'http://www.google.com/ping?sitemap=%s'}

        Returns:
            werkzeug.wrappers.Response: 
                Redirect response to the sitemap settings view ('sitemap_admin.settings').
        """
        engines = configs.SEARCH_ENGINES
        site_url = tk.config.get("ckan.site_url", "http://localhost:5000")
        sitemap_url = tk.url_for("sitemap.index")

        for name, url in engines.items():
            try:
                final_url = url + urljoin(site_url, sitemap_url)
                requests.get(final_url, timeout=5)
                tk.h.flash_success(tk._("Sitemap pinged to %s") % name)
            except Exception as e:
                tk.h.flash_error(tk._("Error pinging %s: %s") % name, str(e))

        return tk.redirect_to("sitemap_admin.settings")


sitemap_admin.add_url_rule(
    "/ckan-admin/sitemap",
    endpoint="settings",
    view_func=SitemapAdminView.as_view("sitemap_settings"),
    methods=["GET", "POST"]
)

sitemap_admin.add_url_rule(
    "/ckan-admin/sitemap/reset",
    endpoint="reset_settings",
    view_func=SitemapAdminView().reset_settings,
    methods=["GET", "POST"]
)

sitemap_admin.add_url_rule(
    "/ckan-admin/sitemap/ping",
    endpoint="ping_search_engines",
    view_func=SitemapAdminView().ping_search_engines,
    methods=["GET", "POST"]
)
