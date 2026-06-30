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
        type: base
        editable: true

      - key: ckanext.sitemap.default_frequency
        description: Default change frequency for sitemap entries in all sections
        default: monthly
        type: base
        editable: true

      - key: ckanext.sitemap.default_changefreq
        description: Default change frequency for sitemap entries in all sections
        default: monthly
        type: base
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

      - key: ckanext.sitemap.standard_urlset
        description: Render URL entries directly under the urlset element instead of grouping them by section.
        default: false
        type: bool
        editable: true

      - key: ckanext.sitemap.datasets_fetch_all
        description: Fetch all public datasets using the dataset limit as the package_search batch size.
        default: false
        type: bool
        editable: true

      - key: ckanext.sitemap.pages_limit
        description: Limit for the number of page URLs in the sitemap.
        default: 1000
        type: int
        editable: true

      - key: ckanext.sitemap.pages_priority
        description: Priority for page URLs in the sitemap.
        default: 0.5
        type: base
        editable: true

      - key: ckanext.sitemap.pages_changefreq
        description: Change frequency for page URLs in the sitemap.
        default: monthly
        type: base
        editable: true

      - key: ckanext.sitemap.pages_exclude
        description: Exclude static pages from the sitemap.
        default: false
        type: bool
        editable: true

      - key: ckanext.sitemap.datasets_limit
        description: Limit for the number of dataset URLs, or package_search batch size when fetching all datasets.
        default: 1000
        type: int
        editable: true

      - key: ckanext.sitemap.datasets_priority
        description: Priority for dataset URLs in the sitemap.
        default: 0.5
        type: base
        editable: true

      - key: ckanext.sitemap.datasets_changefreq
        description: Change frequency for dataset URLs in the sitemap.
        default: monthly
        type: base
        editable: true

      - key: ckanext.sitemap.datasets_exclude
        description: Exclude datasets from the sitemap.
        default: false
        type: bool
        editable: true

      - key: ckanext.sitemap.organizations_limit
        description: Limit for the number of organization URLs in the sitemap.
        default: 1000
        type: int
        editable: true

      - key: ckanext.sitemap.organizations_priority
        description: Priority for organization URLs in the sitemap.
        default: 0.5
        type: base
        editable: true

      - key: ckanext.sitemap.organizations_changefreq
        description: Change frequency for organization URLs in the sitemap.
        default: monthly
        type: base
        editable: true

      - key: ckanext.sitemap.organizations_exclude
        description: Exclude organizations from the sitemap.
        default: false
        type: bool
        editable: true

      - key: ckanext.sitemap.groups_limit
        description: Limit for the number of group URLs in the sitemap.
        default: 1000
        type: int
        editable: true

      - key: ckanext.sitemap.groups_priority
        description: Priority for group URLs in the sitemap.
        default: 0.5
        type: base
        editable: true

      - key: ckanext.sitemap.groups_changefreq
        description: Change frequency for group URLs in the sitemap.
        default: monthly
        type: base
        editable: true

      - key: ckanext.sitemap.groups_exclude
        description: Exclude groups from the sitemap.
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

### Standard dataset-only sitemap

By default, the extension keeps its sectioned sitemap structure and limits each
section to `ckanext.sitemap.default_limit` items. To generate a standard sitemap
that includes every public dataset and excludes other sections, enable:

```ini
ckanext.sitemap.standard_urlset = true
ckanext.sitemap.datasets_fetch_all = true
ckanext.sitemap.pages_exclude = true
ckanext.sitemap.organizations_exclude = true
ckanext.sitemap.groups_exclude = true
```

When `datasets_fetch_all` is enabled, `datasets_limit` is used as the
`package_search` batch size rather than the maximum number of dataset URLs.

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
