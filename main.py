import urllib3
import urllib
import simplejson as json
import re


class Jokes:
    def __init__(self):
        self.http = urllib3.PoolManager()
        self.info = self.http.request('GET', "https://sv443.net/jokeapi/v2/info")
        print("Sv443's JokeAPI")

    def build_request(
        self,
        category=[],
        blacklist=[],
        response_format="json",
        type=None,
        search_string=None,
        id_range=None,
        amount=1,
        lang="en"
    ):
        r = "https://sv443.net/jokeapi/v2/joke/"

        if len(category):
            for c in category:
                if not c.lower() in self.info["categories"]:
                    raise ValueError(
                        f'''Invalid category selected.
                        You selected {c}.
                        Available categories are:
                            "programming"
                            "miscellaneous"
                            "dark"
                            "pun".
                        Leave blank for any.'''
                    )

            cats = ",".join(category)
        else:
            cats = "Any"

        if len(blacklist) > 0:
            for b in blacklist:
                if b not in self.info["flags"]:
                    raise ValueError(
                        f'''


                        You have blacklisted flags which are not available or you have not put the flags in a list.
                        Available flags are:
                            {"""
                            """.join(self.info["flags"])}
                        '''
                    )
                    return
            blacklistFlags = ",".join(blacklist)
        else:
            blacklistFlags = None

        if response_format not in ["json", "xml", "yaml", "txt"]:
            raise Exception(
                "Response format must be either json, xml, txt or yaml."
            )
        if type:
            if type not in ["single", "twopart"]:
                raise ValueError(
                    '''Invalid joke type.
                    Available options are "single" or "twopart".'''
                )
                return
        else:
            type = "Any"

        if search_string:
            if not isinstance(search_string, str):
                raise ValueError("search_string must be a string.")
                return
            else:
                search_string = urllib.parse.quote(search_string)
        if id_range:
            range_limit = self.info["totalCount"]

            if len(id_range) > 2:
                raise ValueError("id_range must be no longer than 2 items.")
            elif id_range[0] < 0:
                raise ValueError(
                    "id_range[0] must be greater than or equal to 0."
                )
            elif id_range[1] > range_limit:
                raise ValueError(
                    f"id_range[1] must be less than or equal to {range_limit-1}."
                )

        r += cats

        r += f"?format={response_format}"

        if blacklistFlags:
            r += f"&blacklistFlags={blacklistFlags}"


        r += f"&type={type}"

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
                                           #'accept-encoding': 'gzip'
                                          }
                                  )
        else:
            r = self.http.request('GET', request, headers={'user-agent': str(user_agent)})

        data = r.data.decode('utf-8')

        if response_format == "json":
            try:
                data = json.loads(data)
            except:
                print(data)
                raise
        else:
            if len(' '.join(re.split("error", data.lower().replace("\n", "NEWLINECHAR"))[0:][1:]).replace(
                    '<', '').replace('/', '').replace(' ', '').replace(':', '').replace('>', '').replace('NEWLINECHAR', '\n')) == 4:
                return [Exception(f"API returned an error. Full response: \n\n {data}")]

        headers = str(r.headers).replace(r'\n', '').replace(
            '\n', '').replace(r'\\', '').replace(r"\'", '')[15:-1]

        returns.append(data)
        if return_headers:
            returns.append(headers)

        if auth_token:
            returns.append({"Token-Valid": bool(int(re.split(r"Token-Valid", headers)[1][4]))})

        return returns

    def get_joke(
        self,
        category=[],
        blacklist=[],
        response_format="json",
        type=None,
        search_string=None,
        id_range=None,
        amount=1,
        lang=None,
        auth_token=None,
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0",
        return_headers=False
    ):
        r = self.build_request(
            category, blacklist, response_format, type, search_string, id_range, amount, lang
        )

        response = self.send_request(r, response_format, return_headers, auth_token, user_agent)
        return response
