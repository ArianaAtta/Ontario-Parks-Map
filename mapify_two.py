"""
The program below forms a map that displays different Ontario campgrounds
and other information about each park
"""

import folium
import pandas

# Creates lists holding imformation that is taken from the campground_data csv file
campground_data = pandas.read_csv("campground_data.csv")
lat = list(campground_data["LAT"])
lon = list(campground_data["LON"])
name = list(campground_data["CAMP_NAME"])
size = list(campground_data["PARK_SIZE"])
fish = list(campground_data["POP_FISH"])
park_fee = list(campground_data["AVG_FEE"])
rated_cost = list(campground_data["RATED_COST"])
camp_trails = list(campground_data["NUM_OF_TRAILS"])
pic_links = list(campground_data["PIC_URL"])
park_dist = list(campground_data["DIST_FROM_TOWN_CITY"])

# Generates the colors of markers for the first layer based on the campground sizes
def size_color_maker(sizes):
    if sizes < 10:
       return 'red'
    elif 10 <= sizes < 100:
       return 'orange'
    else:
       return 'green'

# Generates the colors of markers for the third layer based on the number of trails at each park
def trail_color_maker(park_trails):
    if park_trails <= 5:
       return 'darkred'
    elif 5 < park_trails < 15:
       return 'orange'
    else:
       return 'darkgreen'

# Generates the colors of markers for the fourth layer based on the cost of the park
def cost_color_maker(prices):
    if prices == 1:
        return 'green'
    elif prices == 2:
        return 'orange'
    else:
        return 'red'

# Generates the colors of markers for the fifth layer based on how secluded the park is
def dist_color_maker(distances):
    if distances <= 31:
        return 'lightred'
    elif 31 < distances < 50:
        return 'beige'
    else:
        return 'lightgreen'

# Creates the text that is used in layer one popup through html as well as inserts the pictures
html_layer_one = """
<b>Campground name:</b> <br>
<em><a href="https://www.google.com/search?q=%%22%s%%22" target="_blank">%s</a></em><br>
<b>Size:</b> <mark>%s</mark> km² <br>
<img src="%s"/>
"""

# Creates the text that is used in layer two popup through html
html_layer_two = """
<b>Campground:</b><em><a href="https://www.google.com/search?q=%%22%s%%22" target="_blank">%s</a></em><br>
<b>Popular Fish:</b><br> %s
"""

# Creates the text that is used in layer three popup through html
html_layer_three = """
<a href="https://www.google.com/search?q=%%22%s%%22" target="_blank">%s</a><br>
has <b><mark> %s</mark></b> hiking and biking trails
"""

# Creates the text that is used in layer four popup through html
html_layer_four = """
The price range to camp at <em><a href="https://www.google.com/search?q=%%22%s%%22" target="_blank">%s</a></em> is:<br>
<mark>%s</mark>
"""

# Creates the text that is used in layer five popup through html
html_layer_five = """
<em><a href="https://www.google.com/search?q=%%22%s%%22" target="_blank">%s</a></em> is:
<b><mark>%s</mark></b> km from the nearest town or city.
"""

# Creates the popup when the user's mouse hovers over a marker
user_mouse = "For more info CLICK ME!"

# Makes a map using folium
map = folium.Map(location=[46.57597255482321, -81.34936184783673], zoom_start=6, tiles="openstreetmap")

# Adds another tile(mode) of the map for the user to use
folium.TileLayer('Stamen Toner', name = 'Black and White Mode').add_to(map)

# Makes the dropdown names in a legend for each layer on the map
fg_one = folium.FeatureGroup(name = "Campground Sizes")
fg_two = folium.FeatureGroup(name = "Fishing Prospects")
fg_three = folium.FeatureGroup(name = "Hiking trails")
fg_four = folium.FeatureGroup(name = "Park Fees")
fg_five = folium.FeatureGroup(name= "Distance from nearest town/city")

# Plots the markers in layer one for the sizes of different campgrounds in Ontario
for lt, ln, siz, nm, lnk in zip(lat, lon, size, name, pic_links):
    iframe = folium.IFrame(html=html_layer_one % (nm, nm, siz, lnk ), width=1000, height=600)
    fg_one.add_child(folium.Marker(location=[lt, ln], popup=folium.Popup(iframe), icon=folium.Icon(color= size_color_maker(siz),icon_color='#054a29', icon="fa-tree", prefix='fa'), tooltip=user_mouse))

# Plots the markers in layer two using information on fishing at each campground
for lt, ln, fsh, nm in zip(lat, lon, fish, name):
    iframe = folium.IFrame(html=html_layer_two % (nm, nm, fsh ), width=325, height=100)
    fg_two.add_child(folium.Marker(location=[lt, ln], popup=folium.Popup(iframe), icon=folium.Icon(color= 'cadetblue', icon = 'tint'), tooltip=user_mouse))

# Plots the markers in layer three showing how many trails each park has
for lt, ln, trails, nm in zip(lat, lon, camp_trails, name):
    iframe = folium.IFrame(html=html_layer_three % (nm, nm, trails ), width=220, height=75)
    fg_three.add_child(folium.Marker(location=[lt, ln], popup=folium.Popup(iframe), icon=folium.Icon(color= trail_color_maker(trails), icon="fa-blind", prefix='fa'), tooltip=user_mouse))

# Plots the markers in layer four presenting the price range of each campground
for lt, ln, cost, nm, ranked_cost in zip(lat, lon, park_fee, name, rated_cost):
    iframe = folium.IFrame(html=html_layer_four % (nm, nm, cost ), width=220, height=90)
    fg_four.add_child(folium.Marker(location=[lt, ln], popup=folium.Popup(iframe), icon=folium.Icon(color= cost_color_maker(ranked_cost), icon="fa-money", prefix='fa'), tooltip=user_mouse))

# Plots the markers in layer five showing how secluded each campground is based on the distance from nearest town/city
for lt, ln, dist, nm, in zip(lat, lon, park_dist, name):
    iframe = folium.IFrame(html=html_layer_five % (nm, nm, dist), width=220, height=90)
    fg_five.add_child(folium.Marker(location=[lt, ln], popup=folium.Popup(iframe), icon=folium.Icon(color= dist_color_maker(dist),icon_color='#050505', icon="road", prefix='fa'), tooltip=user_mouse))

# Adds each feature group/layer to the map and allows the user to turn each on and off
map.add_child(fg_five)
map.add_child(fg_four)
map.add_child(fg_three)
map.add_child(fg_two)
map.add_child(fg_one)
map.add_child(folium.LayerControl())

# Saves the map so it can be opened/viewed
map.save("OntarioParksMap.html")