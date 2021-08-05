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


async def test_blank():
    j = await Jokes()
    await j.get_joke(
        user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Brave Chrome/91.0.4472.164 Safari/537.36"
    )


async def test_auth_tokens():
    j = await Jokes()
    token = getenv("token")
    await j.get_joke(
        auth_token=token,
        user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Brave Chrome/91.0.4472.164 Safari/537.36",
    )


async def test_categories():
    j = await Jokes()
    token = getenv("token")
    await j.get_joke(
        category=["programming"],
        auth_token=token,
        user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Brave Chrome/91.0.4472.164 Safari/537.36",
    )
    await j.get_joke(
        category=["misc"],
        auth_token=token,
        user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Brave Chrome/91.0.4472.164 Safari/537.36",
    )
    await j.get_joke(
        category=["dark"],
        auth_token=token,
        user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Brave Chrome/91.0.4472.164 Safari/537.36",
    )


async def test_blacklist():
    j = await Jokes()
    token = getenv("token")
    await j.get_joke(
        blacklist=["nsfw"],
        auth_token=token,
        user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Brave Chrome/91.0.4472.164 Safari/537.36",
    )

    await j.get_joke(
        blacklist=["religious"],
        auth_token=token,
        user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Brave Chrome/91.0.4472.164 Safari/537.36",
    )
    await j.get_joke(
        blacklist=["political"],
        auth_token=token,
        user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Brave Chrome/91.0.4472.164 Safari/537.36",
    )
    await j.get_joke(
        blacklist=["racist"],
        auth_token=token,
        user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Brave Chrome/91.0.4472.164 Safari/537.36",
    )
    await j.get_joke(
        blacklist=["sexist"],
        auth_token=token,
        user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Brave Chrome/91.0.4472.164 Safari/537.36",
    )


async def test_repsonse_format():
    j = await Jokes()
    token = getenv("token")
    await j.get_joke(
        response_format="xml",
        auth_token=token,
        user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Brave Chrome/91.0.4472.164 Safari/537.36",
    )

    await j.get_joke(
        response_format="yaml",
        auth_token=token,
        user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Brave Chrome/91.0.4472.164 Safari/537.36",
    )


async def test_joke_type():
    j = await Jokes()
    token = getenv("token")
    await j.get_joke(
        joke_type="single",
        auth_token=token,
        user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Brave Chrome/91.0.4472.164 Safari/537.36",
    )
    await j.get_joke(
        joke_type="twopart",
        auth_token=token,
        user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Brave Chrome/91.0.4472.164 Safari/537.36",
    )


async def test_search_string():
    j = await Jokes()
    token = getenv("token")
    await j.get_joke(
        search_string="search",
        auth_token=token,
        user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Brave Chrome/91.0.4472.164 Safari/537.36",
    )
    # as long as this gets a response, the api wrapper is fine;
    # it probably doesn't exist in a joke.


async def test_id_range():
    j = await Jokes()
    token = getenv("token")
    await j.get_joke(
        id_range=[30, 151],
        auth_token=token,
        user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Brave Chrome/91.0.4472.164 Safari/537.36",
    )


async def test_safe_mode():
    j = await Jokes()
    token = getenv("token")

    await j.get_joke(
        safe_mode=True,
        auth_token=token,
        user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Brave Chrome/91.0.4472.164 Safari/537.36",
    )


async def test_user_agent():
    j = await Jokes()
    token = getenv("token")
    await j.get_joke(
        user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Brave Chrome/91.0.4472.164 Safari/537.36"
    )


async def test_submit_joke():
    j = await Jokes()
    token = getenv("token")
    await j.submit_joke("Programming", ["foo", "bar"], {}, dry_run=True)
