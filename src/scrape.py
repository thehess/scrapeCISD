# Simple assignment
from bs4.dammit import EncodingDetector
from lxml import etree
from io import StringIO
import requests
import re
import pandas as pd

URL = 'https://www.coppellisd.com/COVID-19Dashboard'
HEADERS = ({'User-Agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
            (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})
TABLEXPATH = '//div[@class = "ui-widget-detail"]/input[@type = "hidden"][1]'
DATEXPATH = '(//em)[1]'

webpage = requests.get(URL, headers=HEADERS)
html_doc = webpage.content
htmlparser = etree.HTMLParser()
html_dom = etree.HTML(html_doc, htmlparser)


raw_tables = []
cleanr = re.compile('<.*?>')

for table_num in range(3):
    raw_tables.append(re.sub(cleanr, '', html_dom.xpath(
        TABLEXPATH)[table_num].get('value')).replace('"', '').replace('[[', '').replace(']]', '').replace('],[', '\n'))

latest_date_object = html_dom.xpath(DATEXPATH)[0]
latest_date = etree.tostring(latest_date_object, encoding='utf-8',
                             method='text').decode().split(': ')[1].split('2021')[0]+'2021'

elem_df = pd.read_csv(StringIO(raw_tables[0]), sep=',')
midl_df = pd.read_csv(StringIO(raw_tables[1]), sep=',')
high_df = pd.read_csv(StringIO(raw_tables[2]), sep=',')

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
final_df['Date'] = latest_date

final_df = final_df[['Date', 'Campuses', 'Grade', 'Cases']]
final_df = final_df.sort_values(by=['Campuses', 'Grade'])
final_df.to_csv('./output/CoppellISDCovid21-22/final.csv', index=False)
print(final_df)
