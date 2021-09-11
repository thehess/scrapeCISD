# Simple assignment
from selenium.webdriver import Safari
import pandas as pd

driver = Safari()
url = 'https://www.coppellisd.com/COVID-19Dashboard'
driver.get(url)

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
