from datetime import datetime
import time

from selenium.webdriver import Keys
from selenium.webdriver.support import expected_conditions as EC
from collections import defaultdict
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import pickle
import pandas as pd


def grab_history(url):
    """
    parse screen values using Selenium library
    :param url: site url
    :return: None

    """
    column_names = ["Round", "Time", "GrabDate", "Bank", "PersonsNumber", "Ratio"]
    result = pd.DataFrame(columns=column_names)

    try:
        with open('./csfail_history.pkl', 'rb') as f:
            result = pickle.load(f)
    except:
        pass

    # Setup Chrome options
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Ensure GUI is off
    options.add_argument("window-size=1200x600")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--remote-debugging-port=9222")
    options.add_argument("start-url=about:blank")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    options.add_argument("executable_path=/home/kok4444/Study/chromedriver")
    options.add_argument("--log-path=chromedriver.log")



    # Set path to chromedriver as per your configuration
    webdriver_service = Service(ChromeDriverManager().install())

    driver = webdriver.Chrome(service=webdriver_service, options=options)

    # Navigate to the website
    driver.get(url)
    time.sleep(5)


    try:
        body = driver.find_element(By.CLASS_NAME, "cdk-virtual-scroll-content-wrapper")

        # Find all div elements within the body
        divs = body.find_elements(By.XPATH, "//div")
        for div in divs:
            seconds = 1
            stop_procedure = False
            while True:
                try:
                    t = div.text
                    break
                except:
                    time.sleep(seconds)
                    print(f"failed to get history {div} seconds: {seconds}")
                    seconds += 2
                    if seconds > 2:
                        stop_procedure = True
                        break   # break while loop
            if stop_procedure:
                break   # break for loop


            if len(t) > 100:
                tokens = t.split("\n")
                last_recorded_round = 0
                for ind, val in enumerate(tokens):
                    if val[0] == "#":
                        rec_dict = {}
                        rec_dict["Round"] = int(tokens[ind][1:])
                        if last_recorded_round == 0:
                            last_recorded_round = rec_dict["Round"]
                        rec_dict["Ratio"] = float(tokens[ind-4].replace(" ", "")[1:])
                        rec_dict["PersonsNumber"] = int(tokens[ind-3])
                        rec_dict["Bank"] = float(tokens[ind-2])
                        rec_dict["Time"] = tokens[ind-1]
                        rec_dict["GrabDate"] = datetime.now().strftime("%d-%m-%Y")

                        result = result.append(rec_dict, ignore_index=True)
                        result.drop_duplicates(inplace=True)
                        result.sort_values("Round", inplace=True)

                try:
                    with open('./csfail_history.pkl', 'wb') as f:
                        pickle.dump(result, f)
                        print(f"time: {datetime.now()}. Statistics history till round {last_recorded_round} recorded")
                        #time.sleep(100)
                        #driver.refresh()
                        break
                except:
                    pass

    finally:
        driver.quit()



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    while True:
        grab_history('https://csfail.live/en/crash/history')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
