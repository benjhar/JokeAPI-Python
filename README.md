# Sv443's Joke API Wrapper
<div align="center" style="text-align:center">

[![Downloads](https://pepy.tech/badge/jokeapi)](https://pepy.tech/project/jokeapi)
[![Downloads](https://pepy.tech/badge/jokeapi/month)](https://pepy.tech/project/jokeapi/month)
[![Downloads](https://pepy.tech/badge/jokeapi/week)](https://pepy.tech/project/jokeapi/week)
[![CircleCI](https://circleci.com/gh/leet-hakker/JokeAPI-Python.svg?style=svg)](https://circleci.com/gh/leet-hakker/JokeAPI-Python)


</div>
An API wrapper for Sv443's joke api which provides simple yet versatile functionality,
while also maintaining a readable codebase.

## Install

You can install jokeapi through [pip](https://pypi.org/project/pip/) by using `pip install jokeapi`

---

# get_joke

The wrapper is structured in such a way that the end-user should only ever have to
interact with one function to get a joke. This function is `get_joke()`.

Please note that urllib3, the core dependency of this wrapper automatically abides by
`Retry-After` headers, which means you may have to wait a long time for a joke if you
have made a lot of requests recently

---

# submit_joke

The wrapper also provides simple access to the submit endpoint through the `submit_joke()`
function.

Note that joke submissions are manually checked and you will be ratelimited.

---

## get_joke

### Example

```python
from jokeapi import Jokes # Import the Jokes class
import asyncio

async def print_joke():
    j = await Jokes()  # Initialise the class
    await j.get_joke()  # Retrieve a random joke
    if joke["type"] == "single": # Print the joke
        print(joke["joke"])
    else:
        print(joke["setup"])
        print(joke["delivery"])

asyncio.run(print_joke())
```

### Parameters

---

#### category

A list of categories that the returned joke should fit in.
Options are:
`programming`,
`miscellaneous`,
`dark`,
`pun`

If left blank it will default to use `Any`.

##### Example

```python
  joke = await j.get_joke(category=['programming', 'dark'])  # Will return a joke that fits in either the programming or dark category.
```

---

#### blacklist

A list of properties that the joke *shouldn't* have.
Options are:
`nsfw`,
`religious`,
`political`,
`racist`,
`sexist`

If left blank it will default to `None`.

##### Example

```python
  joke = await j.get_joke(blacklist=['nsfw', 'racist'])  # Will return a joke that does not have either the flag "nsfw" or "racist".
```

---

#### response_format

The format in which the API should respond.
Options are:
`json`,
`yaml`,
`xml`,
`txt`

If left blank it will default to `json`.

##### Example

```python
  joke = await j.get_joke(response_format="xml")  # Will return a joke in xml format.
```

---

#### joke_type

The type of joke returned.
Options are:
`single`,
`twopart`,
`Any`

If left blank it will default to `Any`

##### Example

```python
  joke = await j.get_joke(joke_type="twopart")  # Will return a twopart joke; both a setup and a delivery.
```

---

#### search_string

A string to search for in jokes.

If left blank it will default to `None`

##### Example

```python
  joke = await j.get_joke(search_string="the")  # Will return a joke with the word "the" in it.
  # If there are no jokes then it will return the error from the API.
```

---

#### id_range

The range in which the selected joke should fall. ID's are decided by the order in which jokes are submitted.
The argument passes should be in form of list or tuple, and should not exceed length of 2 items. First item
should be minimum 0. Maximum value can be determined [here](https://sv443.net/jokeapi/v2/info)

If left blank it will default to the maximum range.


##### Example

```python
  joke = await j.get_joke(id_range=[10,100])  # Will return a joke with the ID between 10 and 100.
```

---

#### amount

The amount of jokes you want the api to return. Will return them in a list. Maximum number is 10 jokes, and the
api defaults to 1 if you use a number larger than the maximum. Defaults to 1.


##### Example

```python
  joke = await j.get_joke(amount=2) # Will return 2 jokes.
```

---

#### lang

The language that the joke and response should be in. Currently supported languages are in the official api
documentation. Defaults to en.

##### Example

```python
  joke = await j.get_joke(lang="de")
```

---

#### auth_token

A string token provided by the api owner. Using it will mean you are whitelisted by the api and can make
more requests than normal users. Defaults to None


##### Example

```python
  joke = await j.get_joke(auth_token="aaaaaaaaaaaaaaaaaaaaabbbbbbbbbbbbbbbbbbbbb") # Will send the token to the api in a header.
```

---

#### user_agent

A string sent the the api that tells the api what browser you are (pretending to be). The default user agent
is Mozilla Firefox from Windows 10 and should work fine, but the functionality is provided in case you wish
to change it


##### Example

```python
  joke = await j.get_joke(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0")
  # This is in fact the default user agent, and tells the API that we are visitng the page from a Firefox 77.0
  # browser using Windows 10 64bit.
```

---

#### return_headers

A boolean value (True or False) that tells the wrapper if you wish to receive headers in the return from the function.
Will return a list instead of a single value
Defaults to False.


##### Example

```python
  response = await j.get_joke(return_headers=True)
  joke = response[0]
  headers = response[1]

  print(f"Joke: {joke}")
  print(f"Headers: {headers}")
```

---

### Returns

Depending on what format is chosen different things will be returned.


#### json

A succesful API call will return:

```json
  {
      "category": "Miscellaneous",
      "type": "twopart",
      "setup": "I told my psychiatrist I got suicidal tendencies.",
      "delivery": "He said from now on I have to pay in advance.",
      "flags": {
          "nsfw": false,
          "religious": false,
          "political": false,
          "racist": false,
          "sexist": false
      },
      "id": 94,
      "error": false
  }
```


#### xml

A succesful API call will return:

```xml
<?xml version='1.0'?>
<data>
    <category>Dark</category>
    <type>single</type>
    <joke>My ex had an accident. I told the paramedics the wrong blood type for her. She'll finally experience what rejection is really like.</joke>
    <flags>
        <nsfw>false</nsfw>
        <religious>false</religious>
        <political>false</political>
        <racist>false</racist>
        <sexist>false</sexist>
    </flags>
    <id>154</id>
    <error>false</error>
</data>
```


#### yaml

A succesful API call will return:

```yaml
category: "Programming"
type: "single"
joke: "Your momma is so fat, you need to switch to NTFS to store a picture of her."
flags:
  nsfw: false
  religious: false
  political: false
  racist: false
  sexist: false
id: 56
error: false
```


#### txt

A succesful API call will return:

```
Why does no one like SQLrillex?

He keeps dropping the database.
```

---

### Errors

The wrapper can raise multiple different errors depending on what you did wrong.

The errors are descriptive enough that you should be able to solve them with the information provided in the error message.
If not, feel free to ask me through one of the channels provided below.

---

## submit_joke

### Example

```python
from jokeapi import Jokes
import asyncio

async def submit_new_joke():
	j = await Jokes()

	await j.submit_joke("Miscellaneous", "funny haha", {
	    "nsfw": False,
	    "religious": False,
	    "political": False,
	    "racist": False,
	    "sexist": False
	}, lang="de")

asyncio.run(submit_new_joke())
```

---

### Parameters

---

#### category

The category the joke is.
Options are:
`programming`,
`miscellaneous`,
`dark`,
`pun`

Has no default value.

---

#### joke

The joke itself. Can either be a single string or a list/tuple, for the setup and
delivery. Setup should be at index 0 in the tuple, delivery at 1.

Has no default value.

---

#### flags

The flags that the joke should have.
Options are:
`nsfw`,
`religious`,
`political`,
`racist`,
`sexist`

Has no default value.

#### lang

The language code for the language the joke it written in. E.g en for english,
de for german.

Defaults to `en`

---


## Contributors

[ThatCopy](https://github.com/ThatCopy)
 - [27994f7](https://github.com/thenamesweretakenalready/Sv443s-JokeAPI-Python-Wrapper/commit/27994f74fdea51cb2ddcee9ea127d393868aca00)
 - [01b578c](https://github.com/thenamesweretakenalready/Sv443s-JokeAPI-Python-Wrapper/commit/01b578cbb500d02ff27925459223e40505aafe96)

[kdiri](https://github.com/kdiri)
 - [3e20cd1](https://github.com/thenamesweretakenalready/Sv443s-JokeAPI-Python-Wrapper/commit/3e20cd1dbd1e5ac6b08ed90c720bf2890a6a4ffd)
 - [3b6a2a6](https://github.com/thenamesweretakenalready/Sv443s-JokeAPI-Python-Wrapper/commit/3b6a2a6164225fb9d5cb1bd77b0ccebd9bd8bffd)


## Developer contact

![Discord](https://discord.com/assets/07dca80a102d4149e9736d4b162cff6f.ico)[**Discord**](https://discord.gg/mB989eP)

[Issue Tracker](https://github.com/thenamesweretakenalready/JokeAPI-Python/issues)

[e-mail](mailto:leet_haker@cyber-wizard.com)
