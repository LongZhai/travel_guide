from bs4 import BeautifulSoup
import requests
from operator import itemgetter
import queue as Q
import googlemaps
from datetime import datetime
from gsearch.googlesearch import search
import os, ssl
import sys
import datetime
import google_hotel


'''
displays itinerary details(opening hours and travelling time)
parameter-> list : itinerary_list
            list of dict : places_to_visit
            date : check_in
'''
def itinerary_details(itinerary_list, places_to_visit, check_in):
    for x in itinerary_list:
        week_number = int(check_in.strftime('%w'))
        week_name = check_in.strftime('%A')
        print("------------------------------------")
        print("date(Y, M, D): ", check_in.year, check_in.month, check_in.day, week_name)
        print("------------------------------------")
        check_in = check_in + datetime.timedelta(days=1)
        query_list = []
        for i in x:
            name = places_to_visit[i]['name']
            query_list.append(name)
            print(name)
            try:
                open_time = places_to_visit[i]['periods'][week_number]['open']['time']
                close_time = places_to_visit[i]['periods'][week_number]['close']['time']
            except Exception:
                open_time = '0000'
                close_time = '0000'
            print(" ", week_name, " opens at ", open_time[:2], ":", open_time[2:], "  closes at ", close_time[:2], ":",
                  close_time[2:])
        distance, duration = googel_travel_guide(query_list)
        print("distance between these attractions : ", distance)
        print("the estimated driving time between these attractions : ", duration)



'''
generates a travel itinerary
parameter-> list : places list  
            int : days
return_value-> a list of lists : things to do for each day
'''
def itinerary(dest_list, days):
    itinerary_list = []
    num_dest = len(dest_list)
    visited_place = []
    extra = num_dest % days
    # whether there is same number of places to visit in every day
    if extra == 0:
        places_visit_daily = int(num_dest / days)
        for x in range(num_dest):
            if x not in visited_place:
                nearby_places = find_dest_nearby(dest_list, x, visited_place)[0:places_visit_daily-1]
                places_in_a_day = [x]+[dest_list.index(place[1]) for place in nearby_places]
                visited_place.extend(places_in_a_day)
                itinerary_list.append(places_in_a_day)
                # print("the visit list : ", visited_place)
                # print("the itinerary list : ", itinerary_list)
    else:
        '''this algorithm below does not return the best solution in some special cases, but it can return a good solution
            in most of the time
            If you want to get the best return value, minimal spanning tree is a solution ,but the algorithm's time 
            complexity will grow exponentially
            
        '''
        places_visit_daily = int((num_dest-extra) / days)
        for x in range(num_dest):
            if x not in visited_place:
                nearby_places = find_dest_nearby(dest_list, x, visited_place)[0:places_visit_daily if extra > 0 else places_visit_daily-1]
                places_in_a_day = [x]+[dest_list.index(palce[1]) for palce in nearby_places]
                visited_place.extend(places_in_a_day)
                itinerary_list.append(places_in_a_day)
                extra -= 1
    # print("itinerary_list : ", itinerary_list)
    return itinerary_list


'''
making several attraction subgroups for the travel itinerary
parameter-> list : places list  
            int : list index
            list : places have added to itinerary
return_value-> list : places near each other
'''
def find_dest_nearby(dest_list, index, visited_list):
    lat0 = float(dest_list[index]['geometry']['lat'])
    lng0 = float(dest_list[index]['geometry']['lng'])
    nearby_dest = []
    for x in dest_list:
        ele_position = dest_list.index(x)
        if ele_position != index and ele_position not in visited_list:
            lat = float(x['geometry']['lat'])
            lng = float(x['geometry']['lng'])
            distance = abs(lat0-lat)+abs(lng0-lng)
            nearby_dest.append((distance, x))
    nearby_dest.sort(key=itemgetter(0))
    # print("find nearby func ",nearby_dest)
    return nearby_dest


