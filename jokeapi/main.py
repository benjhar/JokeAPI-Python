import urllib3
import urllib
import json


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

    def send_request(self, request, response_format):
        r = self.http.request('GET', request)

        if response_format == "json":
            return json.loads(r.data)
        elif response_format == "xml":
            return r.data
        else:
            return r.data

    def get_joke(
        self,
        category=[],
        blacklist=[],
        response_format="json",
        type=None,
        search_string=None,
        id_range=None,
    ):
        r = self.build_request(
            category, blacklist, response_format, type, search_string, id_range
        )
        response = self.send_request(r, response_format)
        return response
