from __future__ import annotations

from importlib import import_module

from ckanext.sitemap import utils

sitemap_module = import_module("ckanext.sitemap.views.sitemap")


def test_sitemap_keeps_section_wrappers_by_default(monkeypatch):
    calls = []

    _patch_settings(
        monkeypatch,
        {
            "pages_exclude": "true",
            "organizations_exclude": "true",
            "groups_exclude": "true",
            "datasets_limit": "2",
        },
    )
    _patch_url_for(monkeypatch)

    def fake_package_search(_context, data_dict):
        calls.append(data_dict)
        return {
            "count": 3,
            "results": [
                _dataset("first-dataset"),
                _dataset("second-dataset"),
            ],
        }

    _patch_action(monkeypatch, fake_package_search)

    root = sitemap_module.SitemapView()._generate_sitemap_content()

    assert root.find("url") is None
    assert len(root.findall("datasets/url")) == 2
    assert [(call["start"], call["rows"]) for call in calls] == [(0, 2)]


def test_sitemap_can_render_standard_urlset_with_all_public_datasets(monkeypatch):
    calls = []
    datasets = [
        _dataset("first-dataset"),
        _dataset("second-dataset"),
        _dataset("third-dataset"),
    ]

    _patch_settings(
        monkeypatch,
        {
            "standard_urlset": "true",
            "datasets_fetch_all": "true",
            "pages_exclude": "true",
            "organizations_exclude": "true",
            "groups_exclude": "true",
            "datasets_limit": "2",
        },
    )
    _patch_url_for(monkeypatch)

    def fake_package_search(_context, data_dict):
        calls.append(data_dict)
        start = data_dict["start"]
        end = start + data_dict["rows"]
        return {
            "count": len(datasets),
            "results": datasets[start:end],
        }

    _patch_action(monkeypatch, fake_package_search)

    root = sitemap_module.SitemapView()._generate_sitemap_content()

    assert root.find("datasets") is None
    assert [loc.text for loc in root.findall("url/loc")] == [
        "http://localhost:5000/dataset/first-dataset",
        "http://localhost:5000/dataset/second-dataset",
        "http://localhost:5000/dataset/third-dataset",
    ]
    assert [(call["start"], call["rows"]) for call in calls] == [(0, 2), (2, 2)]


def test_sitemap_exclude_options_can_come_from_ini_config(monkeypatch):
    _patch_settings(monkeypatch, {})
    monkeypatch.setitem(sitemap_module.tk.config, "ckanext.sitemap.pages_exclude", "true")
    monkeypatch.setitem(sitemap_module.tk.config, "ckanext.sitemap.organizations_exclude", "true")
    monkeypatch.setitem(sitemap_module.tk.config, "ckanext.sitemap.groups_exclude", "true")

    assert sitemap_module.SitemapView()._get_included_sections() == ["datasets"]


def test_sitemap_admin_settings_override_ini_config(monkeypatch):
    _patch_settings(
        monkeypatch,
        {
            "pages_exclude": "true",
            "organizations_exclude": "false",
            "groups_exclude": "true",
        },
    )
    monkeypatch.setitem(sitemap_module.tk.config, "ckanext.sitemap.organizations_exclude", "true")

    assert sitemap_module.SitemapView()._get_included_sections() == ["datasets", "organizations"]


def test_effective_sitemap_settings_include_ini_config(monkeypatch):
    _patch_settings(monkeypatch, {})
    monkeypatch.setitem(sitemap_module.tk.config, "ckanext.sitemap.organizations_exclude", "true")

    assert utils.get_effective_sitemap_settings()["organizations_exclude"] == "true"


def test_sitemap_serializes_numeric_priority(monkeypatch):
    _patch_settings(
        monkeypatch,
        {
            "pages_exclude": "true",
            "organizations_exclude": "true",
            "groups_exclude": "true",
            "datasets_priority": 0.5,
        },
    )
    _patch_url_for(monkeypatch)

    def fake_package_search(_context, _data_dict):
        return {
            "count": 1,
            "results": [_dataset("first-dataset")],
        }

    _patch_action(monkeypatch, fake_package_search)

    root = sitemap_module.SitemapView()._generate_sitemap_content()

    assert root.find("datasets/url/priority").text == "0.5"


def _dataset(name: str) -> dict[str, str]:
    return {
        "type": "dataset",
        "name": name,
        "metadata_modified": "2026-06-29T12:34:56",
    }


def _patch_settings(monkeypatch, settings):
    monkeypatch.setattr(utils, "get_sitemap_settings", lambda: settings)


def _patch_url_for(monkeypatch):
    monkeypatch.setattr(
        sitemap_module.tk,
        "url_for",
        lambda endpoint, id=None: f"/dataset/{id}",
    )


def _patch_action(monkeypatch, package_search):
    monkeypatch.setattr(
        sitemap_module.tk,
        "get_action",
        lambda name: package_search,
    )
