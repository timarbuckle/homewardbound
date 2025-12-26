from selenium import webdriver
from time import sleep
from bs4 import BeautifulSoup
from cats.models import Cat, UpdateLog
import re
from datetime import datetime
import logging

logger = logging.getLogger(__name__)
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.service import Service as ChromeService
# service = ChromeService(executable_path='/usr/local/bin/chrome-mac-arm64')


class UpdateCats:
    def update_cats(self):
        driver = webdriver.Safari()
        driver.implicitly_wait(0.5)
        # driver.get("https://www.homewardboundcats.org/adopt/")
        driver.get("https://www.shelterluv.com/embed/5575")

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

        # print("Finished scrolling and loading all dynamic content.")
        # with open("cats.txt", "w") as f:
        #    f.write(driver.page_source)

        # 1. Initialize Beautiful Soup
        soup = BeautifulSoup(driver.page_source, "html.parser")

        # 2. Find all the individual item containers
        # These are the divs with the classes "px-2 my-4 w-1/2 md:w-56"
        # Since class names can be long and change, we can target the anchor tag
        # or the inner div if that's more stable. Let's target the inner div:
        item_containers = soup.find_all("div", class_="px-2 my-4 w-1/2 md:w-56")
        new_cat_count = 0
        # 3. Loop through each container and extract the data
        for container in item_containers:
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
            try:
                obj = Cat.objects.get(image_cy=image_cy)
                obj.last_seen = datetime.now()
                obj.save()
            except Cat.DoesNotExist:
                new_cat_count += 1
                Cat.objects.create(name=name, image_url=image_url, image_cy=image_cy)

            # print(f"Name: {name}, Image URL: {image_url}, image_cy: {image_cy}")
        driver.quit()
        logger.info(
            f"Total cats: {len(item_containers)}. New cats added: {new_cat_count}"
        )
        UpdateLog.objects.create(
            total_cats=len(item_containers), new_cats=new_cat_count
        )

        # print("Finished scrolling and loading all dynamic content.")
        # with open("cats.txt", "w") as f:
        #    f.write(driver.page_source)

    # not used
    def get_data_v(self, image_tag):
        data_v_pattern = re.compile(r"^data-v-")
        data_v_id = "N/A"
        if image_tag and image_tag.attrs:
            for attr_name in image_tag.attrs:
                # 3. Check if the attribute name matches the pattern
                if data_v_pattern.match(attr_name):
                    # 4. Extract the ID string (e.g., '6333eea1')
                    # We strip the prefix 'data-v-' from the attribute name
                    data_v_id = attr_name.replace("data-v-", "")
                    break  # Exit the loop once the first match is founde(r'^data-v-')
        return data_v_id
