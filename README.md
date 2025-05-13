# CKAN Sitemap Extension

A CKAN extension that generates multilingual sitemaps with advanced features including:

- Multilingual support with `hreflang` tags
- Admin interface for configuration
- Support for datasets, organizations, and groups
- Support for individual priorities for different types of content

## Features

- Generates standard-compliant sitemap.xml
- Supports multiple languages with proper hreflang annotations
- Admin interface to manage settings
- Automatic detection of available translations
- Configurable priorities and change frequencies
- Supports ability to ping Google and Bing search engines
- Supports ability to add blocking 'X-Robots-Tag' header to prevent search engines from indexing certain content
- Supports ability to update robots.txt file using admin interface

Check full [documentation](https://datashades.github.io/ckanext-sitemap/) for more information.

## Installation

1. Activate your CKAN virtual environment:
```
    . /usr/lib/ckan/default/bin/activate
```

2. Install the extension:
```
    pip install -e git+https://github.com/Datashades/ckanext-sitemap.git#egg=ckanext-sitemap
```

3. Add `sitemap` to your `ckan.plugins` in the CKAN config file:
```
    ckan.plugins = ... sitemap
```

4. Configure the extension (optional) in your CKAN config file:
```yaml
version: 1
groups:
  - annotation: ckanext-sitemap
    options:
      - key: ckanext.sitemap.default_limit
        description: Limit for the number of items per sitemap section
        default: 1000
        type: int
        editable: true

      - key: ckanext.sitemap.default_priority
        description: Default priority for sitemap entries in all sections
        default: 0.5
        type: float
        editable: true

      - key: ckanext.sitemap.default_frequency
        description: Default change frequency for sitemap entries in all sections
        default: monthly
        type: str
        editable: true

      - key: ckanext.sitemap.included_endpoints
        description: |
          List of CKAN endpoints that should be included in the sitemap index.

          This function reads a configuration value from CKAN's settings to determine which
          endpoints should be indexed in the sitemap. The endpoints are typically important
          pages that should be crawled by search engines.

          The configuration value is expected to be a space-separated string of endpoint names
          in the format 'blueprint.endpoint_name' (e.g., 'dataset.read', 'organization.index').
        default: []
        type: list
        editable: true

      - key: ckanext.sitemap.enable_indexing_block
        description: |
          Determines whether search engine indexing should be blocked via sitemap configuration.

          This function checks the CKAN configuration to see if the sitemap should include
          directives that prevent search engines from indexing certain content.
        default: false
        type: bool
        editable: true
```

5. Multilingual settings
```
    ckan.locale_default = en
    ckan.locales_offered = en fr es
```

## Usage

After installation, the sitemap will be available at `/sitemap.xml`.

Access the admin interface at `/ckan-admin/sitemap` to configure the extension.


## Development Installation

For developing the extension:

1. Clone the repository:
```
    git clone https://github.com/Datashades/ckanext-sitemap.git
    cd ckanext-sitemap
```

2. Install in development mode:
```
    pip install -e .
    pip install -r dev-requirements.txt
```


## Testing

To run the tests:
```
    pytest --ckan-ini=test.ini
```


## License

This extension is open source and licensed under the GNU Affero General Public License (AGPL) v3.0.
