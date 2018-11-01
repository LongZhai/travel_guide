# travel_guide
the program generates a perfect travel itinerary for you

It is time-consuming and painstaking to make a travel plan because there are so many factors need to be considered.  The program’s motivation is to make life easier and save people from browsing websites for hours for a trip.

Output: a trip itinerary and recommended hotels

Keys of the project:
Web crawling
Google APIs
selenium

Details:
1: User inputs where he/she wants to go and travel date

2: scraping information from Tripadvisor, which provides traditional tourist attractions,  and Airbnb, which offers must-go places recommended by local guides.

3: based on how many travel days, displaying a limited place list

4: user modify the place list

5: calculating geographic positions of destination for a perfect hotel location which possesses minimal driving time during your trip

6: searching hotels near the estimated hotel location

7: sorting hotels by price and review score to find the great value-for-money hotels (cost performance), and then displaying the top 5

8: subgrouping the destination list (each place in a subgroup near each other) 

9: using these subgroups to make an itinerary

10: displaying the agenda with each place’s opening hours and distance each you have to travel.


output:
Enter which country do you want to go: canada

Enter which city do you want to go: toronto

how long are you planning to stay at toronto? (how many days) 3

hotel check in date : (YYY/MM/DD) 2018/11/11

got information from airbnb

got information from tripadvisor

the recommend attraction destinations：

1  name :  CN Tower toronto  website:  http://www.cntower.ca/  phone number:  +1 416-868-6937

2  name :  Ripley's Aquarium Of Canada toronto  website:  https://www.ripleyaquariums.com/canada/  phone number:  +1 647-351-3474

3  name :  St. Lawrence Market toronto  website:  http://www.stlawrencemarket.com/  phone number:  +1 416-392-7219

4  name :  Royal Ontario Museum toronto  website:  https://www.rom.on.ca/  phone number:  +1 416-586-8000

5  name :  Hockey Hall of Fame toronto  website:  http://www.hhof.com/  phone number:  +1 416-360-7765

6  name :  Royal Alexandra Theatre toronto  website:  https://www.mirvish.com/theatres/royal-alexandra-theatre  phone number:  +1 416-872-1212

7  name :  High Park toronto  website:  http://www.highparktoronto.com/  phone number:  +1 416-338-0338

8  name :  Art Gallery of Ontario toronto  website:  http://www.ago.ca/  phone number:  +1 416-979-6648

9  name :  CF Toronto Eaton Centre website:  https://www.cfshops.com/canada/  phone number:  +1 647-351-3474

10  name :  Rogers Centre toronto  website:  http://www.rogerscentre.com/  phone number:  +1 416-341-1000

11  name :  Kensington Market toronto  website:  http://www.kensington-market.ca/  phone number:  +1 416-323-1924

12  name :  Dundas Square toronto  website:  http://ydsquare.ca/  phone number:  +1 416-979-9960

each time input one number and input 0 to exit

please input a index number to delete the destination you do not want to visit:9

the recommend attraction destinations：

1  name :  CN Tower toronto  website:  http://www.cntower.ca/  phone number:  +1 416-868-6937

2  name :  Ripley's Aquarium Of Canada toronto  website:  https://www.ripleyaquariums.com/canada/  phone number:  +1 647-351-3474

3  name :  St. Lawrence Market toronto  website:  http://www.stlawrencemarket.com/  phone number:  +1 416-392-7219

4  name :  Royal Ontario Museum toronto  website:  https://www.rom.on.ca/  phone number:  +1 416-586-8000

5  name :  Hockey Hall of Fame toronto  website:  http://www.hhof.com/  phone number:  +1 416-360-7765

6  name :  Royal Alexandra Theatre toronto  website:  https://www.mirvish.com/theatres/royal-alexandra-theatre  phone number:  +1 416-872-1212

7  name :  High Park toronto  website:  http://www.highparktoronto.com/  phone number:  +1 416-338-0338

8  name :  Art Gallery of Ontario toronto  website:  http://www.ago.ca/  phone number:  +1 416-979-6648

9  name :  Rogers Centre toronto  website:  http://www.rogerscentre.com/  phone number:  +1 416-341-1000

10  name :  Kensington Market toronto  website:  http://www.kensington-market.ca/  phone number:  +1 416-323-1924

11  name :  Dundas Square toronto  website:  http://ydsquare.ca/  phone number:  +1 416-979-9960

each time input one number and input 0 to exit

please input a index number to delete the destination you do not want to visit:0

----------the hotel recommendation : ----------

name:  The Rex Hotel Jazz and Blues Bar  price:  97.0  review score:  4.4

name:  Canada Suites  price:  171.0  review score:  4.3

name:  Gladstone Hotel  price:  206.0  review score:  4.3

name:  Fairmont Royal York  price:  232.0  review score:  4.4

name:  Bond Place Hotel Toronto  price:  128.0  review score:  3.7

------------------------------------

date(Y, M, D):  2018 11 11 Sunday

------------------------------------

CN Tower toronto

  Sunday  opens at  09 : 00   closes at  22 : 30
  
Ripley's Aquarium Of Canada toronto

  Sunday  opens at  09 : 00   closes at  23 : 00
  
Rogers Centre toronto
  Sunday  opens at  00 : 00   closes at  00 : 00
  
Royal Alexandra Theatre toronto

  Sunday  opens at  00 : 00   closes at  00 : 00
  
distance between these attractions :  2.3 km

the estimated driving time between these attractions :  11 mins

------------------------------------

date(Y, M, D):  2018 11 12 Monday

------------------------------------

St. Lawrence Market toronto

  Monday  opens at  08 : 00   closes at  18 : 00
  
Hockey Hall of Fame toronto

  Monday  opens at  10 : 00   closes at  17 : 00
  
Dundas Square toronto

  Monday  opens at  00 : 00   closes at  00 : 00
  
Art Gallery of Ontario toronto

  Monday  opens at  10 : 30   closes at  17 : 00
  
distance between these attractions :  3.4 km

the estimated driving time between these attractions :  17 mins

------------------------------------

date(Y, M, D):  2018 11 13 Tuesday

------------------------------------

Royal Ontario Museum toronto

  Tuesday  opens at  10 : 00   closes at  17 : 30
  
Kensington Market toronto

  Tuesday  opens at  00 : 00   closes at  00 : 00
  
High Park toronto

  Tuesday  opens at  00 : 00   closes at  00 : 00
  
distance between these attractions :  7.8 km

the estimated driving time between these attractions :  27 mins


Process finished with exit code 0
