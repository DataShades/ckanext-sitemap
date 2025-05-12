import json

from typing import Any

from werkzeug.routing import BuildError

from ckan import model
from ckan.model.system_info import SystemInfo
from ckan.plugins import toolkit as tk

from ckanext.sitemap import configs


def get_sitemap_settings():
    """Get dictionary of all sitemap settings from SystemInfo table."""
    sysinfo_data = (
        model.Session.query(SystemInfo)
        .filter(SystemInfo.key == ("sitemap")).first()
    )
    if not sysinfo_data:
        return {}
    return json.loads(sysinfo_data.value)


def get_sitemap_config(key: str, default: Any = None) -> Any:
    """Get sitemap config option by key.

    Args:
        key (str): name of config item.
        default (Any, optional): value if key is absent. Defaults to None.

    Returns:
        Any: value of sitemap config.
    """
    sitemap_settings = get_sitemap_settings()
    value = sitemap_settings.get(key)
    if not value or value == "":
        return default
    return value


def get_endpoints_without_arguments() -> list[str]:
    """Filters indexable endpoints to return only those that don't require URL arguments.
    
    This function checks which endpoints from the sitemap configuration can be generated
    without requiring additional arguments. It's useful for identifying static pages that
    can be included directly in a sitemap without dynamic parameters.
    """
    indexable_endpoints = configs.sitemap_indexable_endpoints()
    endpoints_without_arguments = []
    for endpoint in indexable_endpoints:
        try:
            tk.url_for(endpoint)
            endpoints_without_arguments.append(endpoint)
        except BuildError:
            continue
    return endpoints_without_arguments


def get_default_robots_txt(self):
    """Generate the default robots.txt content with standard CKAN disallow rules."""
    sitemap_url = tk.url_for("sitemap.index", _external=True)
    
    content = [
        "User-agent: *",
        "Disallow: /dataset/rate/",
        "Disallow: /revision/",
        "Disallow: /dataset/*/history",
        "Disallow: /api/",
        "Disallow: /*?view_id=*",
        "Disallow: */view/*",
        "Disallow: /*?tags=*",
        f"Sitemap: {sitemap_url}"
    ]

    return '\n'.join(content)
