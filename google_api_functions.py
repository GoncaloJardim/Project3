# -*- coding: utf-8 -*-
"""
Created on Wed Nov  3 15:54:11 2021

@author: crocs
"""

#import libraries:
import time
import pandas as pd
import googlemaps 
import random

#My API_Key:
API_Key = "AIzaSyDpy1uw8_RvkLGFEGEydm1Yon_1fMPIZhM"

#Running googlemaps key:
map_client = googlemaps.Client(API_Key)

#Function to get places:
def get_place_info(location_name):
    try:
        response = map_client.places(query=location_name)
        results = response.get("results")
        return results 

    except:
        print("could not find")
        return None
 
#Ask the user to input a place address or city, searching the input on the get_place_info function:
result_list = get_place_info(input("search for a place/address/city in Portugal: "))


#Function to get the longitude and latitude of the place we chose in result_list:    
def get_latlog(result_list):
    locations_data = []
    lat_log = []
    final_latlog = []
    for information in result_list[0].values():
        locations_data.append(information)
    
    for info_loc in locations_data[2].values():
        lat_log.append(info_loc)
        
    for lat_log_values in lat_log[0].values():
        final_latlog.append(lat_log_values)
    return final_latlog

lati_logi_info = get_latlog(result_list)


"""Next we will Search for restaurants that are in a X meter distance 
from the place we chose, by getting the latitude and longitude from
get_latlog function: """

def restaurants_nearby(lati_logi_info):
    map_client = googlemaps.Client(API_Key)
    lat_log = (lati_logi_info[0],lati_logi_info[1])
    search_string = input("what kind of food would you like to eat there?")
    distance = input("What is your radius distance in meters?")
    while int(distance) > 2000:
            display("Ohh, don't walk that much, choose a distance inferior of 2000 m")
            distance = input("What is your radius distance in meters?")   
    business_list = []

    response = map_client.places_nearby(
    location = lat_log,
    keyword = search_string,
    type = "restaurant",
    radius = distance,
    )

    business_list.extend(response.get("results"))
    next_page_token = response.get("next_page_token")

    while next_page_token:
        time.sleep(random.random()+2)
        response = map_client.places_nearby(
        location = lat_log,
        keyword = search_string,
        type = "restaurant",
        radius = distance,
        page_token = next_page_token
    )
        business_list.extend(response.get("results"))
        next_page_token = response.get("next_page_token")
    
    return business_list

#Display maps_df table:
maps_df = pd.DataFrame(restaurants_nearby(lati_logi_info))
maps_df["url"] = "https://google.com/maps/place/?q=place_id:" + maps_df["place_id"]
display(maps_df)