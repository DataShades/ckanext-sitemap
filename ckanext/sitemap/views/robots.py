from __future__ import annotations

from flask import Blueprint, make_response
from flask.views import MethodView

import ckan.lib.base as base

from ckanext.sitemap import utils


robots = Blueprint("sitemap_robots", __name__)

class RobotsTxtView(MethodView):
    """A MethodView for dynamically generating robots.txt files.
    
    This view handles requests for robots.txt files with configurable content.
    """
    def get(self):
        """Generate and serve the robots.txt content."""
        if utils.get_sitemap_config("enable_robots_txt"):
            content = utils.get_sitemap_config("robots_txt")
            if not content:
                content = utils.get_default_robots_txt
        else:
            content = base.render("home/robots.txt")

        return make_response(
            (content, 200, {"Content-Type": "text/plain; charset=utf-8"})
        )


robots.add_url_rule(
    "/robots.txt",
    view_func=RobotsTxtView.as_view("index")
)
