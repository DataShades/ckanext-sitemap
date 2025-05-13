from __future__ import annotations

from copy import copy
from datetime import datetime
from lxml import etree
from typing import Any
from urllib.parse import urljoin

from flask import Blueprint, make_response
from flask.views import MethodView

from ckan.plugins import toolkit as tk

from ckanext.sitemap import configs, utils


NSMAP = {None: configs.SITEMAP_NS, "xhtml": configs.XHTML_NS}

sitemap = Blueprint("sitemap", __name__)

class SitemapView(MethodView):
    """A MethodView for generating XML sitemaps in CKAN.
    
    This view generates sitemap.xml files following the sitemap protocol specification,
    including URLs for datasets, organizations, groups, and custom pages. The sitemap
    supports:
    - Multi-language content through hreflang tags
    - Customizable change frequency and priority
    - Filterable sections and configurable limits
    - Proper XML formatting with namespaces

    The sitemap is dynamically generated from CKAN's content and respects:
    - Private/draft dataset exclusion
    - Configurable limits per section
    - Localization settings
    - Custom date formatting
    """
    def __init__(self):
        self.site_url = tk.config.get("ckan.site_url", "http://localhost:5000")


    def get(self):
        """Handle GET requests to generate and serve the sitemap.xml file.
        
        Generates the complete sitemap XML structure, adds the XML header, and returns
        a properly formatted HTTP response with XML content type.

        Returns:
            flask.Response: A response object containing:
                - The generated XML content
                - HTTP status code 200
                - Content-Type header set to application/xml
        """
        # Generate sitemap XML content
        root = self._generate_sitemap_content()

        # Add XML header
        content = etree.tostring(root)
        content = '<?xml version="1.0" encoding="UTF-8"?>\n' + content.decode("utf-8")
        return make_response(
            (content, 200, {"Content-Type": "application/xml; charset=utf-8"})
        )


    def _generate_sitemap_content(self):
        """Generate the complete sitemap XML structure.
        
        Creates the root urlset element and populates it with URLs for all included
        sections (datasets, organizations, groups, pages). Configures each URL entry
        with:
        - Location (loc)
        - Last modification date (lastmod)
        - Change frequency (changefreq)
        - Priority (priority)
        - Optional hreflang alternate links

        Returns:
            lxml.etree.Element: The root XML element of the generated sitemap.
        """
        date_format = configs.sitemap_date_format()
        include_hreflang = configs.sitemap_include_hreflang()
        default_changefreq = configs.sitemap_default_changefreq()
        default_priority = configs.sitemap_default_priority()
        available_languages = tk.config.get("ckan.locales_offered", ["en"])

        root = etree.Element("urlset", attrib={}, nsmap=NSMAP)
        
        for section in self._get_included_sections():
            entities = etree.SubElement(root, section, attrib={}, nsmap=NSMAP)
            
            comment = etree.Comment(f"========== {section.capitalize()} ==========")
            entities.insert(1, comment)
            for entity in self._get_entities(section):
                url = etree.SubElement(entities, "url", attrib={}, nsmap=NSMAP)
                
                loc = etree.SubElement(url, "loc", attrib={}, nsmap=NSMAP)
                loc.text = self._get_entity_url(entity)
                
                # Include hreflang attribute if enabled in config
                if tk.asbool(include_hreflang):
                    attrib = {
                        "rel": "alternate",
                        "hreflang": "x-default",
                        "href": self._get_entity_url(entity)
                    }
                    etree.SubElement(url, "{https://www.w3.org/1999/xhtml}link", attrib=attrib, nsmap=NSMAP)

                    for lang in available_languages:
                        attrib = {
                            "rel": "alternate",
                            "hreflang": lang,
                            "href": self._get_entity_url(entity, lang)
                        }
                        etree.SubElement(url, "{https://www.w3.org/1999/xhtml}link", attrib=attrib, nsmap=NSMAP)
                
                lastmod = etree.SubElement(url, "lastmod", attrib={}, nsmap=NSMAP)
                if section in ["datasets", "resources"]:
                    date_str = entity["metadata_modified"]
                else:
                    date_str = datetime.now().strftime("%Y-%m-%d")
                lastmod.text = self._format_lastmod(date_str, date_format)
                
                changefreq = etree.SubElement(url, "changefreq", attrib={}, nsmap=NSMAP)
                changefreq.text = utils.get_sitemap_config(
                    f"{section}_changefreq",
                    str(default_changefreq)
                )
                
                priority = etree.SubElement(url, "priority", attrib={}, nsmap=NSMAP)
                priority.text = utils.get_sitemap_config(
                    f"{section}_priority",
                    str(default_priority)
                )

        return root


    def _get_included_sections(self) -> list[str]:
        """Get the list of sections to include in the sitemap.
        
        Filters the available sections based on configuration settings, excluding any
        sections marked with '<section_name>_exclude' in the sitemap settings.

        Returns:
            list[str]: A list of section names to include in the sitemap.
        """
        available_sections = copy(configs.SITEMAP_SECTIONS)
        for key in utils.get_sitemap_settings():
            if key.endswith("exclude"):
                available_sections.remove(key.split("_")[0])
        return available_sections


    def _format_lastmod(self, date_str: str, format: str) -> str:
        """Format a date string according to the specified format.
        
        Args:
            date_str (str): The date string to format
            format (str): The target format ('iso' for full ISO format, 
                        otherwise returns just the date part)

        Returns:
            str: The formatted date string
        """
        if format == "iso":
            return datetime.fromisoformat(date_str).astimezone().replace(microsecond=0).isoformat()
        else:
            return date_str.split("T")[0]


    def _get_entities(self, section: str) -> list[dict[str, Any]]:
        """Retrieve entities for a specific sitemap section.
        
        Args:
            section (str): The section name (datasets, organizations, groups, or pages)

        Returns:
            list[dict[str, Any]]: A list of entity dictionaries containing:
                - For datasets: package_search results
                - For organizations: organization_list results
                - For groups: group_list results
                - For pages: configured endpoints from sitemap_included_endpoints
        """
        result = []
        limit = int(utils.get_sitemap_config(
            f"{section}_limit",
            configs.sitemap_default_limit()
        ))
        start = 0

        if section == "pages":
            result = utils.get_endpoints_without_arguments()
            if limit < len(result):
                result =result[:limit]

        elif section == "datasets":
            result = tk.get_action("package_search")(
                {},
                {
                    "q": "state:active",
                    "rows": limit,
                    "start": start,
                    "include_private": False,
                    "include_drafts": False,
                },
            )["results"]
        elif section == "organizations":
            result = tk.get_action("organization_list")(
                {},
                {
                    "limit": limit,
                    "offset": start,
                    "all_fields": True,
                },
            )
        elif section == "groups":
            result = tk.get_action("group_list")(
                {},
                {
                    "limit": limit,
                    "offset": start,
                    "all_fields": True,
                },
            )

        return result


    def _get_entity_url(
        self, entity: dict[str, Any] | str, lang: str = None) -> str:
        """Generate the full URL for a sitemap entity.
        
        Args:
            entity (dict[str, Any] | str): The entity data or endpoint name
            lang (str, optional): Language code for localized URLs

        Returns:
            str: The complete absolute URL for the entity
        """
        if lang:
            base_url = urljoin(self.site_url, lang)
        else:
            base_url = self.site_url
        
        if isinstance(entity, str):
            return base_url + tk.h.url_for(entity)
        
        if entity.get("original_path"):
            return urljoin(base_url, entity["original_path"])
        return base_url + tk.url_for(entity["type"] + ".read", id=entity["name"])


sitemap.add_url_rule(
    "/sitemap.xml",
    view_func=SitemapView.as_view("index")
)
