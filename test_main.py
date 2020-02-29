from jokeapi import Jokes

j = Jokes()
errors = []

try:
    j.get_joke()
except Exception as e:
    errors.append({'Error in':  'blank joke get',  'Error': e})

"""Testing for errors in categories"""
try:
    j.get_joke(category=["programming"])
except Exception as e:
    errors.append({'Error in':  'category programming', 'Error': e})
try:
    j.get_joke(category=["miscellaneous"])
except Exception as e:
    errors.append({'Error in':  'category miscellaneous', 'Error': e})
try:
    j.get_joke(category=["dark"])
except Exception as e:
    errors.append({'Error in':  'category dark', 'Error': e})

"""Testing for errors in blacklist"""
try:
    j.get_joke(blacklist=["nsfw"])
except Exception as e:
    errors.append({'Error in':  'blacklist nsfw', 'Error': e})
try:
    j.get_joke(blacklist=["religious"])
except Exception as e:
    errors.append({'Error in':  'blacklist religious', 'Error': e})
try:
    j.get_joke(blacklist=["political"])
except Exception as e:
    errors.append({'Error in':  'blacklist political', 'Error': e})
try:
    j.get_joke(blacklist=["racist"])
except Exception as e:
    errors.append({'Error in':  'blacklist political', 'Error': e})
try:
    j.get_joke(blacklist=["sexist"])
except Exception as e:
    errors.append({'Error in':  'blacklist sexist',  'Error': e})

"""Testing for errors in response_format"""
try:
    j.get_joke(response_format="xml")
except Exception as e:
    errors.append({'Error in':  'response_format xml', 'Error': e})
try:
    j.get_joke(response_format="yaml")
except Exception as e:
    errors.append({'Error in':  'response_format yaml', 'Error': e})

"""Testing for errors in type"""
try:
    j.get_joke(type="single")
except Exception as e:
    errors.append({'Error in':  'type single', 'Error': e})
try:
    j.get_joke(type="twopart")
except Exception as e:
    errors.append({'Error in':  'type double', 'Error': e})

"""Testing for errors in search_string"""
try:
    j.get_joke(search_string="search")
    # as long as this gets a response, the api wrapper is fine;
    # it probably doesn't exist in a joke.
except Exception as e:
    errors.append({'Error in': 'search_string', 'Error': e})

"""Testing for errors in id_range"""
try:
    j.get_joke(id_range=[30, 151])
except Exception as e:
    errors.append({'Error in': 'id_range', 'Error': e})

if len(errors):
    for e in errors:
        print(f"Error in:  {e['Error in']}\nError: {e['Error']}")
    raise Exception("Errors boii")
