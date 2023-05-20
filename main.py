import grab_history
import grab_rounds_with_persons
if __name__ == '__main__':
    while True:
        try:
            grab_history.grab_history('https://csfail.live/en/crash/history')
            grab_rounds_with_persons.grab_rounds_with_persons('https://csfail.live/en/crash/history')
        except:
            continue


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
