"""Config getters of sitemap plugin."""

from __future__ import annotations

import ckan.plugins.toolkit as tk

from ckanext.sitemap.utils import get_sitemap_config


SITEMAP_DEFAULT_LIMIT = "ckanext.sitemap.default_limit"
SITEMAP_DEFAULT_PRIORITY = "ckanext.sitemap.default_priority"
SITEMAP_DEFAULT_CHANGEFREQ = "ckanext.sitemap.default_changefreq"
SITEMAP_INDEXABLE_ENDPOINTS = "ckanext.sitemap.indexable_endpoints"
SITEMAP_ENABLE_INDEXING_BLOCK = "ckanext.sitemap.enable_indexing_block"

SITEMAP_SECTIONS = [
    "pages",
    "datasets",
    "organizations",
    "groups"
]

SITEMAP_FREQUENCY_OPTIONS = [
    "always",
    "hourly",
    "daily",
    "weekly",
    "monthly",
    "yearly",
    "never",
]

SITEMAP_NS = "http://www.sitemaps.org/schemas/sitemap/0.9"
XHTML_NS = "https://www.w3.org/1999/xhtml"

SEARCH_ENGINES = {
    "Google": "https://www.google.com/ping?sitemap=",
    "Bing": "https://www.bing.com/ping?sitemap="
}


def sitemap_default_limit() -> int:
    """Get the limit for the number of items in each sitemap section.
    
    This limit is used to control the number of entries in each section
    of the sitemap (eg. pages, datasets, resources, organizations, groups).
    The default value is 10,000.
    """
    return int(tk.config.get(SITEMAP_DEFAULT_LIMIT, 10000))


def sitemap_default_priority() -> float:
    """Get default priority for sitemap entries.
    
    This is a float value between 0.0 and 1.0 that indicates the priority
    of the sitemap entry relative to other entries.
    The default value is 0.5.
    """
    return float(tk.config.get(SITEMAP_DEFAULT_PRIORITY, 0.5))


def sitemap_default_changefreq() -> str:
    """Get default change frequency for sitemap entries.
    
    This is a string that indicates how frequently the content of the
    sitemap is expected to change. The possible values: always, hourly, daily,
    weekly, monthly, yearly, never.
    The default value is "weekly".
    """
    return tk.config.get(SITEMAP_DEFAULT_CHANGEFREQ, "weekly")


def sitemap_include_hreflang() -> bool:
    """Check if hreflang attribute should be included in the sitemap.
    
    This is a boolean value that indicates whether the hreflang
    attribute should be included in the sitemap.
    The default value is False.
    """
    return get_sitemap_config("include_hreflang", False)


def sitemap_indexable_endpoints() -> set[tuple[str, str]]:
    """Get the list of CKAN endpoints that should be included in the sitemap index.
    
    This function reads a configuration value from CKAN's settings to determine which
    endpoints should be indexed in the sitemap. The endpoints are typically important
    pages that should be crawled by search engines.

    The configuration value is expected to be a comma-separated string of endpoint names
    in the format 'blueprint.endpoint_name' (e.g., 'dataset.read', 'organization.index').
    
    The default value is an empty list.
    """
    return tk.aslist(tk.config.get(SITEMAP_INDEXABLE_ENDPOINTS, ""))


def sitemap_enable_indexing_block() -> bool:
    """Determines whether search engine indexing should be blocked via sitemap configuration.

    This function checks the CKAN configuration to see if the sitemap should include
    directives that prevent search engines from indexing certain content.
    """
    return tk.asbool(tk.config.get(SITEMAP_ENABLE_INDEXING_BLOCK, False))


def sitemap_date_format() -> str:
    """Get the date format for the sitemap entries.
    
    This is a string that indicates the format of the date in the sitemap
    entries. Available formats are:
    - "default": YYYY-MM-DD
    - "iso": ISO 8601 format (YYYY-MM-DDTHH:MM:SSZ)
    The default value is "default".
    """
    return get_sitemap_config("date_format", "default")
