# Simple assignment
from bs4 import BeautifulSoup
from lxml import etree
import requests
import re
import pandas as pd

URL = 'https://www.coppellisd.com/COVID-19Dashboard'
HEADERS = ({'User-Agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
            (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})

webpage = requests.get(URL, headers=HEADERS)
html_doc = webpage.content
htmlparser = etree.HTMLParser()
html_dom = etree.HTML(html_doc, htmlparser)
print(html_dom.xpath(
    '//div[@class = "ui-widget-detail"]/input[@type = "hidden"][1]'))

test = html_dom.xpath(
    '//div[@class = "ui-widget-detail"]/input[@type = "hidden"][1]')

print(test[0].get('value'))

cleanr = re.compile('<.*?>')
cleantext = re.sub(cleanr, '', test[0].get('value'))
print(cleantext)
cleanertext = cleantext.replace('],[', '\n').replace('"', '')
print(cleanertext)


latestDate = driver.find_element_by_xpath(
    "(//em)[1]").text.lstrip('Last Updated On: ').split('\\')[0]
elem_df = pd.read_html(driver.find_element_by_xpath(
    "(//table)[1]").get_attribute('outerHTML'))[0]
midl_df = pd.read_html(driver.find_element_by_xpath(
    "(//table)[2]").get_attribute('outerHTML'))[0]
high_df = pd.read_html(driver.find_element_by_xpath(
    "(//table)[3]").get_attribute('outerHTML'))[0]

elem_df.to_csv('./output/CoppellISDCovid21-22/elem.csv')
midl_df.to_csv('./output/CoppellISDCovid21-22/midl.csv')
high_df.to_csv('./output/CoppellISDCovid21-22/high.csv')

for df in [elem_df, midl_df, high_df]:
    df.rename(columns={df.columns[0]: 'Campuses'}, inplace=True)
    df.drop([df.columns[df.shape[1]-1], df.columns[df.shape[1]-2]],
            axis=1, inplace=True)

elem_df = elem_df.melt(id_vars=["Campuses"],
                       value_vars=["Pre-K", "Kinder", "1st Grade", "2nd Grade", "3rd Grade", "4th Grade", "5th Grade", "Staff"], var_name="Grade", value_name="Cases")

midl_df = midl_df.melt(id_vars=["Campuses"],
                       value_vars=["6th Grade", "7th Grade", "8th Grade", "Staff"], var_name="Grade", value_name="Cases")

high_df = high_df.melt(id_vars=["Campuses"],
                       value_vars=["9th Grade", "10th Grade", "11th Grade", "12th Grade", "Staff"], var_name="Grade", value_name="Cases")

# print(elem_df)
# print(midl_df)
# print(high_df)
final_df = pd.concat([elem_df, midl_df, high_df], ignore_index=True)
final_df['Date'] = latestDate

final_df = final_df[['Date', 'Campuses', 'Grade', 'Cases']]
final_df = final_df.sort_values(by=['Campuses', 'Grade'])
final_df.to_csv('./output/CoppellISDCovid21-22/final.csv', index=False)
print(final_df)

# close browser
driver.quit()
