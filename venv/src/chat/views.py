from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from chat.models import PrivateChatRoom, RoomChatMessage
from friend.models import FriendList
import json
from account.models import Account
from itertools import chain
from chat.utils import find_or_create_private_chat

DEBUG = False

def private_chat_room_view(request, *args, **kwargs):
	room_id = request.GET.get("room_id")
	user = request.user
	context = {}
	if room_id:
		try :
		   room = PrivateChatRoom.objects.get(pk=room_id)
		   context['room'] = room
		except PrivateChatRoom.DoesNotExist:
			pass
	if not user.is_authenticated:
		return redirect("login")
	# 1. Find all the rooms this user is a part of 
	rooms1 = PrivateChatRoom.objects.filter(user1=user, is_active=True)
	rooms2 = PrivateChatRoom.objects.filter(user2=user, is_active=True)

	# 2. merge the lists
	rooms = list(chain(rooms1, rooms2))
	"""
	m_and_f
	[{"message":"hey","friend":"Mitch"},{"message":"hello","friend":"Blake"}]
	"""
	m_and_f = []
	for room in rooms:
		# Figure out which user is the "other user" (aka friend)
		if room.user1 == user:
			friend = room.user2
		else:
			friend = room.user1
		m_and_f.append({"message":"","friend":friend})
	# confirm you are even friends (in case chat is left active somehow)
	context['m_and_f'] = m_and_f
	context['debug'] = DEBUG
	context['debug_mode'] = settings.DEBUG
	return render(request, "chat/room.html", context)


# Ajax call to return a private chatroom or create one if does not exist
def create_or_return_private_chat(request, *args, **kwargs):
	user1 = request.user
	payload = {}
	if user1.is_authenticated:
		if request.method == "POST":
			user2_id = request.POST.get("user2_id")
			try:
				user2 = Account.objects.get(pk=user2_id)
				chat = find_or_create_private_chat(user1, user2)
				print("Successfully got the chat")
				payload['response'] = "Successfully got the chat."
				payload['chatroom_id'] = chat.id
			except Account.DoesNotExist:
				payload['response'] = "Unable to start a chat with that user."
	else:
		payload['response'] = "You can't start a chat if you are not authenticated."
	return HttpResponse(json.dumps(payload), content_type="application/json")
