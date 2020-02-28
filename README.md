# Sv443-s-JokeAPI-Python-Wrapper

Just frickin

```python
  from jokeapi import Jokes

  j = Jokes()
  joke = j.get_joke()
  print(joke)
```
bam you got yourself a joke

The `get_joke()` function has multiple optional parameters:


`category` - a list of categories the joke should fit in. Possible entries are "Programming", "Miscellaneous" and "Dark". Leave blank for any.

`blacklist` - a list of things you don't *really* want to see. Maybe you're babysitting. Possible entries are "nsfw", "religious", "political", "racist" and "sexist"

`response_format` - a string which describes what format you want your response in. Default is json, and it will return a dict. Other options are "xml" and "yaml"

`type` - what type of joke it is. Defaults to use either. Possible options are "single" and "twopart"

`search_string` - string to search for in jokes. Defaults to None

`id_range` - a list (which should only contain two items) which describes the range in which to search for jokes, by joke id.

