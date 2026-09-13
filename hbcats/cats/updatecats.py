from bs4 import BeautifulSoup
from datetime import datetime
from dataclasses import dataclass
import httpx
import json
import logging
import os
import platform
from time import sleep
from typing import Final

from django.db.models import Q, QuerySet
from django.utils import timezone

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.safari.options import Options as SafariOptions
from selenium.common.exceptions import WebDriverException

from cats.models import Cat, CatStatus, UpdateLog

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


@dataclass
class LatestCatInfo:
    name: str
    image_url: str
    image_tag: str
    image_cy: str
    location: str
    birthday: datetime
    intake_date: datetime
    breed: str
    primary_color: str
    sex: str


class UpdateCats:
    ALL_CATS_URL: Final[str] = "https://www.shelterluv.com/embed/5575"
    CAT_DETAILS_URL: Final[str] = "https://www.shelterluv.com/embed/animal/"
    # "https://www.homewardboundcats.org/adopt/"

    def __init__(self):
        self.driver: webdriver.Chrome | webdriver.Safari | None = None

    def get_driver(self, system: str) -> webdriver.Chrome | webdriver.Safari:
        options = None
        driver = None

        if system == "Darwin":
            # options.binary_location = "/usr/local/bin/chromedriver"
            # options.binary_location = "/opt/homebrew/bin/chromium"
            options = SafariOptions()
            options.add_argument("--headless=new")  # Run without a GUI
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            driver = webdriver.Safari(options=options)
        elif system == "Linux":
            # options = wedriver.get_default_chrome_options()
            options = ChromeOptions()
            options.add_argument("--headless")  # Run without a GUI
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")          # Usually unnecessary in headless
            options.add_argument("--disable-extensions")   # Disables background extensions
            options.add_argument("--disable-infobars")
            options.add_argument("--window-size=800,600")  # Smaller window = less pixels to render
            options.add_argument("--blink-settings=imagesEnabled=false") # Don't load images (huge RAM saver)
            options.add_argument("--disable-notifications")      # Stops background notification processes
            options.add_argument("--no-first-run")
            # options.add_argument("--single-process")      # use if needed

            # tell Chrome not to process media or heavy features
            prefs = {
                "profile.managed_default_content_settings.images": 2, # Don't load images
                "disk-cache-size": 0,                                 # Disable disk cache
                "media-cache-size": 0                                 # Disable media cache
            }
            options.add_experimental_option("prefs", prefs)
            service = Service(os.getenv("CHROMEDRIVER_PATH"))
            driver = webdriver.Chrome(service=service, options=options)
        else:
            options = ChromeOptions()
            options.add_argument("--headless")  # Run without a GUI
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            driver = webdriver.Chrome(options=options)

        return driver

    def get_latest_animal_details(self) -> list[LatestCatInfo]:
        # return value
        latest_kats: list[LatestCatInfo] = []

        # get web driver
        driver = self.get_driver(platform.system())
        try:
            driver.implicitly_wait(0.5)
            driver.get(self.ALL_CATS_URL)

            # get initial scroll height
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

            # 1. initialize Beautiful Soup
            soup = BeautifulSoup(driver.page_source, "html.parser")
            # 2. find all the individual item containers
            # These are the divs with the classes "px-2 my-4 w-1/2 md:w-56"
            # Since class names can be long and change, we can target the anchor tag
            # or the inner div if that's more stable. Let's target the inner div:
            item_containers = soup.find_all("div", class_="px-2 my-4 w-1/2 md:w-56")
            if not item_containers:
                logger.warning("No item containers found")
                return latest_kats

            # 3. loop through each container and extract the data
            for container in item_containers:
                # 3a. Extract the Image URL
                # The image is inside the <img> tag
                cat_image_tag = container.find("img")
                cat_image_url = cat_image_tag.get("src") if cat_image_tag else "N/A"
                cat_image_cy = cat_image_tag.get("data-cy") if cat_image_tag else "N/A"
                # 3b. Extract the Name
                # The name is inside the <div> tag right after the image
                name_div = container.find("div", class_="text-center text-gray-500 mt-2")
                # Use get_text(strip=True) to grab the text and remove whitespace
                cat_name = name_div.get_text(strip=True) if name_div else "N/A"
                logger.info(f"Name: {cat_name}")

                cat_details_url = self.get_animal_info_url(cat_image_cy)
                cat_details = self.get_animal_details(cat_details_url)
                cat_location = cat_details.get("location", "N/A")

                cat_birthday_raw = cat_details.get("birthday") or "0"
                cat_birthday = timezone.make_aware(
                    datetime.fromtimestamp(int(cat_birthday_raw))
                )
                cat_intake_date_raw = cat_details.get("intake_date") or "0"
                cat_intake_date = timezone.make_aware(
                    datetime.fromtimestamp(int(cat_intake_date_raw))
                )
                cat_breed=cat_details.get("breed", "N/A")
                cat_primary_color=cat_details.get("primary_color", "N/A")
                cat_sex=cat_details.get("sex", "N/A")

                # 3c. Store the results
                latest_kats.append(LatestCatInfo(
                    name=cat_name,
                    image_url=cat_image_url,
                    image_tag=cat_image_tag,
                    image_cy=cat_image_cy,
                    location=cat_location,
                    birthday=cat_birthday,
                    intake_date=cat_intake_date,
                    breed=cat_breed,
                    primary_color=cat_primary_color,
                    sex=cat_sex,
                ))
        except WebDriverException as e:
            # this catches browser-specific errors (crash, timeout, etc.)
            logger.exception(f"Selenium Error: {str(e)}")
        except Exception as e:
            # this catches non-Selenium Python errors
            logger.exception(f"General Error: {str(e)}")
        finally:
            if driver:
                try:
                    driver.quit() # important
                except:
                    logger.warning("Failed to quit driver", exc_info=True)
                    pass # already closed or crashed

        return latest_kats

    def update_cats(self):
        latest_kats = self.get_latest_animal_details()
        datetime_now = timezone.now()
        logger.info(f"{datetime_now}: Updating cats ...")
        # reset status of all NEW cats to AVAILABLE
        Cat.objects.filter(status=CatStatus.NEW).update(status=CatStatus.AVAILABLE)
        new_cat_count = 0
        total_cats = 0
        for kat in latest_kats:
                # Store the results
                obj = Cat.objects.filter(image_cy=kat.image_cy).first()
                if obj:
                    obj.last_seen = datetime_now
                    # handle if cat was adopted and is now back
                    if obj.status == CatStatus.ADOPTED:
                        new_cat_count += 1
                        obj.status = CatStatus.NEW
                    obj.save()
                else:
                    new_cat_count += 1

                    #logger.info(f"Name: {kat.name} Image: {kat.image_url} Location: {kat.location}")
                    #logger.info(f"Breed: {kat.breed} Primary Color: {kat.primary_color} Sex: {kat.sex}")
                    #logger.info(f"Birthday: {kat.birthday} Intake Date: {kat.intake_date}")
                    #logger.info(f"Image Cy: {kat.image_cy}")

                    logger.info(f"Creating cat: {kat.name}")
                    try:
                        Cat.objects.create(
                            name=kat.name,
                            sex=kat.sex,
                            location=kat.location,
                            birthday=kat.birthday,
                            breed=kat.breed,
                            primary_color=kat.primary_color,
                            intake_date=kat.intake_date,
                            image_url=kat.image_url,
                            image_cy=kat.image_cy,
                            first_seen=datetime_now,
                            last_seen=datetime_now,
                            status=CatStatus.NEW,
                        )
                        logger.info(f"New cat added: {kat.name}")
                    except Exception as e:
                        logger.exception(f"Failed to create cat: {e}")


        # calculate number of cats adopted, cats not seen today and not marked as adopted
        # TODO: THIS LOOKS WRONG
        adopted = Cat.objects.filter(
            ~Q(status=CatStatus.ADOPTED), last_seen__lt=datetime_now
        )
        for cat in adopted:
            cat.status = CatStatus.ADOPTED
            cat.save()
        total_cats = Cat.objects.filter(status__in=[CatStatus.AVAILABLE, CatStatus.NEW]).count()

        logger.info(
            f"Total cats: {total_cats} | New cats added: {new_cat_count} | Adopted cats: {adopted.count()}"
        )
        UpdateLog.objects.create(
            total_cats=total_cats,
            new_cats=new_cat_count,
            adopted_cats=adopted.count(),
            last_updated=datetime_now,
        )
        return {
            "Total": len(latest_kats),
            "New": new_cat_count,
            "Adopted": adopted.count(),
        }

    def get_animal_info_url(self, animal_id):
        return self.CAT_DETAILS_URL + animal_id

    def get_animal_details(self, url):
        # fetch the page
        try:
            with httpx.Client(follow_redirects=True) as client:
                response = client.get(url)
                response.raise_for_status()
            # parse the HTML
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
        cats: QuerySet[Cat] = Cat.objects.all()
        for cat in cats:
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
        return
