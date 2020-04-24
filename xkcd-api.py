#!/usr/bin/python

import requests, json, fire, os

slack_webhook_url = os.environ['XKCD_SLACK_WEBHOOK_URL']
slack_headers={'Content-Type': 'application/json'}

def slack_post(content):
    _slack_post = requests.post(slack_webhook_url, data=json.dumps(content), headers=slack_headers)
    return(_slack_post.text)

def slack_content_build(title, image, alt):
    _output = {"text": "*{0}*\n{1}\n{2}".format(title,alt,image)}
    return(_output)

# class named Get for cli usability 
class Get(object):

    def comic_current(self):
        _current_comic = requests.get("https://xkcd.com/info.0.json").json()
        _title = _current_comic["title"]
        _alt = _current_comic["alt"]
        _image = _current_comic["img"]
        _content = slack_content_build(_title, _image, _alt)
        slack_post(_content)

    def comic_by_id(self, comic_id):
        _comic = requests.get("https://xkcd.com/{0}/info.0.json".format(comic_id)).json()
        _title = _comic["title"]
        _alt = _comic["alt"]
        _image = _comic["img"]
        _content = slack_content_build(_title, _image, _alt)
        slack_post(_content)

class Pipeline(object):
    
    def __init__(self):
        self.get = Get()

if __name__ == '__main__':
    fire.Fire(Pipeline)
