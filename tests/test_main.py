from os import getenv
from dotenv import load_dotenv
import sys, os
import asyncio
import pytest
import pytest_asyncio.plugin
import traceback

sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir, "src"))
from jokeapi import Jokes

load_dotenv()

pytestmark = pytest.mark.asyncio

async def test_main():
    j = await Jokes()
    errors = []
    token = getenv("token")

    try:
        await j.get_joke(user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Brave Chrome/91.0.4472.164 Safari/537.36")
    except Exception as e:
        errors.append({"Error in": "blank joke get", "Error": traceback.extract_tb()})

    """Testing auth tokens"""
    try:
        await j.get_joke(auth_token=token, user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Brave Chrome/91.0.4472.164 Safari/537.36")
    except Exception as e:
        auth_token = None
        errors.append({"Error in": "auth usage", "Error": traceback.extract_tb()})

    """Testing for errors in categories"""
    try:
        await j.get_joke(category=["programming"], auth_token=token, user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Brave Chrome/91.0.4472.164 Safari/537.36")
    except Exception as e:
        errors.append({"Error in": "category programming", "Error": traceback.extract_tb()})
    try:
        await j.get_joke(category=["misc"], auth_token=token, user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Brave Chrome/91.0.4472.164 Safari/537.36")
    except Exception as e:
        errors.append({"Error in": "category miscellaneous", "Error": traceback.extract_tb()})
    try:
        await j.get_joke(category=["dark"], auth_token=token, user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Brave Chrome/91.0.4472.164 Safari/537.36")
    except Exception as e:
        errors.append({"Error in": "category dark", "Error": traceback.extract_tb()})

    """Testing for errors in blacklist"""
    try:
        await j.get_joke(blacklist=["nsfw"], auth_token=token, user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Brave Chrome/91.0.4472.164 Safari/537.36")
    except Exception as e:
        errors.append({"Error in": "blacklist nsfw", "Error": traceback.extract_tb()})

    try:
        await j.get_joke(blacklist=["religious"], auth_token=token, user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Brave Chrome/91.0.4472.164 Safari/537.36")
    except Exception as e:
        errors.append({"Error in": "blacklist religious", "Error": traceback.extract_tb()})

    try:
        await j.get_joke(blacklist=["political"], auth_token=token, user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Brave Chrome/91.0.4472.164 Safari/537.36")
    except Exception as e:
        errors.append({"Error in": "blacklist political", "Error": traceback.extract_tb()})

    try:
        await j.get_joke(blacklist=["racist"], auth_token=token, user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Brave Chrome/91.0.4472.164 Safari/537.36")
    except Exception as e:
        errors.append({"Error in": "blacklist political", "Error": traceback.extract_tb()})

    try:
        await j.get_joke(blacklist=["sexist"], auth_token=token, user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Brave Chrome/91.0.4472.164 Safari/537.36")
    except Exception as e:
        errors.append({"Error in": "blacklist sexist", "Error": traceback.extract_tb()})

    """Testing for errors in response_format"""
    try:
        await j.get_joke(response_format="xml", auth_token=token, user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Brave Chrome/91.0.4472.164 Safari/537.36")
    except Exception as e:
        errors.append({"Error in": "response_format xml", "Error": traceback.extract_tb()})

    try:
        await j.get_joke(response_format="yaml", auth_token=token, user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Brave Chrome/91.0.4472.164 Safari/537.36")
    except Exception as e:
        errors.append({"Error in": "response_format yaml", "Error": traceback.extract_tb()})

    """Testing for errors in type"""
    try:
        await j.get_joke(joke_type="single", auth_token=token, user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Brave Chrome/91.0.4472.164 Safari/537.36")
    except Exception as e:
        errors.append({"Error in": "type single", "Error": traceback.extract_tb()})

    try:
        await j.get_joke(joke_type="twopart", auth_token=token, user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Brave Chrome/91.0.4472.164 Safari/537.36")
    except Exception as e:
        errors.append({"Error in": "type double", "Error": traceback.extract_tb()})

    """Testing for errors in search_string"""
    try:
        await j.get_joke(search_string="search", auth_token=token, user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Brave Chrome/91.0.4472.164 Safari/537.36")
        # as long as this gets a response, the api wrapper is fine;
        # it probably doesn't exist in a joke.
    except Exception as e:
        errors.append({"Error in": "search_string", "Error": traceback.extract_tb()})

    """Testing for errors in id_range"""
    try:
        await j.get_joke(id_range=[30, 151], auth_token=token, user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Brave Chrome/91.0.4472.164 Safari/537.36")
    except Exception as e:
        errors.append({"Error in": "id_range", "Error": traceback.extract_tb()})

    """Testing for errors in safe_mode"""
    try:
        await j.get_joke(safe_mode=True, auth_token=token, user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Brave Chrome/91.0.4472.164 Safari/537.36")
    except Exception as e:
        errors.append({"Error in": "safe_mode", "Error": traceback.extract_tb()})

    """Testing for errors in user agent"""
    try:
        await j.get_joke(user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Brave Chrome/91.0.4472.164 Safari/537.36")
    except Exception as e:
        errors.append({"Error in": "user agent", "Error": traceback.extract_tb()})


    """    Testing jokeapi.submit_joke()    """
    try:
        await j.submit_joke("Programming", ["foo", "bar"], {}, dry_run=True)
    except Exception as e:
        errors.append({"Error in": "dry_run", "Error": traceback.extract_tb()})


    if len(errors):
        for e in errors:
            print(f"Error in:  {e['Error in']}\nError: {e['Error']}")
        if len(errors) == 1:
            raise Exception("1 error occured")

        raise Exception(f"{len(errors)} errors occurred")
