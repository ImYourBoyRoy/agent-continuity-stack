# Discovery validation

## robots.txt

- Confirm the response is plain text and available at the origin root.
- Check environment-specific allow and disallow behavior.
- Ensure sitemap references use the intended canonical origin.
- Remember that robots directives are not access control.

## XML sitemaps

- Validate XML and namespace usage.
- Include canonical, indexable URLs only.
- Use verified modification dates; do not emit build time as content time.
- Split large sitemaps using the applicable search-engine limits.

## Canonical and social metadata

- Resolve URLs absolutely for deployed output.
- Use one canonical URL per page.
- Confirm social images exist, have suitable dimensions, and are public.
- Keep title, description, locale, and content type aligned with the page.

## JSON-LD

- Select schema types that describe visible content.
- Use stable identifiers and canonical URLs.
- Do not invent ratings, prices, authors, legal entities, or contact details.
- Validate syntax and inspect rendered page output.

## security.txt

- Publish at `/.well-known/security.txt`.
- Verify contact ownership, canonical field, language, policy, and expiry.
- Do not publish a personal address without explicit approval.

## llms.txt and AI indexes

- Treat them as optional discovery aids.
- Publish only content already appropriate for public consumption.
- Avoid implying crawler support that has not been verified.

