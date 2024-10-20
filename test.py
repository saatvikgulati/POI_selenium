from scraper import *
# get_home_links(url_home)
df = pd.read_csv('all_property_links.csv')
links = df['links'].tolist()
get_area_details(links)