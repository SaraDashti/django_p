from django.shortcuts import render
from django.http import JsonResponse
import requests

def member_list(request):
	sara = request.user

	social_account = sara.socialaccount_set.get(user=sara.id)
	social_token = social_account.socialtoken_set.get(account=social_account.id)
	token = social_token.token

	#url = "https://api.github.com/orgs/joinCODED/members"
	url = "https://api.github.com/users/SaraDashti/repos"
	res = requests.get(url, headers={"Authorization": "token "+token})
	return JsonResponse(res.json(), safe=False)

