from os import getenv
from jokeapi import Jokes
from dotenv import load_dotenv
import time
load_dotenv()

j = Jokes()
errors = []
token = getenv("token")


try:
    j.get_joke()
except Exception as e:
    errors.append({'Error in':  'blank joke get',  'Error': e})

"""Testing auth tokens"""
try:
    j.get_joke(auth_token=token)
except Exception as e:
    auth_token = None
    errors.append({'Error in':  'auth usage',  'Error': e})

"""Testing for errors in categories"""
try:
    j.get_joke(category=["programming"], auth_token=token)
except Exception as e:
    errors.append({'Error in':  'category programming', 'Error': e})
try:
    j.get_joke(category=["miscellaneous"], auth_token=token)
except Exception as e:
    errors.append({'Error in':  'category miscellaneous', 'Error': e})
try:
    j.get_joke(category=["dark"], auth_token=token)
except Exception as e:
    errors.append({'Error in':  'category dark', 'Error': e})

"""Testing for errors in blacklist"""
try:
    j.get_joke(blacklist=["nsfw"], auth_token=token)
except Exception as e:
    errors.append({'Error in':  'blacklist nsfw', 'Error': e})

try:
    j.get_joke(blacklist=["religious"], auth_token=token)
except Exception as e:
    errors.append({'Error in':  'blacklist religious', 'Error': e})

try:
    j.get_joke(blacklist=["political"], auth_token=token)
except Exception as e:
    errors.append({'Error in':  'blacklist political', 'Error': e})

try:
    j.get_joke(blacklist=["racist"], auth_token=token)
except Exception as e:
    errors.append({'Error in':  'blacklist political', 'Error': e})

try:
    j.get_joke(blacklist=["sexist"], auth_token=token)
except Exception as e:
    errors.append({'Error in':  'blacklist sexist',  'Error': e})


"""Testing for errors in response_format"""
try:
    j.get_joke(response_format="xml", auth_token=token)
except Exception as e:
    errors.append({'Error in':  'response_format xml', 'Error': e})

try:
    j.get_joke(response_format="yaml", auth_token=token)
except Exception as e:
    errors.append({'Error in':  'response_format yaml', 'Error': e})


"""Testing for errors in type"""
try:
    j.get_joke(type="single", auth_token=token)
except Exception as e:
    errors.append({'Error in':  'type single', 'Error': e})

try:
    j.get_joke(type="twopart", auth_token=token)
except Exception as e:
    errors.append({'Error in':  'type double', 'Error': e})


"""Testing for errors in search_string"""
try:
    j.get_joke(search_string="search", auth_token=token)
    # as long as this gets a response, the api wrapper is fine;
    # it probably doesn't exist in a joke.
except Exception as e:
    errors.append({'Error in': 'search_string', 'Error': e})


"""Testing for errors in id_range"""
try:
    j.get_joke(id_range=[30, 151], auth_token=token)
except Exception as e:
    errors.append({'Error in': 'id_range', 'Error': e})


if len(errors):
    for e in errors:
        print(f"Error in:  {e['Error in']}\nError: {e['Error']}")
    if len(errors) == 1:
        raise Exception("1 error occured")

    raise Exception(f"{len(errors)} errors occurred")
