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
- **Styling:** Tailwind CSS is *not yet* compiled via a standalone CLI script to maintain a lightweight repository.

---

## Setup Instructions

### System Setup

```bash
sudo apt install guvicorn
curl -LsSf https://astral.sh/uv/install.sh | env UV_INSTALL_DIR="$HOME/.local" sh
# sudo snap install astral-uv --classic
sudo apt install chromium-browser chromium-chromedriver
chromium-browser --version
chromedriver --version
```

May have to move uv and uvx from $HOME/.local to $HOME/.local/bin and make sure $HOME/.local/bin in PATH 
or just use snap version


### Django Project Setup

```bash
git clone git@github.com:timarbuckle/homewardbound.git
cd homewardbound
uv sync
uv run hbcats/manage.py collectstatic
```

### Create .env file

### Cloudflare Setup

Install cloudflared service

```bash
curl -fsSL https://pkg.cloudflare.com/cloudflare-main.gpg | sudo tee /usr/share/keyrings/cloudflare-main.gpg >/dev/null
echo 'deb [signed-by=/usr/share/keyrings/cloudflare-main.gpg] https://pkg.cloudflare.com/cloudflared any main' | sudo tee /etc/apt/sources.list.d/cloudflared.list
sudo apt-get update && sudo apt-get install cloudflared
```

Finish configuring on Cloudflare Dashboard

### Setup CRON job
```bash
crontab -e
```
add the following

```
# m h  dom mon dow   command
0 2,14,20 * * * /home/timarbuckle/projects/homewardbound/update_cats.sh >> /home/timarbuckle/projects/homewardbound/update_cats.log 2>&1

# Daylight Saving Time
#0 1,13,19 * * * /home/timarbuckle/projects/homewardbound/update_cats.sh >> /home/timarbuckle/projects/homewardbound/update_cats.log 2>&1
```

### SYSTEMCTL --user setup to replace CRON

CRON updates were unstable so now using this to run updates on a schedule.
* Added 2GB swap to avoid memory problems and no longer need to stop the service before running
* Added cats.service and cats.timer in ~/.config/system/user
* No longer use updatecats.log, check journalctl instead (see below)

Whenever modify these files, need to reload

Reload the configuration

    systemctl --user daemon-reload

Manually run the script

    systemctl --user start cats.service

Check the results

    journalctl --user -u cats.service -f

### DJANGO LOCKDOWN

I am using this to prevent others from accessing the site.
[django-lockdown on PyPi](https://pypi.org/project/django-lockdown/)
