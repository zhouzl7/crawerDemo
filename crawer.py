# encoding: utf-8
"""
@author: zhou zelong
@contact: zzl850783164@163.com
@time: 2021/8/6 17:11
@file: crawer.py
@desc: 
"""
from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.ui import Select
import pandas as pd
import time


def run(begin, end):
    # 当测试好能够顺利爬取后，为加快爬取速度可设置无头模式，即不弹出浏览器
    # 添加无头headlesss 1使用chrome headless,2使用PhantomJS
    # 使用 PhantomJS 会警告高不建议使用phantomjs，建议chrome headless
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    browser = webdriver.Chrome()
    browser.maximize_window()  # 最大化窗口,可以选择设置

    browser.get('https://gs.amac.org.cn/amac-infodisc/res/pof/fund/index.html')
    time.sleep(10)
    close_btn = browser.find_element_by_class_name('layui-layer-btn0')
    close_btn.click()
    time.sleep(1)
    s1 = Select(browser.find_element_by_name('fundlist_length'))
    s1.select_by_value('100')
    time.sleep(2)
    lst = []  # 存储为list  1629
    for i in range(begin, end):
        input_page = browser.find_element_by_id('goInput')
        input_page.clear()
        input_page.send_keys(i)
        jump_button = browser.find_element_by_class_name('btn-go')
        jump_button.click()
        time.sleep(2)
        jump_button.click()
        time.sleep(3)
        element = browser.find_element_by_id('fundlist')  # 定位表格，element是WebElement类型
        time.sleep(1)
        # 提取表格内容td
        td_content = element.find_elements_by_tag_name("td")  # 进一步定位到表格内容所在的td节点
        time.sleep(1)
        if len(td_content) == 0:
            continue
        for td in td_content:
            try:
                lst.append(td.text)
            except StaleElementReferenceException:
                lst.append('')
                continue

    # 确定表格列数
    col = 6  # len(element.find_elements_by_css_selector('tr:nth-child(1) td'))
    # 通过定位一行td的数量，可获得表格的列数，然后将list拆分为对应列数的子list
    lst = [lst[i:i + col] for i in range(0, len(lst), col)]

    # list转为dataframe
    columns = ['编号', '基金名称', '私募基金管理人名称', '托管人名称', '成立时间', '备案时间']
    df_table = pd.DataFrame(lst, columns=columns)
    df_table.to_csv('私募基金公示' + str(begin) + '_' + str(end) + '.csv', encoding='utf_8_sig', index=False)
    browser.close()
    time.sleep(2)


if __name__ == '__main__':
    run(1621, 1630)
    # for i in range(201, 1621, 20):
    #     run(i, i+20)
