# mico

Demo brochure site showcasing product listings. Product cards now display
example prices and discounts. A promotional popup appears after 20 seconds of
inactivity prompting visitors to enter their name and phone number to claim a
20% discount.

## i18n

The project uses Django's `LocaleMiddleware` with English and Macedonian enabled.
Language can be changed from the navbar selector. The choice is stored in the
session using Django's `set_language` view.

## Fixtures and search

Load mock products:

```bash
python manage.py loaddata products_mock.json
```

Search products via API:

```
/api/products/?q=term
```

## Partials

Reusable template fragments live in `core/templates/partials/` and
`products/templates/products/partials/`.
