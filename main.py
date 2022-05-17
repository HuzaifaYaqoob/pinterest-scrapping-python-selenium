
from selenium.webdriver import Chrome 
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
import json
import time

cr_options = ChromeOptions()
cr_options.add_argument("--start-maximized")

#  Input keywords
queries = [
    # 'vegan icecream',
    # 'avocado icecream',
    'python',
    # 'programming',
    # 'javascript',
]
driver = Chrome(executable_path='./chromedriver.exe' , options=cr_options)
all_pins = {}
for query in queries:
    base_url = f'https://www.pinterest.com/search/pins/?q={query}'
    driver.get(base_url)
    time.sleep(1)
    all_elements = driver.find_elements_by_css_selector('[data-test-id="pin"]')
    for elm in all_elements:
        try:
            pin_id = elm.get_attribute('data-test-pin-id')
            hvr_elm = elm.find_element(By.CSS_SELECTOR, '[data-test-id="pincard-image-with-link"]')
            hover = ActionChains(driver).move_to_element(hvr_elm)
            hover.perform()
        except:
            pass
        else:
            try:
                anchor_tag = hvr_elm.find_element(By.TAG_NAME , 'a')
                a_link = anchor_tag.get_attribute('href')
                get_q_obj = all_pins.get(query , None)
                new_obj = {
                    'pin_id' : f'https://www.pinterest.com/pin/{pin_id}/',
                    '_blank_site_link' : a_link
                }
                if get_q_obj:
                    get_q_obj.append(new_obj)
                else:
                    all_pins[query] = [new_obj]
            except:
                pass
try:
    driver.quit()
except:
    pass

with open('output.json' , 'w') as o_file:
    json.dump(all_pins , o_file)