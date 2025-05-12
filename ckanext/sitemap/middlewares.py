from ckan import types
from ckan.plugins import toolkit as tk

from ckanext.sitemap import configs


def add_noindex_nofollow(response: types.Response) -> types.Response:
    """Add X-Robots-Tag header to control search engine indexing behavior.

    This function adds noindex/nofollow tags to pages that should not be indexed
    by search engines.

    Pages that are not in the indexable_endpoints list or contain query parameters
    will not be indexed.
    """
    endpoint = ".".join(tk.get_endpoint())

    # Default to noindex/nofollow for non-indexable endpoints
    if endpoint not in configs.sitemap_indexable_endpoints():
        response.headers["X-Robots-Tag"] = "noindex, nofollow"
        return response

    # Remove any existing X-Robots-Tag header
    response.headers.pop("X-Robots-Tag", None)

    # Add noindex/nofollow for pages with query parameters
    if "?" in tk.request.url:
        response.headers["X-Robots-Tag"] = "noindex, nofollow"
        return response

    return response
