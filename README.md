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

    . /usr/lib/ckan/default/bin/activate

2. Install the extension:

    pip install -e git+https://github.com/Datashades/ckanext-sitemap.git#egg=ckanext-sitemap

3. Add `sitemap` to your `ckan.plugins` in the CKAN config file:

    ckan.plugins = ... sitemap

4. Configure the extension (optional) in your CKAN config file:

    ckanext.sitemap.default_limit = 5000
    ckanext.sitemap.default_priority = 0.8
    ckanext.sitemap.default_frequency = monthly
    ckanext.sitemap.included_endpoints = home.index dataset.search organization.index group.index
    ckanext.sitemap.enable_indexing_block = false

5. Multilingual settings

    ckan.locales_offered = en uk ru
    ckan.locale_default = en

## Usage

After installation, the sitemap will be available at `/sitemap.xml`.

Access the admin interface at `/ckan-admin/sitemap` to configure the extension.

## Development Installation

For developing the extension:

1. Clone the repository:

    git clone https://github.com/Datashades/ckanext-sitemap.git
    cd ckanext-sitemap

2. Install in development mode:

    pip install -e .
    pip install -r dev-requirements.txt


## Testing

To run the tests:

    pytest --ckan-ini=test.ini


## License

This extension is open source and licensed under the GNU Affero General Public License (AGPL) v3.0.