'''
calculates then perfect hotel location based on geographic positions of tourist attraction
parameter-> list : places list 
return_value-> int tuple : (latitude, longitude)
'''
def find_location_for_hotel(dest_list):
    lat = 0
    lng = 0
    for x in dest_list:
        lat += float(x['geometry']['lat'])
        lng += float(x['geometry']['lng'])
    return lat/len(dest_list), lng/len(dest_list)


'''
deletes places you do not want to visit
parameter-> list : place list 
return_value-> list : modified place list
'''
def modify_list(dest_list):
    while True:
        print("the recommend attraction destinations：")
        for x in dest_list:
            print((dest_list.index(x) + 1), " name : ", x['name'], " website: ", x['website'], " phone number: ", x['phone_number'])
        print("each time input one number and input 0 to exit")
        input_value = int(input("please input a index number to delete the destination you do not want to visit:"))
        if input_value not in range(len(dest_list)+1):
            print("please put a number in range of ", len(dest_list))
            continue
        if input_value == 0:
            break
        else:
            dest_list.pop(input_value - 1)
    return dest_list


'''
finds hotels nearby perfect accommodation location 
(this function prints hotel names without price information)
'''
def find_hotel(lat, lng):
    gmaps = googlemaps.Client(key='AIzaSyCIKt1Y6CFaVVSww_kN7VZSUT6Z2lPKDD4')
    result = gmaps.places(query='hotel toronto ca', location={'lat': lat, 'lng': lng}, radius=5000)
    print("the hotel", result)


'''
finds place details 
parameter-> String : place name 
return_value->  dict : {'name': , 'geometry': , 'periods' : , 'website': , 'phone_number': }
'''
def find_place(query):
    periods = 'None'
    website = 'None'
    phone_number = 'None'
    gmaps = googlemaps.Client(key='AIzaSyCIKt1Y6CFaVVSww_kN7VZSUT6Z2lPKDD4')
    # search the place by its name and return ID and geometry
    result = gmaps.find_place(input=[query], input_type='textquery', fields=['place_id', 'geometry'])
    place_id = result['candidates'][0]['place_id']
    # geometry is a dict which contains lat and lng (geometry = {'lat': 43.6425662, 'lng': -79.3870568})
    geometry = result['candidates'][0]['geometry']['location']
    # search the place's details by its ID
    placeOdetail = gmaps.place(place_id)['result']
    if 'opening_hours' in placeOdetail.keys():
        # periods is a list of dicts {'close': {'day': 0, 'time': '2230'}, 'open': {'day': 0, 'time': '0900'}}
        if 'periods' in placeOdetail['opening_hours'].keys():
            periods = placeOdetail['opening_hours']['periods']
    if 'website' in placeOdetail.keys():
        website = placeOdetail['website']
    if 'international_phone_number' in placeOdetail.keys():
        phone_number = placeOdetail['international_phone_number']
    place_dictionary = {'name': query, 'geometry': geometry, 'periods': periods, 'website': website, 'phone_number': phone_number}
    return place_dictionary

'''
the function returns a distance between a list of tourist attractions, by using google map API to get directions.
(science google API is not for free, the function just uses API once, so the return value is not guaranteed to be
the shortest distance. However, the input list is a sorted list based on approximate distance, so the output is 
close to the shortest path)
parameter-> list : places list 
return_value-> string tuple : (distance, duration)
'''
def googel_travel_guide(places_list):
    gmaps = googlemaps.Client(key='AIzaSyCIKt1Y6CFaVVSww_kN7VZSUT6Z2lPKDD4')
    waypoints = ""
    length = len(places_list)
    if length > 2:
        for x in range(length-2):
            waypoints += "via:" +places_list[x+1] + "|"
    directions = gmaps.directions(origin=places_list[0], destination=places_list[-1],
                                  mode="driving",
                                  waypoints=waypoints[:len(waypoints)-1])
    distace_value = directions[0]['legs'][0]['distance']['text']
    travel_time =  directions[0]['legs'][0]['duration']['text']
    return distace_value, travel_time

