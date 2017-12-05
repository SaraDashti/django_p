from django.http import JsonResponse
from urllib.parse import quote
from allauth.socialaccount.admin import SocialApp
import requests
from requests_oauthlib import OAuth1


def tweet_search(request):
	search_term = "#Python"
	query = quote(search_term)
	url = "https://api.twitter.com/1.1/search/tweets.json?q=%s"%(query)



	user = request.user
	social_account = user.socialaccount_set.get(user=user.id)
	social_token = social_account.socialtoken_set.get(account=social_account.id)
	token = social_token.token
	token_secret = social_token.token_secret

	social_app = SocialApp.objects.get(provider=social_account.provider)
	client_id = social_app.client_id
	client_secret = social_app.secret

	auth_value = OAuth1(client_id, client_secret, token, token_secret)

	resp = requests.get(url, auth=auth_value)

	return JsonResponse(resp.json(), safe=False)