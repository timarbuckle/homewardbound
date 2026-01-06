## Project Roadmap

### Completed Tasks
- [x] **Data Scraping:** Open each cat page (via `src=`) and import:
    * Intake date
    * Age
    * Gender
    * Location
- [x] **Sorting & Filtering:**
    * Sort main page by intake date by default.
    * Added options to sort by age and gender.
- [x] **Reporting:** Integrated the report view.
- [x] **Deployment:** Confirmed site is working at [cats.timarbuckle.com](https://cats.timarbuckle.com).
- [x] **Media Hosting:** Implemented local image serving (migrated away from hotlinking).
- [x] **Dashboard:** Fixed totals and filter logic.
- [x] **Bug Fixes:** Resolved time zone errors occurring during the update process.
- [x] **Automation:** Added a cron job to handle updates on a set schedule.

---

### Implementation Notes
* **Images:** Now served via `MEDIA_ROOT` and optimized through Cloudflare for better performance at the public domain.
* **Environment:** Moved all sensitive credentials to `.env` files to keep the Git history clean.
* **Styling:** Tailwind CSS is now compiled via a standalone CLI script to maintain a lightweight repository.

