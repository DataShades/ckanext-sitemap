import ckan.plugins.toolkit as tk
from ckanext.sitemap.logic.validators import is_ranged_float


def sitemap_schema():
    ignore_empty = tk.get_validator("ignore_empty")
    natural_number_validator = tk.get_validator("natural_number_validator")
    unicode_safe = tk.get_validator("unicode_safe")
    
    return {
        # General section options 
        "date_format": [ignore_empty, unicode_safe],
        "include_hreflang": [ignore_empty],
        "robots_txt": [ignore_empty, unicode_safe],
        
        # Pages section options 
        "pages_limit": [ignore_empty, natural_number_validator],
        "pages_priority": [ignore_empty, is_ranged_float],
        "pages_changefreq": [ignore_empty, unicode_safe],
        "pages_api": [ignore_empty],
        "pages_exclude": [ignore_empty],
        
        # Dataset section options 
        "datasets_limit": [ignore_empty, natural_number_validator],
        "datasets_priority": [ignore_empty, is_ranged_float],
        "datasets_changefreq": [ignore_empty, unicode_safe],
        "datasets_exclude": [ignore_empty],
        
        # Organizations section options 
        "organizations_limit": [ignore_empty, natural_number_validator],
        "organizations_priority": [ignore_empty, is_ranged_float],
        "organizations_changefreq": [ignore_empty, unicode_safe],
        "organizations_exclude": [ignore_empty],
        
        # Groups section options 
        "groups_limit": [ignore_empty, natural_number_validator],
        "groups_priority": [ignore_empty, is_ranged_float],
        "groups_changefreq": [ignore_empty, unicode_safe],
        "groups_exclude": [ignore_empty],
    }
