from nonebot import on_command, CommandSession, get_bot
from selenium import webdriver
import selenium.common.exceptions as ex
from selenium.webdriver.chrome.options import Options
import re
from lxml import etree
from asyncio import sleep
option = Options()
option.add_argument("--headless")
prefs = {
    "profile.managed_default_content_settings.images": 2
}
option.add_experimental_option("prefs", prefs)
bot = get_bot()
browser = webdriver.Chrome(chrome_options=option)

@on_command('image', only_to_me=False)
async def image(session: CommandSession):
    picture = session.get('image', prompt='Standing by...')
    if re.findall("CQ:image", session.current_arg):
        pic_name = re.findall("file=.+,", picture)[0].strip("file=").strip(",")
        await bot.get_image(file=pic_name)
        await session.send("Searching now...")
        browser.get("https://saucenao.com/")
        browser.find_element_by_id("file").send_keys(r"C:\Users\Plasmatank\Desktop\Desktop\酷Q Air\data\image\\"+pic_name)
        browser.find_element_by_xpath('//*[@id="Search"]/form/input[2]').click()
        try:
            title = browser.find_elements_by_xpath('//*[@id="middle"]/div[2]/table/tbody/tr/td[2]/div[2]/div[1]/strong')
            creator = browser.find_elements_by_xpath('//*[@id="middle"]/div[*]/table/tbody/tr/td[*]/div[*]/div[*]/a[contains(@href,"pixiv.net/member.php")]')
            similar = browser.find_element_by_xpath('//*[@id="middle"]/div[2]/table/tbody/tr/td[2]/div[1]/div[1]').text
            try:
                pixiv_id = browser.find_element_by_xpath('//*[@id="middle"]/div[*]/table/tbody/tr/td[*]/div[*]/div[*]/strong[contains(text(),"Pixiv ID: ")]')
                pixiv_id_result = pixiv_id.find_element_by_xpath(".//..").text
            except ex.NoSuchElementException:
                pixiv_id_result = "这张图并未在Pixiv上发布..."
            try:
                character = browser.find_element_by_xpath('//*[@id="middle"]/div[*]/table/tbody/tr/td[*]/div[*]/div[*]/strong[contains(text(),"Characters:")]')
                character_result = character.find_element_by_xpath(".//..").text
            except ex.NoSuchElementException:
                character_result = "并未识别到图中的角色..."
            try:
                material = browser.find_element_by_xpath('//*[@id="middle"]/div[*]/table/tbody/tr/td[*]/div[*]/div[*]/strong[contains(text(),"Material:")]')
                material_result = material.find_element_by_xpath(".//..").text
            except ex.NoSuchElementException:
                material_result = "未知"
            twitter = browser.find_elements_by_xpath('//*[@id="middle"]/div[*]/table/tbody/tr/td[*]/div[*]/div[*]/a[contains(@href,"twitter")]')
            if not twitter or pixiv_id_result:
                print(character_result)
                print(material_result)
                print(title)
                print(creator)
                print(pixiv_id_result)
                await session.send(f"{title[0].text if title else ''}\n相似度:{similar}\nPixiv ID:{re.findall('[0-9]+', pixiv_id_result)[0]}\n作者:{creator[0].text if creator else ''}\n{character_result.split(',')[0].replace('Characters:','图中角色:')}\n这是一张{material_result.split(':')[-1].strip(' ') if material_result.split(':')[-1].strip(' ') != 'touhou' else '东方Project'}的作品。")
            else:
                await session.send(f"相似度:{similar}\n作者:{creator[0].text if creator else ''}{twitter[0].text}\n{character_result.split(',')[0].replace('Characters:','图中角色:')}\n这是一张{material_result.split(':')[-1].strip(' ') if material_result.split(':')[-1].strip(' ') != 'touhou' else '东方Project'}的作品。")
        except Exception as Error:
            print(Error)
            await session.send("Not found")

@on_command('history', only_to_me=False)
async def history(session: CommandSession):
    if "today" not in globals():
        browser.get("https://lishishangdejintian.51240.com/")
        page = browser.page_source
        elements, temp = etree.HTML(page), ""
        day = elements.xpath('//*[@id="main_content"]/ul/li[*]/text()')
        happened = elements.xpath('//*[@id="main_content"]/ul/li[*]/a/text()')
        for i, j in zip(day, happened):
            temp += f"{i},{j}\n"
        globals()["today"] = f"历史上的今天:\n{temp}:D"
        await session.send(globals()["today"])
    else:
        await session.send(globals()["today"])

@on_command("百度", only_to_me=False, aliases=("百科", "百毒", "baidu"))
async def du(session: CommandSession):
    browser.get("https://baike.baidu.com/")
    browser.find_element_by_id("query").send_keys(session.current_arg)
    browser.find_element_by_id("search").click()
    page = browser.page_source
    await session.send(re.findall('<meta name="description" content="(.*)">', page)[0] if "百度百科" not in re.findall('<meta name="description" content="(.*)">', page)[0] else "Not found... D:")