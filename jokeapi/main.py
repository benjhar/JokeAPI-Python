import urllib3
import urllib
import simplejson as json
import re


class Jokes:
    def __init__(self):
        self.http = urllib3.PoolManager()
        print("Sv443's JokeAPI")

    def build_request(
        self,
        category=[],
        blacklist=[],
        response_format="json",
        type=None,
        search_string=None,
        id_range=None,
    ):
        r = "https://sv443.net/jokeapi/v2/joke/"

        if len(category) > 0:
            for c in category:
                if not c.lower() in ["programming", "miscellaneous", "dark"]:
                    raise ValueError(
                        '''Invalid category selected. Available categories are:
                            "programming"
                            "miscellaneous"
                            "dark".
                        Leave blank for any.'''
                    )
                    return
            cats = ",".join(category)
        else:
            cats = "Any"

        if len(blacklist) > 0:
            for b in blacklist:
                if b not in [
                    "nsfw",
                    "religious",
                    "political",
                    "racist",
                    "sexist"
                ]:
                    raise ValueError(
                        '''\n\n
                        You have blacklisted flags which are not available.
                        Available flags are:
                            "racist"
                            "religious"
                            "political"
                            "sexist"
                            "nsfw"
                        '''
                    )
                    return
            blacklistFlags = ",".join(blacklist)
        else:
            blacklistFlags = None

        if response_format not in ["json", "xml", "yaml", "txt"]:
            raise Exception(
                "Response format must be either json, xml or yaml."
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

            response = self.http.request(
                'GET',
                "https://sv443.net/jokeapi/v2/info"
            )
            dict = json.loads(response.data)
            range_limit = dict["jokes"]["totalCount"]

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

        prev_flags = None

        if blacklistFlags:
            r += f"?blacklistFlags={blacklistFlags}"
            prev_flags = True
        if prev_flags:
            r += f"&format={response_format}"
        else:
            r += f"?format={response_format}"
            prev_flags = True
        if prev_flags:
            r += f"&type={type}"
        else:
            r += f"?type={type}"
            prev_flags = True
        if search_string:
            if prev_flags:
                r += f"&contains={search_string}"
                prev_flags = True
            else:
                r += f"?contains={search_string}"
        if id_range:
            if prev_flags:
                r += f"&idRange={id_range[0]}-{id_range[1]}"
            else:
                r += f"?idRange={id_range[0]}-{id_range[1]}"

        return r

    def send_request(self, request, response_format, return_headers, auth_token, user_agent):
        returns = []

        if auth_token:
            r = self.http.request('GET', request, headers={'Authorization': str(
                auth_token), 'user-agent': str(user_agent)})
        else:
            r = self.http.request('GET', request, headers={'user-agent': str(user_agent)})

        data = r.data

        if response_format == "json":
            try:
                data = json.loads(data)
            except:
                print(data)
                raise
        else:
            data = str(data)[2:-1].replace(r'\n', '\n').replace('\\', '')
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
        auth_token=None,
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0",
        return_headers=False
    ):
        r = self.build_request(
            category, blacklist, response_format, type, search_string, id_range
        )

        response = self.send_request(r, response_format, return_headers, auth_token, user_agent)
        return response
