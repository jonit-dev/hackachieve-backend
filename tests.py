places_names = ['Burnaby','Stanley Park','Yaletown','Oakridge']


def generate_places_names_string(places_names):
    if len(places_names) == 3:
        output = ", ".join(places_names)
    elif len(places_names) == 2:
        output = places_names[0] + " and " + places_names[1]
    elif len(places_names) == 1:
        output = places_names[0]
    else:
        output = places_names[0] + ", " + places_names[1] + ", " + places_names[2] + " and more"

    return output


print(generate_places_names_string(places_names))