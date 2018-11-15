
neighborhoods = {
    "Downtown Vancouver": "is the main or central business district of Vancouver. Major business have their offices and towers located here. Notable and popular entertainment venues and eateries are found here. There is housing in the area. Mostly high-rises and apartments.",
    "West End": " is a mixed commercial and residential area. Housing is a mix of apartments and condos. It is home to the city's gay community, the Davie Village.",
    "Yaletown": "is the heritage area of the city. Formerly home to the city's warehouses, the area has been revitalized with commercial and residential developments. Home to a middle class with a mix of condos and apartments. The area is located along False Creek and the seawall.",
    "Coal Harbor": "is the city's former port area. Like Yaletown, the area has been redeveloped for residences and some business. Home to middle class residents.",
    "Gastown": "is another heritage area of the city. Some streets are still cobblestone. Tourist shops are found near the notable Gastown Steam Clock. The area is mixed with low and middle class residents living in apartments, condos and lofts.",
    "Chinatown": "is where many Chinese immigrants established their homes and businesses when they first moved to Vancouver. Residential areas are home to low income residents in apartments. There are some warehouses still located in the area.",
    "Downtown Eastside": "is a rundown area of the city. It is home to the city's homeless and drug addicted. Low income residents living in early 1900s apartments or hotels.",
    "Crosstown": "is a roughly four-block area that connects Chinatown, Vancouver, Gastown, and Yaletown/Stadium District. Notable landmarks include the historic Sun Tower and a row of heritage high-rise boutique loft conversions.",
    "Arbutus Ridge": "",
    "Dunbar-Southlands": "",
    "False Creek": "",
    "Granville Island/Fairview": "is a tourist area of the city. The notable public market is home to various shops and eateries. An artist haven is found nearby. Housing consists of co-ops, apartments and condos.",
    "South Cambie-Oakridge": "an upper middle class neighbourhood in the centre of the city. Area residents live in detached homes from the 1970s, some are heritage properties. Oakridge Shopping Centre is located in the area.",
    "Kerrisdale": "",
    "Kitsilano": "Arbutus is a beach-side community with a view of English Bay. Mix of homes and shops.",
    "Marpole": "",
    "Oakridge": "",
    "Shaughnessy": "Large detached homes are found here and some are heritage properties from the pre-1950s.",
    "South Cambie": "",
    "West Point Grey": "is a pre-1976 neighbourhood with a some UBC students and local families. The upper middle class to upper class lives here. Some luxury homes are found here.",
    "Commercial Drive": "Grandview is one of Vancouver's multicultural areas. A mix of residential and commercial development in the area.",
    "Grandview-Woodland": "",
    "Hastings-Sunrise": "is another multicultural area of the city. Service sector businesses are located here. Pre-1960 housing found here. It is home to Hastings Park.",
    "Kensington-Cedar Cottage": "is another multicultural enclave of the city. The area has the city's only lake, Trout Lake. A mixed income community with pre-1960 apartments and houses.",
    "Killarney": "",
    "Mount Pleasant": "is a community with mixed residential and business development. Close to False Creek, it has some businesses and warehouses located here. Single and low income residents live here.",
    "Main Street-Riley Park": "is home to the city's vintage and antiques shops, but also a middle class community. Houses and apartments are the main forms of homes. Queen Elizabeth Park is found here as well as the city's highest point.",
    "Renfrew-Collingwood": "",
    "Riley Park-Little Mountain": "",
    "Strathcona": "is home to newer Chinese arrivals to the city.",
    "Sunset": "",
    "Victoria-Fraserview": "",
    "Dunbar": "is close to UBC and home to many students. There are local middle and upper class families. Homes are mixed with rental units.",
    "Kerrisdale": "is a quiet and affluent area of the city with homes built in the 1970s.",
    "Marpole": "is yet another multi-ethnic area of the city. Lower income residents live in affordable or rental units (houses, apartments, divided homes). There are business located in the area.",
    "Sunset-Victoria-Fraserview": "is home to Punjabi residents and restaurants. Some homes are referred to as a Vancouver Special. The area has a view of the Fraser River and mountains. Low rise apartments, houses and rentals are found here.",
    "Renfrew-Killarney": "is a mixed and multicultural neighbourhood. Homes date to the 1970s (row houses, apartments and rentals)."
}

van = City.objects.get(pk=384)

for key, value in neighborhoods.items():
    print("{} => {}".format(key, value))
    # n = Neighborhood(name=key,description=value,city=van)
    # n.save()
