from datetime import datetime
import time
import auth_data

from selenium.webdriver import Keys
from selenium.webdriver.support import expected_conditions as EC
from collections import defaultdict
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import pickle
import pandas as pd

def parse(url):
    """
    parse screen values using Selenium library
    :param url: site url
    :return: None

    """
    column_names = ["Round", "Stake", "Win", "Ratio"]
    result = pd.DataFrame(columns=column_names)
    #result = pd.DataFrame()
    last_round_id = 3920000
    current_session_ids = []
    # Open the file in binary read mode
    try:
        with open('./csfail_rounds.pkl', 'rb') as f:
            result = pickle.load(f)
    except:
        pass
    if result.shape[0] != 0:
        last_round_id = result["Round"].max()  # get max last round id
    id = int(last_round_id)
    # Setup Chrome options
    options = webdriver.ChromeOptions()
    #options.add_argument("--headless")  # Ensure GUI is off
    options.add_argument("window-size=1200x600")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--remote-debugging-port=9222")
    options.add_argument("start-url=about:blank")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    options.add_argument("executable_path=/home/kok4444/Study/chromedriver")
    options.add_argument("--log-path=chromedriver.log")

    try:
        # Set path to chromedriver as per your configuration
        webdriver_service = Service(ChromeDriverManager().install())

        driver = webdriver.Chrome(service=webdriver_service, options=options)

        # Navigate to the website
        """
        driver.get("https://csfail.live/en/")
        time.sleep(7)
        login_button = driver.find_element(By.XPATH,
                                           "/html/body/app-root/div/shell-wrapper/div/shell-header/div[3]/users-login-button/button")
        login_button.click()
        time.sleep(2)
        google_button = driver.find_element(By.CLASS_NAME, "button_yandex")
        google_button.click()
        time.sleep(2)
        email_input = driver.find_element(By.ID, "passp-field-login")
        email_input.clear()
        email_input.send_keys(auth_data.yandex_email)
        time.sleep(2)
        yandex_button = driver.find_element(By.CLASS_NAME, "Button2_type_submit")
        yandex_button.click()
        time.sleep(2)

        pass_input = driver.find_element(By.ID, "passp-field-passwd")
        pass_input.clear()
        pass_input.send_keys(auth_data.yandex_password)
        time.sleep(2)
        yandex_button = driver.find_element(By.CLASS_NAME, "Button2_type_submit")
        yandex_button.click()
        """
        while True:
            id += 1
            driver.get(url+"/" + str(id))
            time.sleep(5)

            count = 1

            rounds = driver.find_element(By.CSS_SELECTOR, 'cdk-virtual-scroll-viewport')
            scroll_position_previous = -1
            scroll_position = 0
            count = 1
            while scroll_position != scroll_position_previous:


                seconds = 1
                stop_procedure = False
                while True:
                    try:
                        t = rounds.text
                        break
                    except:
                        time.sleep(seconds)
                        print(f"failed to get round info for {str(id)} seconds: {seconds}")
                        seconds += 1
                        if seconds > 3:
                            stop_procedure = True
                            break       # break while loop
                driver.execute_script("arguments[0].scrollTop = arguments[0].scrollTop + 500;", rounds)
                time.sleep(2)
                scroll_position_previous = scroll_position
                scroll_position = driver.execute_script("return arguments[0].scrollTop;", rounds)
                time.sleep(2)
                #print(f"round {id} scroll {count}: {scroll_position_previous} <> {scroll_position}")
                count += 1
                if stop_procedure:
                    driver.quit()
                    continue

                tokens = t.split("\n")
                prev_ind = 0
                for ind, val in enumerate(tokens):
                    if val == "+1":
                        tokens.pop(ind)
                for ind, val in enumerate(tokens):
                    if val[0] == "X":
                        rec_dict = {}
                        rec_dict["Round"] = int(id)
                        rec_dict["Stake"] = float(tokens[prev_ind])
                        if ind - prev_ind == 2:
                            rec_dict["Win"] = float(tokens[prev_ind + 1])
                        else:
                            rec_dict["Win"] = -float(tokens[prev_ind])
                        rec_dict["Ratio"] = float(tokens[ind][1:])
                        result = result.append(rec_dict, ignore_index=True)
                        prev_ind = ind+1
                result.drop_duplicates(inplace=True)
            try:
                with open('./csfail_rounds.pkl', 'wb') as f:
                    pickle.dump(result, f)
                    print(f"round {id} recorded")
            except:
                pass
    finally:
        driver.quit()

        time.sleep(3)




# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    while True:
        parse('https://csfail.live/en/crash/history')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
