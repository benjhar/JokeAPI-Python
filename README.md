# Sv443's Joke API Wrapper

[![Downloads](https://pepy.tech/badge/jokeapi)](https://pepy.tech/downloads/jokeapi)
[![CircleCI](https://circleci.com/gh/thenamesweretakenalready/Sv443s-JokeAPI-Python-Wrapper.svg?style=svg)](https://circleci.com/gh/thenamesweretakenalready/Sv443s-JokeAPI-Python-Wrapper)

An API wrapper for Sv443's joke api which provides simple yet versatile functionality,
while also maintaining a readable codebase.

## Install

You can install jokeapi through [pip](https://pypi.org/project/pip/) by using `pip install jokeapi`

So far there are no build from source instructions.

---

# get_joke

The wrapper is structured in such a way that the end-user should only ever have to
interact with one function. This function is `get_joke()`

---

## get_joke

### Example

```python
  from jokeapi import Jokes # Import the Jokes class

  j = Jokes()  # Initialise the class
  j.get_joke()  # Retrieve a random joke
```

### Parameters

---

#### category

A list of categories that the returned joke should fit in.
Options are:
`programming`,
`miscellaneous`,
`dark`

If left blank it will default to use `Any`.

##### Example

```python
  joke = get_joke(categories=['programming', 'dark'])  # Will return a joke that fits in either the programming or dark category.
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
  joke = get_joke(blacklist=['nsfw', 'racist'])  # Will return a joke that does not have either the flag "nsfw" or "racist".
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

#### Example

```python
  joke = get_joke(response_format="xml")  # Will return a joke in xml format.
```

---

### type

The type of joke returned.
Options are:
`single`,
`twopart`

If left blank it will default to `Any`

#### Example

```python
  joke = get_joke(type="twopart")  # Will return a twopart joke; both a setup and a delivery.
```

---

### search_string

A string to search for in jokes.

If left blank it will default to `None`

#### Example

```python
  joke = get_joke(search_string="the")  # Will return a joke with the word "the" in it.
  # If there are no jokes then it will return the error from the API.
```

---

### id_range

The range in which the selected joke should fall. ID's are decided by the order in which jokes are submitted.
The argument passes should be in form of list or tuple, and should not exceed length of 2 items. First item
should be minimum 0.

If left blank it will default to the maximum range.


#### Example

```python
  joke = get_joke(id_range=[10,100])  # Will return a joke with the ID between 10 and 100
```

---

## Returns

Depending on what format is chosen different things will be returned.


### json

A succesful API call will return:

```python
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


### xml

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


### yaml

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


### txt

A succesful API call will return:

```
Why does no one like SQLrillex?

He keeps dropping the database.
```

---

## Errors

The wrapper can raise multiple different errors depending on what you did wrong.

### ValueErrors will always be raised with expected errors.

The errors are descriptive enough that you should be able to solve them with the information provided in the error message.
If not, feel free to ask me through one of the channels provided below.

---

Developer contact:
[Discord](https://discord.gg/mB989eP)
[Issue Tracker](https://github.com/thenamesweretakenalready/Sv443s-JokeAPI-Python-Wrapper/issues)
[e-mail](mailto:leet_haker@cyber-wizard.com)
[Twitter](https://twitter.com/HakkerLeet)
