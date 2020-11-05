import urllib3
import urllib
import urllib.request
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


class Jokes:
    def __init__(self):
        self.http = urllib3.PoolManager()
        self.info = self.http.request(
            'GET', "https://sv443.net/jokeapi/v2/info")
        self.info = data = json.loads(self.info.data.decode('utf-8'))["jokes"]

    def build_request(
        self,
        category=[],
        blacklist=[],
        response_format="json",
        joke_type="Any",
        search_string="",
        id_range=[],
        amount=1,
        lang="en"
    ):
        r = "https://sv443.net/jokeapi/v2/joke/"

        if len(category):
            for c in category:
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
            raise BlacklistError(f'''blacklist must be a list or tuple.''')

        if response_format not in ["json", "xml", "yaml", "txt"]:
            raise ResponseTypeError(
                "Response format must be either json, xml, txt or yaml."
            )
        if joke_type:
            if joke_type not in ["single", "twopart", "Any"]:
                raise JokeTypeError(
                    '''Invalid joke type.
                    Available options are "single" or "twopart".'''
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
                id_range[1] must be less than or equal to {range_limit-1}.")

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
            r += f"i&dRange={id_range[0]}-{id_range[1]}"
        if amount > 10:
            raise ValueError(
                f"amount parameter must be no greater than 10. you passed {amount}."
            )
        r += f"&amount={amount}"

        r += f"&lang={lang}"

        return r

    def send_request(self,
                     request,
                     response_format,
                     return_headers,
                     auth_token,
                     user_agent
                     ):
        returns = []

        if auth_token:
            r = self.http.request('GET',
                                  request,
                                  headers={'Authorization': str(auth_token),
                                           'user-agent': str(user_agent),
                                           'accept-encoding': 'gzip'
                                           }
                                  )
        else:
            r = self.http.request('GET', request, headers={
                                  'user-agent': str(user_agent),
                                  'accept-encoding': 'gzip'})

        data = r.data.decode('utf-8')

        if response_format == "json":
            try:
                data = json.loads(data)
            except:
                print(data)
                raise
        else:
            if len(' '.join(re.split("error", data.lower())[0:][1:]).replace(
                    '<', '').replace('/', '').replace(' ', '').replace(':', '')
                    .replace('>', '')) == 4:
                raise Exception(f"API returned an error. \
                Full response: \n\n {data}")

        headers = str(r.headers).replace(r'\n', '').replace(
            '\n', '').replace(r'\\', '').replace(r"\'", '')[15:-1]

        returns.append(data)
        if return_headers:
            returns.append(headers)

        if auth_token:
            returns.append(
                {"Token-Valid": bool(int(re.split(r"Token-Valid", headers)[1][4]))})

        if len(returns) > 1:
            return returns
        return returns[0]

    def get_joke(
        self,
        category=[],
        blacklist=[],
        response_format="json",
        joke_type="Any",
        search_string="",
        id_range=[],
        amount=1,
        lang=None,
        auth_token=None,
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) \
        Gecko/20100101 Firefox/77.0",
        return_headers=False
    ):
        r = self.build_request(
            category,
            blacklist,
            response_format,
            joke_type,
            search_string,
            id_range,
            amount,
            lang
        )

        response = self.send_request(
            r, response_format, return_headers, auth_token, user_agent)
        return response

    def submit_joke(self, category, joke, flags, lang="en"):
        request = {"formatVersion": 3}

        if category not in self.info["categories"]:
            raise CategoryError(
                f'''Invalid category selected.
            You selected {category}.
            Available categories are:
            {"""
            """.join(self.info["categories"])}''')
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
                ''')
        request["flags"] = flags
        request["lang"] = lang

        data = str(request).replace("'", '"')
        data = data.replace(": True", ": true").replace(": False", ": false")
        data = data.encode('ascii')
        url = "https://sv443.net/jokeapi/v2/submit"

        try:
            response = urllib.request.urlopen(url, data=data)
            data = response.getcode()

            return data
        except urllib.error.HTTPError as e:
            body = e.read().decode()  # Read the body of the error response

            _json = json.loads(body)
            return _json
