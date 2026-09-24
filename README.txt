COMPUTATIONAL SCIENCES TALENT HUB
=================================

Ready-to-publish static recruiting website.

FILES
- index.html   Main site
- config.js    Optional Google Sheet live-data connection
- roles.json   Included snapshot of 20 current opportunities
- google_sheet_template.csv   Candidate-safe starter data for a Google Sheet

QUICK PREVIEW
Open index.html in a browser. The page contains an inline fallback copy of all roles, so it works even before hosting.

PUBLISHING
Upload this entire folder to an approved static web host. Examples include an internally approved Roche/Genentech host, GitHub Pages, Netlify, Cloudflare Pages, or similar. Confirm company policy before using an external host for a recruiting page.

OPTIONAL: AUTO-UPDATE FROM GOOGLE SHEETS
1. Create a Google Sheet with these column headers in row 1:
   Job Title | Organization | Location | Requisition ID | URL | Focus
2. Publish that sheet/tab as CSV.
3. Open config.js and paste the published CSV URL into googleSheetCsvUrl.
4. Republish the site. From then on, the site will try to load the sheet each time a visitor opens the page. If the sheet is unavailable, it falls back to the included role data.

NOTE
Publishing a Google Sheet can make its contents accessible to anyone with the published link. Use only candidate-safe fields and follow Roche/Genentech policies.
