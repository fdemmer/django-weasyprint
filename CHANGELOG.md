# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.2.0] - 2022-08-07

- Attempt to load static files from disk when using `ManifestStaticFilesStorage` (#48)
- Add debug logging to django_url_fetcher
- Add Python 3.10 and Django 4.1 to test matrix, remove Django 2.2

## [1.1.0.post2] - 2022-02-24

Another post-release backporting fixes from 2.x for those still using WeasyPrint/Cairo.

- Add `font_config` argument to `WeasyTemplateResponse.get_css()` to properly
  set up the `weasyprint.CSS` instance for `weasyprint.HTML.render()` (20f701b, #54)
- Add Django 3.2 & 4.0 to test matrix, remove 3.0 & 3.1

## [2.1.0] - 2021-10-28

- Add `font_config` argument to `WeasyTemplateResponse.get_css()` to properly
  set up the `weasyprint.CSS` instance for `weasyprint.HTML.render()` (f944d45, #54)

## [2.0.0] - 2021-10-26

- [WeasyPrint >= 53.0](https://github.com/Kozea/WeasyPrint/releases/tag/v53.0)
  is required ("PDF is the only output format supported!")
- Remove `PNGView` and `CONTENT_TYPE_*` constants
- Add Django 3.2 to test matrix, remove 3.0

## [1.1.0.post1] - 2021-08-10

- Pin WeasyPrint<53 due to module path change (thanks @hnb2, @n1ngu, @ThomSawyer)

## [1.1.0] - 2021-02-19

- Add `pathlib` support to `django_url_fetcher` (ba77f41, #42, by @niccolomineo)
- Fix missing import in README example (2f33713, by @ScottBarkman)
- Fix typo in CHANGELOG (293e6e7, by @GitRon)

## [1.0.2.post1] - 2021-08-10

- Pin WeasyPrint<53 due to module path change

## [1.0.2] - 2020-10-07

- Handle `SCRIPT_NAME` being added to `MEDIA_URL` in Django 3.1
  (https://code.djangoproject.com/ticket/25598)

## [1.0.1] - 2020-05-02

- Fix classifiers and changelog

## [1.0.0] - 2020-05-02

- Drop Python 2 support: WeasyPrint >= 43 and Django >= 2.2 are required

## [0.6.0] - 2020-04-27

- Update README to demonstrate override of URL fetcher (65ced6f)
- Fix URL fetcher when used with empty `MEDIA_URL` (fd3fb30, #34)
- Add tests for views and `django_url_fetcher` & tox configuration

## [0.5.5] - 2019-12-20

- Update signature of `weasyprint.default_url_fetcher` by Vlastimil Zíma (c9abfe8)
- Add `font_config` to handle `@font-config` rules

  An additional argument called font_config must be provided to handle
  `@font-config` rules. The same `fonts.FontConfiguration` object must be
  used for different CSS objects applied to the same document.

  https://weasyprint.readthedocs.io/en/latest/api.html#weasyprint.CSS

## [0.5.4] - 2018-07-16

- Fix for usage of `urlparse` by Jay Ennis (244b89b)

## [0.5.3] - 2018-07-09

- Use Python 3 compatible import of `urlparse` by Christian Karrié (4eb72cf)

## [0.5.2] - 2018-03-08

- Fix for `content_type` with WeasyTemplateResponse

## [0.5.1] - 2018-03-08

- Add `custom_url_fetcher` reading `file://` urls directly from disk or storage
- Add `content_type` to WeasyTemplateResponse
- Fixed example in README (46fc62e)

## [0.5.0] - 2018-02-02

- Packaging improvements by Thomas Grainger (8baf780)
- Require Django>=1.8

## [0.4] - 2017-09-26

- Add override for URL fetcher by Thomas Jost (d946d6b)

  Overriding the default URL fetcher from Weasyprint is often useful.
  For instance, this makes it easy to open local files that are exposed on other
  subdomains (CDN…) without having to do a single network request, which makes
  the PDF rendering *much* faster.

- Fix for Content-Disposition

## [0.3] - 2017-04-05

- Add switch for 'attachment' Content-Disposition

## [0.2] - 2017-04-05

- Transfer of GitHub repo to Florian Demmer
- Merge improvements by Tim Bell (6f10a0a), Thomas Desveaux (249ad56) and
  Bruno Alla (ce1e2dc, ddc0343)
- Add generating PNG

## [0.1] - 2017-01-13

- Initial release by Jeroen Dekkers
- Some credits for API design and actual source for documentation go to
  Filip Wasilewski and other authors and contributors of django-easy-pdf.
