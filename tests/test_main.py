from os import getenv
from dotenv import load_dotenv
import sys, os
import asyncio
import pytest
import pytest_asyncio.plugin

sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir, "src"))
from jokeapi import Jokes

load_dotenv()

pytestmark = pytest.mark.asyncio

async def test_main():
    j = await Jokes()
    errors = []
    token = getenv("token")

    try:
        await j.get_joke()
    except Exception as e:
        errors.append({"Error in": "blank joke get", "Error": e})

    """Testing auth tokens"""
    try:
        await j.get_joke(auth_token=token)
    except Exception as e:
        auth_token = None
        errors.append({"Error in": "auth usage", "Error": e})

    """Testing for errors in categories"""
    try:
        await j.get_joke(category=["programming"], auth_token=token)
    except Exception as e:
        errors.append({"Error in": "category programming", "Error": e})
    try:
        await j.get_joke(category=["misc"], auth_token=token)
    except Exception as e:
        errors.append({"Error in": "category miscellaneous", "Error": e})
    try:
        await j.get_joke(category=["dark"], auth_token=token)
    except Exception as e:
        errors.append({"Error in": "category dark", "Error": e})

    """Testing for errors in blacklist"""
    try:
        await j.get_joke(blacklist=["nsfw"], auth_token=token)
    except Exception as e:
        errors.append({"Error in": "blacklist nsfw", "Error": e})

    try:
        await j.get_joke(blacklist=["religious"], auth_token=token)
    except Exception as e:
        errors.append({"Error in": "blacklist religious", "Error": e})

    try:
        await j.get_joke(blacklist=["political"], auth_token=token)
    except Exception as e:
        errors.append({"Error in": "blacklist political", "Error": e})

    try:
        await j.get_joke(blacklist=["racist"], auth_token=token)
    except Exception as e:
        errors.append({"Error in": "blacklist political", "Error": e})

    try:
        await j.get_joke(blacklist=["sexist"], auth_token=token)
    except Exception as e:
        errors.append({"Error in": "blacklist sexist", "Error": e})

    """Testing for errors in response_format"""
    try:
        await j.get_joke(response_format="xml", auth_token=token)
    except Exception as e:
        errors.append({"Error in": "response_format xml", "Error": e})

    try:
        await j.get_joke(response_format="yaml", auth_token=token)
    except Exception as e:
        errors.append({"Error in": "response_format yaml", "Error": e})

    """Testing for errors in type"""
    try:
        await j.get_joke(joke_type="single", auth_token=token)
    except Exception as e:
        errors.append({"Error in": "type single", "Error": e})

    try:
        await j.get_joke(joke_type="twopart", auth_token=token)
    except Exception as e:
        errors.append({"Error in": "type double", "Error": e})

    """Testing for errors in search_string"""
    try:
        await j.get_joke(search_string="search", auth_token=token)
        # as long as this gets a response, the api wrapper is fine;
        # it probably doesn't exist in a joke.
    except Exception as e:
        errors.append({"Error in": "search_string", "Error": e})

    """Testing for errors in id_range"""
    try:
        await j.get_joke(id_range=[30, 151], auth_token=token)
    except Exception as e:
        errors.append({"Error in": "id_range", "Error": e})

    """Testing for errors in safe_mode"""
    try:
        await j.get_joke(safe_mode=True, auth_token=token)
    except Exception as e:
        errors.append({"Error in": "safe_mode", "Error": e})

    """Testing for errors in user agent"""
    try:
        await j.get_joke(user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Brave Chrome/91.0.4472.164 Safari/537.36")
    except Exception as e:
        errors.append({"Error in": "user agent", "Error": e})


    """    Testing jokeapi.submit_joke()    """
    try:
        await j.submit_joke("Programming", ["foo", "bar"], {}, dry_run=True)
    except Exception as e:
        errors.append({"Error in": "dry_run", "Error": e})


    if len(errors):
        for e in errors:
            print(f"Error in:  {e['Error in']}\nError: {e['Error']}")
        if len(errors) == 1:
            raise Exception("1 error occured")

        raise Exception(f"{len(errors)} errors occurred")