'''
opens tripadvisor website and crawls the content to find popular tourist attractions
(annotation: tripadvisor content is messy and it is required to sort and format the information)
parameter-> string : tripadvisor website
return_value-> string list : place names
'''
def tripadvisor(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    news_links = soup.select("a.review_count")
    attraction_list = list()
    # use priority queue to sort places based on popularity
    pri_queue = Q.PriorityQueue()
    for l in news_links:
        t = l.text
        x = [i for i in t if i.isdigit()]
        num = int(''.join(x))
        name = l.parent.parent.find("a").text
        pri_queue.put((-num, name))
    while not pri_queue.empty():
        next_value = pri_queue.get()[1]
        # filter redundant data
        if next_value not in attraction_list:
            attraction_list.append(next_value)
    print("got information from tripadvisor")
    return attraction_list

'''
opens airbnb website and crawl its content to find popular tourist attractions
parameter-> string : airbnb website
return_value-> string list : place names
'''
def airbnb(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    attraction_name = soup.find_all("h3", class_="guidebook-place-card__title")
    attraction_list = []
    for n in attraction_name:
        attraction_list.append(n.text)
    print("got information from airbnb")
    return attraction_list

'''
uses google search API to find tripadvisor and airbnb websites
parameter-> string : airbnb query
            string : tripadvisor query
return_value-> string tuple : (airbnb website, tripadvisor website)
'''
def google_search(query1, query2):
    if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
            getattr(ssl, '_create_unverified_context', None)):
        ssl._create_default_https_context = ssl._create_unverified_context
    search_result1 = search(query1, num_results=1)
    search_result2 = search(query2, num_results=1)
    if len(search_result1)>=1 and len(search_result2)>=1:
        return search_result1[0][1], search_result2[0][1]
    else:
        print("there is a problem with google search API.")
        sys.exit()

'''
truncates tourist attraction lists and merges them together to get a recommendation list
parameter-> int : days
            list : resource from airbnb
            list : resoruce from tripadvisor
return_value-> String list : recommended things_to_do
'''
def things_to_do(days, aribnb, tripadvisor):
    # first half recommended destinations from tripadvisor
    to_do_list = tripadvisor[0:days*2] if len(tripadvisor) >= days*2 else tripadvisor
    # second half recommended destinations from airbnb
    for i in range(len(aribnb)):
        ''' 
        (if aribnb[i] not in to_do_list) does not work when string has both single quote and double quote
         using for loop with if statement to solve the problem 
        '''
        if aribnb[i] not in to_do_list:
            to_do_list.append(aribnb[i])
            if len(to_do_list) >= days*4:
                    break
    # the length of return list depends on travelling days
    return to_do_list


country = input("Enter which country do you want to go: ")
city = input("Enter which city do you want to go: ")
days = int(input("how long are you planning to stay at "+city+"? (how many days) "))
date = input("hotel check in date : (YYY/MM/DD) ")
check_in = datetime.datetime.strptime(date, '%Y/%m/%d')
check_out = check_in+datetime.timedelta(days=days)
checkin_list = list(map(int, date.split('/')))
checkout_list = [check_out.year, check_out.month, check_out.day]
airbnb_query = "things to do in "+city+" "+country+" airbnb"
tripadvisor_query = "things to do in "+city+" "+country+" tripadvisor"
search_results = google_search(airbnb_query, tripadvisor_query)
airbnb_lists = airbnb(search_results[0])
tripadvisor_lists = tripadvisor(search_results[1])
attraction_des = things_to_do(days, airbnb_lists, tripadvisor_lists)
recommand_list = []
for x in attraction_des:
    recommand_list.append(find_place(x+" "+city))
final_plan = modify_list(recommand_list)
hotel_location = find_location_for_hotel(final_plan)
x = google_hotel.google_hotel(' '.join(map(str, hotel_location)))
x.hotel_list(checkin_list,checkout_list)
itinerary_list = itinerary(final_plan, days)
itinerary_details(itinerary_list, final_plan, check_in)
