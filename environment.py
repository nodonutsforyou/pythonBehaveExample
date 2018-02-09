import os


def before_all(context):
    print("before all")
    request_token_url = 'https://api.twitter.com/oauth/request_token'
    access_token_url = 'https://api.twitter.com/oauth/access_token'
    authorize_url = 'https://api.twitter.com/oauth/authorize'
    context.request_token_url = os.getenv('REQUEST_TOKEN_URL', 'https://api.twitter.com/oauth/request_token')
    context.access_token_url = os.getenv('ACCESS_TOKEN_URL', 'https://api.twitter.com/oauth/access_token')
    context.authorize_url = os.getenv('AUTH_TOKEN_URL', 'https://api.twitter.com/oauth/authorize')
    #TODO this assert is a wrong way to check if we got the parameter - but I do not have time to find the best one
    assert len(context.request_token_url) > 0, "TOKEN is not set - you need to set TOKEN environment variable"
    assert len(context.access_token_url) > 0, "TOKEN is not set - you need to set TOKEN environment variable"
    assert len(context.authorize_url) > 0, "TOKEN is not set - you need to set TOKEN environment variable"
