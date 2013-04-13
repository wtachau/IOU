import oauth2
OAUTH_CONSUMER_KEY = 'VlTIjlyQYnnZ_1q3JoE73w'
OAUTH_CONSUMER_SECRET = '8kMrTChVZbNGLzglzgwik1hinT4'
OAUTH_TOKEN = 'w1tR4XWMdlyJpiNimEuowQMfOFvdOlBS'
OAUTH_TOKEN_SECRET = 'j6NE2U0jaESpKNMs0nQufhlM1rA'


def sign_url(url):
    consumer = oauth2.Consumer(OAUTH_CONSUMER_KEY, OAUTH_CONSUMER_SECRET)
    token = oauth2.Token(OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
    oauth_request = oauth2.Request('GET', url, {})
    oauth_request.update({'oauth_nonce': oauth2.generate_nonce(),
                          'oauth_timestamp': oauth2.generate_timestamp(),
                          'oauth_token': token.key,
                          'oauth_consumer_key': OAUTH_CONSUMER_KEY})
    oauth_request.sign_request(oauth2.SignatureMethod_HMAC_SHA1(),
                               consumer,
                               token)
    return oauth_request.to_url()
