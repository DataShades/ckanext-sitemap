from typing import Any

from ckan.common import _
from ckan.plugins import toolkit as tk

from ckanext.sitemap import configs


def get_available_languages():
    """Get list of available languages from config."""
    langs = tk.config.get("ckan.locales_offered", "en")
    return langs.split()


def get_default_language():
    """Get default language from CKAN config."""
    return tk.config.get("ckan.locale_default", "en")


def get_config(key, default=None):
    """Get configuration value from CKAN config."""
    value = tk.config.get(key)
    if not value or value == "":
        return default
    return value


def get_frequency_options():
    """Get frequency options for sitemap."""
    return [
        {
            "value": option,
            "text": _(option.capitalize()),
        }
        for option in configs.SITEMAP_FREQUENCY_OPTIONS
    ]


def as_bool(value):
    """Convert value to boolean"""
    return tk.asbool(value)


def get_sitemap_settings(key: str) -> Any:
    """Get sitemap core settings from configs module."""
    settings = {
        "sitemap_sections": configs.SITEMAP_SECTIONS,
        "sitemap_default_limit": configs.sitemap_default_limit(),
        "sitemap_default_priority": configs.sitemap_default_priority(),
        "sitemap_default_changefreq": configs.sitemap_default_changefreq(),
        "sitemap_indexable_endpoints": configs.sitemap_indexable_endpoints(),
        "sitemap_date_format": configs.sitemap_date_format(),
        "sitemap_include_hreflang": configs.sitemap_include_hreflang(),
    }
    return settings.get(key, None)
