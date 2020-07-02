from selenium import webdriver
import requests
import os
import re
web = input('Enter a bilibili passage:(e.g. "cv2676130"): ')
folder = input('Enter a folder in which you want to storage pictures: ')
if "bilibili" not in web:
    pass
else:
    web = re.findall(r"cv\d+", web)[0]
os.makedirs(folder, exist_ok=True)
os.chdir(folder)
browser = webdriver.Chrome()
browser.get(f"https://www.bilibili.com/read/{web}")
print("Looking through pictures...")
elements = browser.find_elements_by_xpath(f"/html/body/div[2]/div[5]/figure[*]/img")
for element in elements:
    name = element.find_element_by_xpath(".//../figcaption").text
    if name:
        name = re.sub(r"[/\\*?\n\r\t]", "", name)
    else:
        name = f"Picture {elements.index(element)+1}"
    picture = element.get_attribute("data-src").split("@")[0]
    suffix = picture.split(".")[-1]
    with open(f"{name}.{suffix}", "wb") as f:
        print(name)
        f.write(requests.get(f"http:{picture}").content)
    print(f"Picture {elements.index(element)+1} has been downloaded...")
browser.quit()
print("Download process succeeded! :D")