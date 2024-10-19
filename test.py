from scraper import *
# get_home_links(url_home)
df = pd.read_csv('all_property_links.csv')
get_area_details(df['links'][0])