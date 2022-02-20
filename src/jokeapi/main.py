import urllib
import aiohttp
import simplejson as json
import re


class CategoryError(Exception):
    pass


class BlacklistError(Exception):
    pass


class ResponseTypeError(Exception):
    pass


class JokeTypeError(Exception):
    pass


async def fetch(session, url, headers=None):
    if headers:
        async with session.get(url, headers=headers) as response:
            response_text = await response.text()
            return response_text, response.headers
    else:
        async with session.get(url) as response:
            response_text = await response.text()
            return response_text, response.headers


async def post(session, url, data, headers=None):
    async with session.post(url, data=data, headers=headers) as response:
        response_text = await response.text()
        return response_text, response.headers


# https://stackoverflow.com/a/36724229
class AsyncIterator:
    def __init__(self, seq):
        self.iter = iter(seq)

    def __aiter__(self):
        return self

    async def __anext__(self):
        try:
            return next(self.iter)
        except StopIteration:
            raise StopAsyncIteration


class Joke_Class:
    async def init(self):
        async with aiohttp.ClientSession() as session:
            self.info, _ = await fetch(session, "https://v2.jokeapi.dev/info")
            self.info = json.loads(self.info)
            self.info = self.info["jokes"]

    async def build_request(
        self,
        category=[],
        blacklist=[],
        response_format="json",
        joke_type="Any",
        search_string="",
        id_range=[],
        amount=1,
        safe_mode=False,
        lang="en",
    ):
        r = "https://v2.jokeapi.dev/joke/"

        if len(category):
            async for c in AsyncIterator(category):
                if not c.title() in self.info["categories"]:
                    raise CategoryError(
                        f'''Invalid category selected.
                        You selected {c}.
                        Available categories are:
                        {"""
                        """.join(self.info["categories"])}
                        Leave blank for any.'''
                    )

            cats = ",".join(category)
        else:
            cats = "Any"

        if type(blacklist) in [list, tuple]:
            if len(blacklist) > 0:
                for b in blacklist:
                    if b not in self.info["flags"]:
                        raise BlacklistError(
                            f'''


                            You have blacklisted flags which are not available.
                            Available flags are:
                                {"""
                                """.join(self.info["flags"])}
                            '''
                        )
                        return
                blacklistFlags = ",".join(blacklist)
            else:
                blacklistFlags = None
        else:
            raise BlacklistError(f"""blacklist must be a list or tuple.""")

        if response_format not in ["json", "xml", "yaml", "txt"]:
            raise ResponseTypeError(
                "Response format must be either json, xml, txt or yaml."
            )
        if joke_type:
            if joke_type not in ["single", "twopart", "Any"]:
                raise JokeTypeError(
                    """Invalid joke type.
                    Available options are "single" or "twopart"."""
                )
                return
        else:
            joke_type = "Any"

        if search_string:
            if not isinstance(search_string, str):
                raise ValueError("search_string must be a string.")
                return
            else:
                search_string = urllib.parse.quote(search_string)
        range_limit = self.info["totalCount"]

        if len(id_range) and (id_range[1] - id_range[0] > range_limit):
            raise ValueError(
                "id_range must be no longer than 2 items, \
                id_range[0] must be greater than or equal to 0 and \
                id_range[1] must be less than or equal to {range_limit-1}."
            )

        if amount > 10:
            raise ValueError(
                f"amount parameter must be no greater than 10. \
                you passed {amount}."
            )

        r += cats

        r += f"?format={response_format}"

        if blacklistFlags:
            r += f"&blacklistFlags={blacklistFlags}"

        r += f"&type={joke_type}"

        if search_string:
            r += f"&contains={search_string}"
        if id_range:
            r += f"&idRange={id_range[0]}-{id_range[1]}"
        if amount > 10:
            raise ValueError(
                f"amount parameter must be no greater than 10. you passed {amount}."
            )
        r += f"&amount={amount}"

        r += f"&lang={lang}"

        r += f"{'&safe-mode'*safe_mode}"

        return r

    async def send_request(
        self, request, response_format, return_headers, auth_token, user_agent
    ):
        async with aiohttp.ClientSession() as session:
            returns = []

            if auth_token:
                r, headers = await fetch(
                    session,
                    request,
                    {
                        "Authorization": str(auth_token),
                        "user-agent": str(user_agent),
                        "accept-encoding": "gzip",
                    },
                )
            else:
                r, headers = await fetch(
                    session,
                    request,
                    {"user-agent": str(user_agent), "accept-encoding": "gzip"},
                )

            if response_format == "json":
                try:
                    data = json.loads(r)
                except:
                    print(r)
                    raise
            else:
                data = r
                if (
                    len(
                        " ".join(re.split("error", data.lower())[0:][1:])
                        .replace("<", "")
                        .replace("/", "")
                        .replace(" ", "")
                        .replace(":", "")
                        .replace(">", "")
                    )
                    == 4
                ):
                    raise Exception(
                        f"API returned an error. \
                    Full response: \n\n {data}"
                    )

            headers = (
                str(headers)
                .replace(r"\n", "")
                .replace("\n", "")
                .replace(r"\\", "")
                .replace(r"\'", "")[15:-1]
            )

            returns.append(data)
            if return_headers:
                returns.append(headers)

            if auth_token:
                if "token-valid" in headers:
                    returns.append(
                        {"Token-Valid": bool(int(headers.split("token-valid")[1][4]))}
                    )
                elif "Token-Valid" in headers:
                    returns.append(
                        {"Token-Valid": bool(int(headers.split("Token-Valid")[1][4]))}
                    )

            if len(returns) > 1:
                return returns
            return returns[0]

    async def get_joke(
        self,
        category=[],
        blacklist=[],
        response_format="json",
        joke_type="Any",
        search_string="",
        id_range=[],
        amount=1,
        safe_mode=False,
        lang="en",
        auth_token=None,
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) \
        Gecko/20100101 Firefox/77.0",
        return_headers=False,
    ):
        r = await self.build_request(
            category,
            blacklist,
            response_format,
            joke_type,
            search_string,
            id_range,
            amount,
            safe_mode,
            lang,
        )

        response = await self.send_request(
            r, response_format, return_headers, auth_token, user_agent
        )
        return response

    async def submit_joke(
        self,
        category,
        joke,
        flags,
        lang="en",
        dry_run=False,
        auth_token=None,
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) \
        Gecko/20100101 Firefox/77.0",
    ):
        async with aiohttp.ClientSession() as session:
            request = {"formatVersion": 3}

            if category not in self.info["categories"]:
                raise CategoryError(
                    f'''Invalid category selected.
                You selected {category}.
                Available categories are:
                {"""
                """.join(self.info["categories"])}'''
                )
            request["category"] = category

            if type(joke) in [list, tuple]:
                if len(joke) > 1:
                    request["type"] = "twopart"
                    request["setup"] = joke[0]
                    request["delivery"] = joke[1]
                else:
                    request["type"] = "single"
                    request["joke"] = joke[0]
            else:
                request["type"] = "single"
                request["joke"] = joke

            for key in flags.keys():
                if key not in self.info["flags"]:
                    raise BlacklistError(
                        f'''
                    You have blacklisted flags which are not available.
                    Available flags are:
                        {"""
                        """.join(self.info["flags"])}
                    '''
                    )
            request["flags"] = flags
            request["lang"] = lang

            data = json.dumps(request).replace("'", '"')
            data = data.encode("ascii")
            url = f"https://v2.jokeapi.dev/submit{'?dry-run'*dry_run}"

            if auth_token:
                headers = {
                    "Authorization": str(auth_token),
                    "user-agent": str(user_agent),
                    "accept-encoding": "gzip",
                }
            else:
                headers = {
                    "user-agent": str(user_agent),
                    "accept-encoding": "gzip",
                }

            try:
                response, headers = await post(session, url, data, headers)
                data = json.loads(response)

                return data
            except aiohttp.ClientResponseError as e:
                error_json = {
                    "error": True,
                    "message": e.message,
                    "status": e.status,
                    "headers": e.headers,
                }

                return error_json


async def Jokes():
    jokes = Joke_Class()
    await jokes.init()
    return jokes
