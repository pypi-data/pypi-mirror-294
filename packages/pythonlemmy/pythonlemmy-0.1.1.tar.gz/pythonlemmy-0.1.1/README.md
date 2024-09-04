# Pythonlemmy: a Python package for accessing the Lemmy API

<img src="https://github.com/Fedihosting-Foundation/plemmy/blob/main/img/plemmy.png" alt="drawing" width="325"/>

[![GitHub version](https://badge.fury.io/gh/Fedihosting-Foundation%2Fplemmy.svg)](https://badge.fury.io/gh/Fedihosting-Foundation%2Fplemmy)
[![PyPI version](https://badge.fury.io/py/plemmy.svg)](https://badge.fury.io/py/plemmy)
[![GitHub license](https://img.shields.io/badge/license-Apache-blue.svg)](https://raw.githubusercontent.com/Fedihosting-Foundation/plemmy/master/LICENSE.txt)

Pythonlemmy allows you to interact with any Lemmy instance using Python and the [LemmyHttp API](https://join-lemmy.org/api/classes/LemmyHttp.html).

**WARNING:** Pythonlemmy is still in development and needs testing!

## Installation ##

A PyPI repository is updated whenever a new version is available:

```
python -m pip install pythonlemmy
```

## Basic usage ##

Interact with a Lemmy instance using the _LemmyHttp_ object:

```python
from pythonlemmy import LemmyHttp

# create object for Lemmy.world, log in
srv = LemmyHttp("https://lemmy.world")
srv.login("<username_or_email>", "<password>")
```

Access specific communities:

```python
from pythonlemmy.responses import GetCommunityResponse

# obtain community, parse JSON
api_response = srv.get_community(name="Lemmy")
response = GetCommunityResponse(api_response)

# community info
community = response.community_view.community
print(community.name)
print(community.actor_id)
print(community.id)

# list community moderators
for person in response.moderators:
    print(person.moderator.name, person.community.name)
```

Create a post:

```python
from pythonlemmy.responses import PostResponse

# create post, parse JSON
api_response = srv.create_post(community.id, "Test post please ignore", "Body text")
response = PostResponse(api_response)

# post info
post = response.post_view.post
print(post.creator_id)
print(post.community_id)
print(post.name)
print(post.body)
```

Full documentation is on its way, but in the meantime check out our source code and some [examples](https://github.com/Fedihosting-Foundation/plemmy/tree/main/examples).

## Reporting issues, making contributions, etc. ##

Don't hesitate to report a bug or unexpected results! Want to contribute? Make a pull request. Contact [@tjkessler](https://github.com/tjkessler) with any questions.
