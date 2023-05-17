from datetime import datetime
import time
from selenium.webdriver.support import expected_conditions as EC
from collections import defaultdict
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import pickle

def parse(url):
    """
    parse screen values using Selenium library
    :param url: site url
    :return: None

    """
    result = defaultdict(list)
    current_session_ids = []
    # Open the file in binary read mode
    try:
        with open('./csfail_history.pkl', 'rb') as f:
            result = pickle.load(f)
    except:
        pass
    print(len(result))
    print(result)
    # Setup Chrome options
    options = webdriver.ChromeOptions()
    #options.add_argument("--headless")  # Ensure GUI is off
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # Set path to chromedriver as per your configuration
    webdriver_service = Service(ChromeDriverManager().install())

    driver = webdriver.Chrome(service=webdriver_service, options=options)

    # Navigate to the website
    driver.get(url)


    #time.sleep(5)

    # Get page title and print it
    print(driver.title)
    try:
        """
        elements = WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".crash-round__ratio.crash-round__ratio_purple"))
        )
        for element in elements:
            print("1:", element.text)
        """
        body = driver.find_element(By.XPATH, "//body")

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

            #print(t[:13], "----", "Authorization", "=== ", t[:13] == "Authorization")
            if len(t) > 13 and t[:13] == "Authorization":
                tokens = t.split("\n")
                for ind, val in enumerate(tokens):
                    if val[0] == "#":
                        result[val[1:]] = [tokens[ind -4], tokens[ind -3], tokens[ind -2], tokens[ind -1], datetime.now().strftime("%d-%m-%Y")]
                        current_session_ids.append(val[1:])
                #print(f"rounds: {result}")



        """
        cuts = WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.XPATH, "//*[contains(@class, 'crash-round__ratio')]"))
        )
        for cut in cuts:
            child_elements = cut.find_elements(By.XPATH, ".//*")
            for child in child_elements:
                print(child.text)
            #print("2:", cut.text)
        """
    finally:
        driver.quit()


    count = 1
    for id in current_session_ids:
        time.sleep(5)
        print(f"{id} is {count} from {len(current_session_ids)} ids to parse")
        if len(result[id]) == 5:

            driver = webdriver.Chrome(service=webdriver_service, options=options)
            driver.get(url+"/" + str(id))
            try:
                """
                elements = WebDriverWait(driver, 20).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".crash-round__ratio.crash-round__ratio_purple"))
                )
                for element in elements:
                    print("1:", element.text)
                """
                body = driver.find_element(By.XPATH, "//body")

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
                            print(f"failed to get round info for {str(id)} seconds: {seconds}")
                            seconds += 1
                            if seconds > 2:
                                stop_procedure = True
                                break       # break while loop
                    if stop_procedure:
                        break           # break for loop


                    # print(t[:13], "----", "Authorization", "=== ", t[:13] == "Authorization")
                    if len(t) > 13 and t[:13] == "Authorization":
                        tokens = t.split("\n")
                        prev_ind = 0
                        for ind, val in enumerate(tokens):
                            if val[0] == "X":
                                result[id].append(tokens[prev_ind:ind])
                                prev_ind = ind
                try:
                    with open('./csfail_history.pkl', 'wb') as f:
                        pickle.dump(result, f)
                except:
                    pass
            finally:
                driver.quit()
        count += 1


    time.sleep(10)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    while True:
        parse('https://csfail.live/en/crash/history')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
