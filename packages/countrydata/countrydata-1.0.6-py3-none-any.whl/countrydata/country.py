from glob import glob
from os.path import isfile, realpath, dirname, join, isdir
import json
from difflib import get_close_matches

class CountryData:
    """To get the available properties of a certain country

    Example:
        country = CountryData('Spain')
        print(country.info())
    """
    def __init__(self, country_name=None):
        """constructor method

        :param country_name: str
            pass country name
        """
        self.country_name = country_name.lower() if country_name else ''
        self.countries = {}  # Initialize self.countries here
        self.country_list = []  # Initialize as an empty list
        
     

        dir_path = dirname(realpath(__file__))
        data_path = join(dir_path, 'data')
        # NOTE: MANIFEST.in may cause package data to be stored under "Data/" instead of "data/" depending on OS
        if not isdir(data_path):
            data_path = join(dir_path, 'Data')

        data_files = join(data_path, 'countries')

        country_files = [files for files in glob(data_files + '/*.json')]
        #print(f"Looking for data files in: {data_path}")
        #print(f"Found these country files: {country_files}")           

        for country_file in country_files:
            if isfile(country_file):
                with open(country_file, encoding='utf-8') as file:
                    country_info = json.load(file)
                    if country_info.get('name', None):
                        country_name_lower = country_info['name'].lower()
                        self.countries[country_name_lower] = country_info
                        self.country_list.append(country_info['name'])
                        if self.country_name in map(lambda an: an.lower(), country_info.get('altSpellings', [])):
                            self.country_name = country_name_lower

        #print("Country Name Received:", country_name)
        #print("Available Country Keys:", list(self.countries.keys()))

    def info(self):
        """Returns all the available information for a specified country.

        :return: dict
        """
        if self.country_name:
            try:
                country = self.countries[self.country_name]
                try:
                    all_info = country
                    return all_info

                except KeyError as k:
                    return (f'There is no data for {self.country_name}')

            except KeyError as e:
                result=get_close_matches(self.country_name, self.country_list,cutoff=0.5 )
                if result != []:
                    return (f"Your given Country {self.country_name} is not available. May be you are looking for these", ', '.join(result)) 
                else:
                    return(f'There is no available country named {self.country_name}')


    def states(self):
        """Returns all available in a  states list

        :return: list
        """
        if self.country_name:
            try:
                country = self.countries[self.country_name]
                try:
                    s=[]
                    states = country['states']
                    for i in states:
                        s.append(i['name'])      
                    
                    if s !=[]:
                        return s
                    else:
                        return (f"Sorry {self.country_name} states doesnot exist :(")

                except KeyError as k:
                    return (f'There is no data for {k} of {self.country_name}')

            except KeyError as e:
                result=get_close_matches(self.country_name, self.country_list,cutoff=0.5 )
                if result != []:
                    return (f"Your given Country {self.country_name} is not available. May be you are looking for these", ', '.join(result)) 
                else:
                    return(f'There is no available country named {self.country_name}') 

    def cities(self):
        """Returns all available cities in a list

        :return: list
        """
        if self.country_name:
            try:
                country = self.countries[self.country_name]
                try:
                    c=[]
                    cities = country['states']
                    for i in cities:
                        for j in i['cities']:
                            c.append(j['name']) 
                    if c !=[]:
                        return c 
                    else:
                        return (f"Sorry {self.country_name} cities doesnot exist :(")

                except KeyError as k:
                    return (f'There is no data for cities of {self.country_name}')

            except KeyError as e:
                result=get_close_matches(self.country_name, self.country_list,cutoff=0.5 )
                if result != []:
                    return (f"Your given Country {self.country_name} is not available. May be you are looking for these", ', '.join(result)) 
                else:
                    return(f'There is no available country named {self.country_name}')
                return (f'There is no data for {e} of {self.country_name}')        

    def states_and_cities(self):
        """Returns states and cities in a dict

        :return: dict
        """
        if self.country_name:
            try:
                country = self.countries[self.country_name]
                try:
                    states_and_cities = country['states']
                    if states_and_cities != {}:
                        return states_and_cities
                    else:
                        return (f"Sorry {self.country_name} states_and_cities doesnot exist :(")

                except KeyError as k:
                    return (f'There is no data for states and cities of {self.country_name}')

            except KeyError as e:
                result=get_close_matches(self.country_name, self.country_list,cutoff=0.5 )
                if result != []:
                    return (f"Your given Country {self.country_name} is not available. May be you are looking for these", ', '.join(result)) 
                else:
                    return(f'There is no available country named {self.country_name}')
                return (f'There is no data for {e} of {self.country_name}') 

    def iso(self, alpha=None):
        """Returns ISO codes for a specified country

        :param alpha: int

        :return: dict
            based on param
        """
        if self.country_name:
            try:
                country = self.countries[self.country_name]
                try:
                    iso = country['ISO']
                    if iso != {}:
                        return iso
                    else:
                        return (f"Sorry {self.country_name} ISO doesnot exist :(")

                except KeyError as k:
                    return (f'There is no data for {k} of {self.country_name}')

            except KeyError as e:
                result=get_close_matches(self.country_name, self.country_list,cutoff=0.5 )
                if result != []:
                    return (f"Your given Country {self.country_name} is not available. May be you are looking for these", ', '.join(result)) 
                else:
                    return(f'There is no available country named {self.country_name}') 

    def alt_spellings(self):
        """Returns alternate spellings for the name of a specified country

        :return: list
        """
        if self.country_name:
            try:
                country = self.countries[self.country_name]
                try:
                    alt = country['altSpellings']
                    if alt != []:
                        return alt
                    else:
                        return (f"Sorry {self.country_name} alternate spellings doesnot exist :(")

                except KeyError as k:
                    return (f'There is no data for {k} of {self.country_name}')

            except KeyError as e:
                result=get_close_matches(self.country_name, self.country_list,cutoff=0.5 )
                if result != []:
                    return (f"Your given Country {self.country_name} is not available. May be you are looking for these", ', '.join(result)) 
                else:
                    return(f'There is no available country named {self.country_name}')
                

    def area(self):
        """Returns area (km²) for a specified country

        :return: int
        """
        if self.country_name:
            try:
                country = self.countries[self.country_name]
                try:
                    area = country['area']
                    if area != '':
                        return area
                    else:
                        return (f"Sorry {self.country_name} area doesnot exist :(")

                except KeyError as k:
                    return (f'There is no data for {k} of {self.country_name}')

            except KeyError as e:
                result=get_close_matches(self.country_name, self.country_list,cutoff=0.5 )
                if result != []:
                    return (f"Your given Country {self.country_name} is not available. May be you are looking for these", ', '.join(result)) 
                else:
                    return(f'There is no available country named {self.country_name}') 

    def borders(self):
        """Returns bordering countries (ISO3) for a specified country

        :return: list
        """
        if self.country_name:
            try:
                country = self.countries[self.country_name]
                try:
                    borders = country['borders']
                    if borders != []:
                        return borders
                    else:
                        return (f"Sorry {self.country_name} borders doesnot exist :(")

                except KeyError as k:
                    return (f'There is no data for {k} of {self.country_name}')

            except KeyError as e:
                result=get_close_matches(self.country_name, self.country_list,cutoff=0.5 )
                if result != []:
                    return (f"Your given Country {self.country_name} is not available. May be you are looking for these", ', '.join(result)) 
                else:
                    return(f'There is no available country named {self.country_name}')

    def calling_codes(self):
        """Returns international calling codes for a specified country

        :return: list
        """
        if self.country_name:
            try:
                country = self.countries[self.country_name]
                try:
                    call = country['callingCodes']
                    if call != []:
                        return call
                    else:
                        return (f"Sorry {self.country_name} calling codes doesnot exist :(")

                except KeyError as k:
                    return (f'There is no data for {k} of {self.country_name}')

            except KeyError as e:
                result=get_close_matches(self.country_name, self.country_list,cutoff=0.5 )
                if result != []:
                    return (f"Your given Country {self.country_name} is not available. May be you are looking for these", ', '.join(result)) 
                else:
                    return(f'There is no available country named {self.country_name}')

    def capital(self):
        """Returns capital city for a specified country

        :return: str
        """
        if self.country_name:
            try:
                country = self.countries[self.country_name]
                try:
                    capital = country['capital']
                    if capital != '':
                        return capital
                    else:
                        return (f"Sorry {self.country_name} capital doesnot exist :(")

                except KeyError as k:
                    return (f'There is no data for {k} of {self.country_name}')

            except KeyError as e:
                result=get_close_matches(self.country_name, self.country_list,cutoff=0.5 )
                if result != []:
                    return (f"Your given Country {self.country_name} is not available. May be you are looking for these", ', '.join(result)) 
                else:
                    return(f'There is no available country named {self.country_name}')

    def independence(self):
            """Returns independence year for a specified country

            :return: int
            """
            if self.country_name:
                try:
                    country = self.countries[self.country_name]
                    try:
                        independence = country['independence']
                        if independence != '':
                            return independence
                        else:
                            return (f"Sorry {self.country_name} independence doesnot exist :(")

                    except KeyError as k:
                        return (f'There is no data for {k} of {self.country_name}')

                except KeyError as e:
                    result=get_close_matches(self.country_name, self.country_list,cutoff=0.5 )
                    if result != []:
                        return (f"Your given Country {self.country_name} is not available. May be you are looking for these", ', '.join(result)) 
                    else:
                        return(f'There is no available country named {self.country_name}')



    def capital_latlng(self):
        """Returns capital city latitude and longitude for a specified country

        :return: str
        """
        if self.country_name:
            try:
                country = self.countries[self.country_name]
                try:
                    capital_latlng = country['capital_latlng']
                    if capital_latlng != []:
                        return capital_latlng
                    else:
                        return (f"Sorry {self.country_name} capital latitude and longitude doesnot exist :(")

                except KeyError as k:
                    return (f'There is no data for {k} of {self.country_name}')

            except KeyError as e:
                result=get_close_matches(self.country_name, self.country_list,cutoff=0.5 )
                if result != []:
                    return (f"Your given Country {self.country_name} is not available. May be you are looking for these", ', '.join(result)) 
                else:
                    return(f'There is no available country named {self.country_name}')

    def currency(self):
        """Returns official currency for a specified country

        :return: list
        """
        if self.country_name:
            try:
                country = self.countries[self.country_name]
                try:
                    currency = country['currencies']
                    if currency != []:
                        return currency
                    else:
                        return (f"Sorry {self.country_name} currency doesnot exist :(")

                except KeyError as k:
                    return (f'There is no data for {k} of {self.country_name}')

            except KeyError as e:
                result=get_close_matches(self.country_name, self.country_list,cutoff=0.5 )
                if result != []:
                    return (f"Your given Country {self.country_name} is not available. May be you are looking for these", ', '.join(result)) 
                else:
                    return(f'There is no available country named {self.country_name}')

    def demonym(self):
        """Returns the demonyms for a specified country

        :return: str
        """
        if self.country_name:
            try:
                country = self.countries[self.country_name]
                try:
                    demonym = country['demonym']
                    if demonym != '':
                        return demonym
                    else:
                        return f"Sorry, {self.country_name} demonym does not exist :("

                except KeyError as k:
                    return f'There is no data for {k} of {self.country_name}'

            except KeyError as e:
                result = get_close_matches(self.country_name, self.country_list, cutoff=0.6)
                if result:
                    return f"Your given Country {self.country_name} is not available. Maybe you are looking for these: {', '.join(result)}"
                else:
                    return f'There is no available country named {self.country_name}'
        else:
            return "No country name provided"

    def flag(self):
        """Returns SVG link of the official flag for a specified country

        :return: str
            it will return an URL if available
        """
        if self.country_name:
            try:
                country = self.countries[self.country_name]
                try:
                    flag = country['flag']
                    if flag != '':
                        return flag
                    else:
                        return (f"Sorry there is no link for {self.country_name} :(")

                except KeyError as k:
                    return (f'There is no data for {k} of {self.country_name}')

            except KeyError as e:
                result=get_close_matches(self.country_name, self.country_list,cutoff=0.5 )
                if result != []:
                    return (f"Your given Country {self.country_name} is not available. May be you are looking for these", ', '.join(result)) 
                else:
                    return(f'There is no available country named {self.country_name}')

    def geo_json(self):
        """Returns geoJSON for a specified country

        :return: dict
        """
        if self.country_name:
            try:
                country = self.countries[self.country_name]
                try:
                    geoJSON = country['geoJSON']
                    if geoJSON != {}:
                        return geoJSON
                    else:
                        return (f"Sorry {self.country_name} geoJSON doesnot exist :(")

                except KeyError as k:
                    return (f'There is no data for {k} of {self.country_name}')

            except KeyError as e:
                result=get_close_matches(self.country_name, self.country_list,cutoff=0.5 )
                if result != []:
                    return (f"Your given Country {self.country_name} is not available. May be you are looking for these", ', '.join(result)) 
                else:
                    return(f'There is no available country named {self.country_name}')

    def languages(self):
        """Returns all spoken languages for a specified country

        :return: list
        """
        if self.country_name:
            try:
                country = self.countries[self.country_name]
                try:
                    lang = country['languages']
                    if lang != []:
                        return lang
                    else:
                        return (f"Sorry {self.country_name} languages doesnot exist :(")

                except KeyError as k:
                    return (f'There is no data for {k} of {self.country_name}')

            except KeyError as e:
                result=get_close_matches(self.country_name, self.country_list,cutoff=0.5 )
                if result != []:
                    return (f"Your given Country {self.country_name} is not available. May be you are looking for these", ', '.join(result)) 
                else:
                    return(f'There is no available country named {self.country_name}')

    def latlng(self):
        """Returns approx latitude and longitude for a specified country

        :return: list
        """
        if self.country_name:
            try:
                country = self.countries[self.country_name]
                try:
                    latlng = country['latlng']
                    if latlng != []:
                        return latlng
                    else:
                        return (f"Sorry {self.country_name} latitude and longitude doesnot exist :(")

                except KeyError as k:
                    return (f'There is no data for {k} of {self.country_name}')

            except KeyError as e:
                result=get_close_matches(self.country_name, self.country_list,cutoff=0.5 )
                if result != []:
                    return (f"Your given Country {self.country_name} is not available. May be you are looking for these", ', '.join(result)) 
                else:
                    return(f'There is no available country named {self.country_name}')

    def name(self):
        """ Returns the english name of the country as registered in the library
        :return: str
        """
        if self.country_name:
            try:
                country = self.countries[self.country_name]
                try:
                    name = country['name']
                    if name != '':
                        return name
                    else:
                        return (f"Sorry {self.country_name} name doesnot exist :(")

                except KeyError as k:
                    return (f'There is no data for {k} of {self.country_name}')

            except KeyError as e:
                result=get_close_matches(self.country_name, self.country_list,cutoff=0.5 )
                if result != []:
                    return (f"Your given Country {self.country_name} is not available. May be you are looking for these", ', '.join(result)) 
                else:
                    return(f'There is no available country named {self.country_name}')

    def native_name(self):
        """ Returns the name of the country in its native tongue

        :return: str
        """
        if self.country_name:
            try:
                country = self.countries[self.country_name]
                try:
                    nativeName = country['nativeName']
                    if nativeName != '':
                        return nativeName
                    else:
                        return (f"Sorry {self.country_name} native name doesnot exist :(")

                except KeyError as k:
                    return (f'There is no data for {k} of {self.country_name}')

            except KeyError as e:
                result=get_close_matches(self.country_name, self.country_list,cutoff=0.5 )
                if result != []:
                    return (f"Your given Country {self.country_name} is not available. May be you are looking for these", ', '.join(result)) 
                else:
                    return(f'There is no available country named {self.country_name}')

    def population(self):
        """Returns population for a specified country

        :return: int
        """
        if self.country_name:
            try:
                country = self.countries[self.country_name]
                try:
                    population = country['population']
                    if population != '':
                        return population
                    else:
                        return (f"Sorry {self.country_name} population doesnot exist :(")

                except KeyError as k:
                    return (f'There is no data for {k} of {self.country_name}')

            except KeyError as e:
                result=get_close_matches(self.country_name, self.country_list,cutoff=0.5 )
                if result != []:
                    return (f"Your given Country {self.country_name} is not available. May be you are looking for these", ', '.join(result)) 
                else:
                    return(f'There is no available country named {self.country_name}')

    def timezones(self):
        """Returns all timezones for a specified country

        :return: list
        """
        if self.country_name:
            try:
                country = self.countries[self.country_name]
                try:
                    time = country['timezones']
                    if time != []:
                        return time
                    else:
                        return (f"Sorry {self.country_name} time zones doesnot exist :(")

                except KeyError as k:
                    return (f'There is no data for {k} of {self.country_name}')

            except KeyError as e:
                result=get_close_matches(self.country_name, self.country_list,cutoff=0.5 )
                if result != []:
                    return (f"Your given Country {self.country_name} is not available. May be you are looking for these", ', '.join(result)) 
                else:
                    return(f'There is no available country named {self.country_name}') 

    def tld(self):
        """Returns official top level domains for a specified country

        :return: list
        """
        if self.country_name:
            try:
                country = self.countries[self.country_name]
                try:
                    tld = country['tld']
                    if tld != []:
                        return tld
                    else:
                        return (f"Sorry {self.country_name} domain extensions doesnot exist :(")

                except KeyError as k:
                    return (f'There is no data for {k} of {self.country_name}')

            except KeyError as e:
                result=get_close_matches(self.country_name, self.country_list,cutoff=0.5 )
                if result != []:
                    return (f"Your given Country {self.country_name} is not available. May be you are looking for these", ', '.join(result)) 
                else:
                    return(f'There is no available country named {self.country_name}') 

    def translations(self):
        """Returns translations for a specified country name in popular languages

        :return: dict
        """
        if self.country_name:
            try:
                country = self.countries[self.country_name]
                try:
                    translations = country['translations']
                    if translations != {}:
                        return translations
                    else:
                        return (f"Sorry {self.country_name} translations doesnot exist :(")

                except KeyError as k:
                    return (f'There is no data for {k} of {self.country_name}')

            except KeyError as e:
                result=get_close_matches(self.country_name, self.country_list,cutoff=0.5 )
                if result != []:
                    return (f"Your given Country {self.country_name} is not available. May be you are looking for these", ', '.join(result)) 
                else:
                    return(f'There is no available country named {self.country_name}') 

    def continent(self):
        """Returns continent for a specified country

        :return: str
        """
        if self.country_name:
            try:
                country = self.countries[self.country_name]
                try:
                    continent = country['continent']
                    if continent != '':
                        return continent
                    else:
                        return (f"Sorry {self.country_name} continent doesnot exist :(")

                except KeyError as k:
                    return (f'There is no data for {k} of {self.country_name}')

            except KeyError as e:
                result=get_close_matches(self.country_name, self.country_list,cutoff=0.5 )
                if result != []:
                    return (f"Your given Country {self.country_name} is not available. May be you are looking for these", ', '.join(result)) 
                else:
                    return(f'There is no available country named {self.country_name}')

    def government(self):
        """Returns type of Government for a specified country

        :return: str
        """
        if self.country_name:
            try:
                country = self.countries[self.country_name]
                try:
                    govt = country['government']
                    if govt != '':
                        return govt
                    else:
                        return (f"Sorry {self.country_name} government doesnot exist :(")

                except KeyError as k:
                    return (f'There is no data for {k} of {self.country_name}')

            except KeyError as e:
                result=get_close_matches(self.country_name, self.country_list,cutoff=0.5 )
                if result != []:
                    return (f"Your given Country {self.country_name} is not available. May be you are looking for these", ', '.join(result)) 
                else:
                    return(f'There is no available country named {self.country_name}')


    def temperature(self):
        """Returns average temperature of a specified country in celsius

        :return: number
        """
        if self.country_name:
            try:
                country = self.countries[self.country_name]
                try:
                    temp = country['temperature']
                    if temp != '':
                        return temp
                    else:
                        return (f"Sorry {self.country_name} average temperature doesnot exist :(")

                except KeyError as k:
                    return (f'There is no data for {k} of {self.country_name}')

            except KeyError as e:
                result=get_close_matches(self.country_name, self.country_list,cutoff=0.5 )
                if result != []:
                    return (f"Your given Country {self.country_name} is not available. May be you are looking for these", ', '.join(result)) 
                else:
                    return(f'There is no available country named {self.country_name}')

    def expectancy(self):
        """Returns life expectancy of a specified country

        :return: number
        """
        if self.country_name:
            try:
                country = self.countries[self.country_name]
                try:
                    life = country['expectancy']
                    if life != '':
                        return life
                    else:
                        return (f"Sorry {self.country_name} average expectancy doesnot exist :(")

                except KeyError as k:
                    return (f'There is no data for {k} of {self.country_name}')

            except KeyError as e:
                result=get_close_matches(self.country_name, self.country_list,cutoff=0.5 )
                if result != []:
                    return (f"Your given Country {self.country_name} is not available. May be you are looking for these", ', '.join(result)) 
                else:
                    return(f'There is no available country named {self.country_name}')
    
    def dish(self):
        """Returns national dish of a specified country

        :return: str
        """
        if self.country_name:
            try:
                country = self.countries[self.country_name]
                try:
                    dish = country['dish']
                    if dish != '':
                        return dish
                    else:
                        return (f"Sorry {self.country_name} national dish doesnot exist :(")

                except KeyError as k:
                    return (f'There is no data for {k} of {self.country_name}')

            except KeyError as e:
                result=get_close_matches(self.country_name, self.country_list,cutoff=0.5 )
                if result != []:
                    return (f"Your given Country {self.country_name} is not available. May be you are looking for these", ', '.join(result)) 
                else:
                    return(f'There is no available country named {self.country_name}')
     
    def symbol(self):
        """Returns national symbol of a specified country

        :return: str
        """
        if self.country_name:
            try:
                country = self.countries[self.country_name]
                try:
                    symbol = country['symbol']
                    if symbol != '':
                        return symbol
                    else:
                        return (f"Sorry {self.country_name} national symbol doesnot exist :(")

                except KeyError as k:
                    return (f'There is no data for {k} of {self.country_name}')
            
            except KeyError as e:
                result=get_close_matches(self.country_name, self.country_list,cutoff=0.5 )
                if result != []:
                    return (f"Your given Country {self.country_name} is not available. May be you are looking for these", ', '.join(result)) 
                else:
                    return(f'There is no available country named {self.country_name}')
                
    
    def density(self):
        """Returns national symbol of a specified country

        :return: str
        """
        if self.country_name:
            try:
                country = self.countries[self.country_name]
                try:
                    density = country['density']
                    if density != '':
                        return density
                    else:
                        return (f"Sorry {self.country_name} density doesnot exist :(")

                except KeyError as k:
                    return (f'There is no data for {k} of {self.country_name}')

            except KeyError as e:
                result=get_close_matches(self.country_name, self.country_list,cutoff=0.5 )
                if result != []:
                    return (f"Your given Country {self.country_name} is not available. May be you are looking for these", ', '.join(result)) 
                else:
                    return(f'There is no available country named {self.country_name}')
       
    def region(self):
        """Returns the region of a specified country

        :return: str
        """
        if self.country_name:
            try:
                country = self.countries[self.country_name]
                try:
                    region = country['location']
                    if region != '':
                        return region
                    else:
                        return (f"Sorry {self.country_name} region doesnot exist :(")

                except KeyError as k:
                    return (f'There is no data for region of {self.country_name}')

            except KeyError as e:
                result=get_close_matches(self.country_name, self.country_list,cutoff=0.5 )
                if result != []:
                    return (f"Your given Country {self.country_name} is not available. May be you are looking for these", ', '.join(result)) 
                
                else:
                    return (f"There is no available country named {self.country_name}") 
    
    def religion(self):
        """Returns religion of a specified country

        :return: str
        """
        if self.country_name:
            try:
                country = self.countries[self.country_name]
                try:
                    religion = country['religion']
                    if religion != '':
                        return religion
                    else:
                        return (f"Sorry {self.country_name} religion doesnot exist :(")
        
                except KeyError as k:
                        return (f'There is no data for {k} of {self.country_name}') 
            except:
                result=get_close_matches(self.country_name, self.country_list,cutoff=0.5 )
                if result != []:
                    return (f"Your given Country {self.country_name} is not available. May be you are looking for these", ', '.join(result)) 
                
                else:
                    return (f"There is no available country named {self.country_name}") 
                    
        
    def total_states(self):
        if self.country_name:
            total_states = self.countries[self.country_name]['states']
            return(len(total_states))

    def total_cities(self):
        if self.country_name:
            cities_count=0
            total_cities = self.countries[self.country_name]['states']
            for i in total_cities:
                cities_count = len(i['cities']) + cities_count
            return cities_count

    def wiki(self):
            """Returns link to wikipedia page for a specified country

            :return: str
                return wiki url if available
            """
            try:
                if self.country_name:
                    _wiki = self.countries[self.country_name]['wiki']
                    return _wiki

            except KeyError as e:
                if e == self.country_name:
                    result=get_close_matches(self.country_name, self.country_list,cutoff=0.5 )
                    if result != []:
                        return (f"Your given Country {self.country_name} is not available. May be you are looking for these", ', '.join(result)) 
                    
                    else:
                        return (f"There is no available country named {self.country_name}") 
                else:
                    return (f'There is no data for {e} of {self.country_name}') 

    def all(self):
        """return all of the countries information

        :return: dict
        """
        _all = self.countries

        return _all


if __name__ == '__main__':
    country = CountryData('Spain')
    print(country.info())

