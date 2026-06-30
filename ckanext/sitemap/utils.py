from __future__ import annotations

import json

from typing import Any
from werkzeug.routing import BuildError

from ckan import model
from ckan.model.system_info import SystemInfo
from ckan.plugins import toolkit as tk


SITEMAP_CONFIG_KEYS = (
    "date_format",
    "include_hreflang",
    "standard_urlset",
    "robots_txt",
    "pages_limit",
    "pages_priority",
    "pages_changefreq",
    "pages_exclude",
    "datasets_limit",
    "datasets_priority",
    "datasets_changefreq",
    "datasets_fetch_all",
    "datasets_exclude",
    "organizations_limit",
    "organizations_priority",
    "organizations_changefreq",
    "organizations_exclude",
    "groups_limit",
    "groups_priority",
    "groups_changefreq",
    "groups_exclude",
)

SITEMAP_CHECKBOX_KEYS = (
    "include_hreflang",
    "standard_urlset",
    "pages_exclude",
    "datasets_fetch_all",
    "datasets_exclude",
    "organizations_exclude",
    "groups_exclude",
)


def get_sitemap_settings() -> dict[str, Any]:
    """Get dictionary of all sitemap settings from SystemInfo table."""
    sysinfo_data = (
        model.Session.query(SystemInfo)
        .filter(SystemInfo.key == ("sitemap")).first()
    )
    if not sysinfo_data:
        return {}
    return json.loads(sysinfo_data.value)


def get_effective_sitemap_settings() -> dict[str, Any]:
    """Get sitemap settings with CKAN config values used as defaults."""
    data = {}
    for key in SITEMAP_CONFIG_KEYS:
        value = tk.config.get(f"ckanext.sitemap.{key}")
        if value is not None and value != "":
            data[key] = value

    data.update(get_sitemap_settings())
    return data


def get_sitemap_config(key: str, default: Any = None) -> Any:
    """Get sitemap config option by key.

    Args:
        key (str): name of config item.
        default (Any, optional): value if key is absent. Defaults to None.

    Returns:
        Any: value of sitemap config.
    """
    sitemap_settings = get_sitemap_settings()
    if key in sitemap_settings and sitemap_settings[key] != "":
        return sitemap_settings[key]

    value = tk.config.get(f"ckanext.sitemap.{key}")
    if value is None or value == "":
        return default
    return value


def get_endpoints_without_arguments() -> list[str]:
    """Filters indexable endpoints to return only those that don't require URL arguments.
    
    This function checks which endpoints from the sitemap configuration can be generated
    without requiring additional arguments. It's useful for identifying static pages that
    can be included directly in a sitemap without dynamic parameters.
    """
    from ckanext.sitemap import configs

    indexable_endpoints = configs.sitemap_indexable_endpoints()
    endpoints_without_arguments = []
    for endpoint in indexable_endpoints:
        try:
            tk.url_for(endpoint)
            endpoints_without_arguments.append(endpoint)
        except BuildError:
            continue
    return endpoints_without_arguments


def get_default_robots_txt() -> str:
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
