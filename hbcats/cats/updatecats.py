import json
import logging
import platform
from datetime import datetime
from time import sleep

import httpx
from bs4 import BeautifulSoup
from django.db.models import Q
from django.utils import timezone
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from cats.models import Cat, CatStatus, UpdateLog

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.service import Service as ChromeService
# service = ChromeService(executable_path='/usr/local/bin/chrome-mac-arm64')


class UpdateCats:
    ALL_CATS_URL = "https://www.shelterluv.com/embed/5575"
    CAT_DETAILS_URL = "https://www.shelterluv.com/embed/animal/"

    def __init__(self):
        self.driver = None

    def update_cats(self):
        # reset status of all NEW cats to AVAILABLE
        Cat.objects.filter(status=CatStatus.NEW).update(status=CatStatus.AVAILABLE)

        # driver = webdriver.Safari()
        # driver = webdriver.Chrome()
        # options = wedriver.get_default_chrome_options()

        options = Options()
        if platform.system() == "Darwin":
            # options.binary_location = "/usr/local/bin/chromedriver"
            # options.binary_location = "/opt/homebrew/bin/chromium"
            driver = webdriver.Safari()
        elif platform.system() == "Linux":
            options.binary_location = "/usr/bin/chromium-browser"
            service = Service(executable_path="/usr/bin/chromedriver")
            driver = webdriver.Chrome(service=service, options=options)
        else:
            driver = webdriver.Chrome()
        # options.add_argument("--headless")  # Run without a GUI
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        driver.implicitly_wait(0.5)
        # driver.get("https://www.homewardboundcats.org/adopt/")
        driver.get(self.ALL_CATS_URL)

        # scroll down to load dynamic content

        # Get initial scroll height
        last_height = driver.execute_script("return document.body.scrollHeight")
        scroll_pause_time = 2  # Pause time to let the dynamic content load

        while True:
            # Scroll down to bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # Wait for new content to load
            sleep(scroll_pause_time)
            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("return document.body.scrollHeight")
            # If the heights are the same, you have reached the bottom
            if new_height == last_height:
                break
            # Update the height for the next iteration
            last_height = new_height

        # 1. Initialize Beautiful Soup
        soup = BeautifulSoup(driver.page_source, "html.parser")

        # 2. Find all the individual item containers
        # These are the divs with the classes "px-2 my-4 w-1/2 md:w-56"
        # Since class names can be long and change, we can target the anchor tag
        # or the inner div if that's more stable. Let's target the inner div:
        item_containers = soup.find_all("div", class_="px-2 my-4 w-1/2 md:w-56")
        new_cat_count = 0
        total_cats = 0
        datetime_now = datetime.now()
        # 3. Loop through each container and extract the data
        for container in item_containers:
            total_cats += 1
            # 3a. Extract the Image URL
            # The image is inside the <img> tag
            image_tag = container.find("img")
            image_url = image_tag.get("src") if image_tag else "N/A"
            image_cy = image_tag.get("data-cy") if image_tag else "N/A"
            # 3b. Extract the Name
            # The name is inside the <div> tag right after the image
            name_div = container.find("div", class_="text-center text-gray-500 mt-2")
            # Use get_text(strip=True) to grab the text and remove whitespace
            name = name_div.get_text(strip=True) if name_div else "N/A"

            # Store the results
            obj = Cat.objects.filter(image_cy=image_cy).first()
            if obj:
                obj.last_seen = datetime_now
                # handle if cat was adopted and is now back
                if obj.status == CatStatus.ADOPTED:
                    new_cat_count += 1
                    obj.status = CatStatus.NEW
                obj.save()
            else:
                new_cat_count += 1

                cat_details_url = self.get_animal_info_url(image_cy)
                cat_details = self.get_animal_details(cat_details_url)
                if len(cat_details) == 0:
                    logger.error(f"Failed to fetch details for cat {name}")
                    continue

                cat_birthday_raw = cat_details.get("birthday") or "0"
                cat_birthday = timezone.make_aware(
                    datetime.fromtimestamp(int(cat_birthday_raw))
                )
                cat_intake_date_raw = cat_details.get("intake_date") or "0"
                cat_intake_date = timezone.make_aware(
                    datetime.fromtimestamp(int(cat_intake_date_raw))
                )

                Cat.objects.create(
                    name=name,
                    sex=cat_details.get("sex", "N/A"),
                    location=cat_details.get("location", "N/A"),
                    birthday=cat_birthday,
                    breed=cat_details.get("breed", "N/A"),
                    primary_color=cat_details.get("primary_color", "N/A"),
                    intake_date=cat_intake_date,
                    image_url=image_url,
                    image_cy=image_cy,
                    first_seen=datetime_now,
                    last_seen=datetime_now,
                    status=CatStatus.NEW,
                )
                logger.info(f"New cat added: {name}")

        driver.quit()

        # calculate number of cats adopted, cats not seen today and not marked as adopted
        adopted = Cat.objects.filter(
            ~Q(status=CatStatus.ADOPTED), last_seen__lt=datetime_now
        )
        for cat in adopted:
            cat.status = CatStatus.ADOPTED
            cat.save()

        logger.info(
            f"Total cats: {total_cats}. New cats added: {new_cat_count} Adopted cats: {adopted.count()}"
        )
        UpdateLog.objects.create(
            total_cats=total_cats,
            new_cats=new_cat_count,
            adopted_cats=adopted.count(),
            last_updated=datetime_now,
        )
        return {
            "Total": len(item_containers),
            "New": new_cat_count,
            "Adopted": adopted.count(),
        }

    def get_animal_info_url(self, animal_id):
        return self.CAT_DETAILS_URL + animal_id

    def get_animal_details(self, url):
        # 1. Fetch the page
        try:
            with httpx.Client(follow_redirects=True) as client:
                response = client.get(url)
                response.raise_for_status()
            # 2. Parse the HTML
            soup = BeautifulSoup(response.text, "html.parser")
            tag = soup.find("iframe-animal")
            animal = tag.get(":animal", "{}")
            return json.loads(animal)
        except httpx.HTTPStatusError as exc:
            logger.error(f"Failed to fetch details for URL {url}: {exc}")
            return {}
        except Exception as exc:
            logger.error(f"Unexpected error fetching details for URL {url}: {exc}")
            return {}

    def update_all_cat_details(self):
        cats = Cat.objects.all()
        for cat in cats:
            # Skip cats with known sex, already pulled the data
            if cat.sex != "Unknown":
                continue

            cat_details_url = self.get_animal_info_url(cat.image_cy)
            logger.info(f"Requesting details for cat {cat.name}")
            cat_details = self.get_animal_details(cat_details_url)

            if len(cat_details) == 0:
                logger.warning(f"No details found for cat {cat.name}")
                continue

            cat_birthday_raw = cat_details.get("birthday") or "0"
            cat_birthday = timezone.make_aware(
                datetime.fromtimestamp(int(cat_birthday_raw))
            )
            cat_intake_date_raw = cat_details.get("intake_date") or "0"
            cat_intake_date = timezone.make_aware(
                datetime.fromtimestamp(int(cat_intake_date_raw))
            )
            cat.birthday = cat_birthday
            cat.intake_date = cat_intake_date
            cat.sex = cat_details.get("sex", "")
            cat.location = cat_details.get("location", "")
            cat.breed = cat_details.get("breed", "")
            cat.primary_color = cat_details.get("primary_color", "")
            cat.save()
            logger.info(f"Updated details for cat {cat.name}")
