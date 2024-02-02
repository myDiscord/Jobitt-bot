def load_countries():
    countries = {}
    with open('geo/countries.txt', 'r', encoding='utf-8') as file:
        for line in file:
            if line.startswith('#'):
                continue
            data = line.strip().split('\t')
            country_code = data[0]
            country_name = data[4]
            countries[country_code] = country_name
    return countries


def load_cities():
    cities = {}
    with open('geo/cities.txt', 'r', encoding='utf-8') as file:
        for line in file:
            data = line.strip().split('\t')
            city_name = data[1]
            country_code = data[8]
            if country_code not in cities:
                cities[country_code] = []
            cities[country_code].append(city_name)
    return cities
