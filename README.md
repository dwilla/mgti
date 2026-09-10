# Medical Gas Training Institute — medgasinstitute.com

Static marketing and public-information site for the Medical Gas Training
Institute (MGTI), the certification body for the ASSE Series 6000 medical gas
certifications and the associated ASME Section IX brazing qualification.

## Building

```
python3 build.py
```

`build.py` stamps the shared partials into every page template and writes the
built site to `site/`, which is the only thing published. The output is
assembled from an explicit allow list — the page templates plus the assets named
in `ASSETS` — so nothing else in the repo can reach the public site by accident.
GitHub Actions publishes `site/` via the workflow in `.github/workflows/`.

## Structure

- `src/pages/` — one template per page
- `src/partials/` — `header`, `nav`, `footer`, `banner`, stamped in at build time
  via `<!-- include:name -->` markers
- `shared/` — stylesheet, logo, favicons
- `site/` — build output; regenerate rather than editing

Pages use the Bulma CSS framework and Font Awesome from CDN, with site-specific
styles in `shared/styles.css`.

## Content

The site describes the certifications MGTI administers:

- ASSE 6005 — Medical Gas Systems Generalist
- ASSE 6010 — Medical Gas Systems Installer
- ASSE 6015 — Bulk Medical Gas / Cryogenic Fluid Systems Installer
- ASSE 6020 — Medical Gas Systems Inspector
- ASSE 6030 — Medical Gas Systems Verifier
- ASSE 6035 — Bulk Medical Gas / Cryogenic Fluid Systems Verifier
- ASSE 6040 — Medical Gas Systems Maintenance Personnel
- ASSE 6050 — Medical Gas Systems Instructor
- ASSE 6060 — Medical Gas Systems Designer
- ASME Section IX — Brazing Certification

## Editing content

**Site copy must not contradict MGTI's governing documents.** The *Policies and
Procedures* (MGTI-PP-001) is the source of truth for certification, examination,
and conduct rules; the candidate handbook for each certification is the
candidate-facing statement of them. Two rules bind this repo in particular:

1. **Do not claim accreditation MGTI does not hold.** MGTI is not accredited by
   ANAB, IAS, ANSI, or any other accreditation body. Site copy says MGTI's
   processes are *designed to align with the framework of* ISO/IEC 17024 —
   never *compliant*, *conformant*, *certified to*, or *accredited*.
2. **No prices on this site.** Fees change; medgascerts.com is the single source
   of truth for pricing. Pages may say that a fee applies and link there.

This repository is public. Assume anything committed here is world-readable the
moment it is pushed.
