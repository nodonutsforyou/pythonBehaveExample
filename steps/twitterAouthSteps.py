import requests
from behave import *
import json
import urlparse
# from urllib.parse import urlparse
import oauth2 as oauth
import os


def twitterOAUTH(context, user, key, secret):
    #TODO - some code from google - i do not know how it works and I do not have twitter account with app to check it
    consumer = oauth.Consumer(key, secret)
    client = oauth.Client(consumer)
    context.resp, context.content = client.request(context.request_token_url, "GET")
    if context.resp['status'] != '200':
        return context.resp
    context.request_token = dict(urlparse.parse_qsl(content))
    accepted = 'n'
    while accepted.lower() == 'n':
        accepted = raw_input('Have you authorized me? (y/n) ')
    context.oauth_verifier = raw_input('What is the PIN? ')
    context.token = oauth.Token(context.request_token['oauth_token'],
                                context.request_token['oauth_token_secret'])
    context.token.set_verifier(context.oauth_verifier)
    context.client = oauth.Client(consumer, context.token)
    context.resp, context.content = client.request(context.access_token_url, "POST")
    context.access_token = dict(urlparse.parse_qsl(context.content))
    #TODO hire I assume that good response never == 0. That should probobly be true - but need to check
    return 0

def getRateLimit(context):
    #TODO better way to get this - somewhere from database. We shouldn't rely on api calls for that
    if 'rateLimit' in context:
        return context.rateLimit-1
    return 100


@given(u'we login with {user} and keys from environment variables {keyVar} and {secretVar}')
def step_impl(context, user, keyVar, secretVar):
    context.key = os.getenv(keyVar) #TODO check if variable exists and not empty
    context.secret = os.getenv(secretVar) #TODO check if variable exists and not empty
    twitterOAUTH(context, 'testUser', context.key, context.secret)

@then(u'user logged in successfully')
def step_impl(context):
    #TODO here I assume that resp to spring is enough to get full description of an error - probobly not
    assert context.resp['status'] == '200', "login was not successful: " + context.resp
    #TODO here I assume code 200 is enough to understand if user is logged in - but we need to check something else, like do a health check

@then(u'user have been redirected to redirected url')
def step_impl(context):
    print("test message")
    #TODO we need some kind of mock which logs our redirects.
    #TODO step should check if that mock got our redirect once

@given(u'we login with {user} and keys {key} and secret from environment variable {secretVar}')
def step_impl(context, user, key, secretVar):
    context.key = key
    context.secret = os.getenv(secretVar) #TODO check if variable exists and not empty
    twitterOAUTH(context, 'testUser', context.key, context.secret)

@then(u'we get error from API')
def step_impl(context):
    #TODO we need a way more description in case when login was success and we expected otherwise
    assert context.resp['status'] != '200', "login was successful: " + context.resp
    #TODO here I assume code 200 is enough to understand if user is logged in - but we need to check something else, like do a health check

@given(u'we login with {user} and keys from environment variable {keyVar} and secret {secret}')
def step_impl(context, user, keyVar, secret):
    context.key = os.getenv(keyVar) #TODO check if variable exists and not empty
    context.secret = secret
    twitterOAUTH(context, 'testUser', context.key, context.secret)

@given(u'rate limit for testUser is bigger than zero')
def step_impl(context):
    #TODO better way to get this - somewhere from database. We shouldn't rely on api calls for that
    context.rateLimit = getRateLimit(context)
    assert context.rateLimit>0, "rate limit for a test user is lower that zero: " + str(context.rateLimit)

@then(u'rate limit is lower by 1')
def step_impl(context):
    newRateLimit = getRateLimit(context)
    assert context.rateLimit - 1 == newRateLimit, "rate limit changed more then expected. expected:" + str(newRateLimit) + " actual:" + str(newRateLimit -1)
    context.rateLimit = newRateLimit

@given(u'we login rate limit times')
def step_impl(context):
    context.key = os.getenv("KEY")  # TODO check if variable exists and not empty
    context.secret = os.getenv("SECRET")  # TODO check if variable exists and not empty
    for i in range(context.rateLimit - 1):
        twitterOAUTH(context, 'testUser', context.key, context.secret)
        raise NotImplementedError(u'STEP: login rate limit times')

@then(u'rate limit is {count}')
def step_impl(context, count):
    context.rateLimit = getRateLimit(context)
    assert context.rateLimit == count, "rate limit is not as expected" #TODO ouptu more info - expected/actual

@then(u'we get error from API which states that rate limit is reached')
def step_impl(context):
    #TODO have no idea what this rate error may look like
    #TODO we need a way more description in case when login was success and we expected otherwise
    assert context.resp['status'] != '200', "login was successful: " + context.resp
    #TODO here I assume code 200 is enough to understand if user is logged in - but we need to check something else, like do a health check


@given(u'we login with very long username')
def step_impl(context):
    username = "verylongUsername"
    for i in range(256): #256 looks like long enough to be too big
        username+="1" #TODO may change it with something pre-generated
    context.key = os.getenv("KEY")  # TODO check if variable exists and not empty
    context.secret = os.getenv("SECRET")  # TODO check if variable exists and not empty
    twitterOAUTH(context, 'testUser', context.key, context.secret)
