from rest_framework import serializers
from dj_p.models import Post
from django_comments.models import Comment
from django.contrib.auth.models import User
from rest_framework_jwt.settings import api_settings

class UserLoginSerializer(serializers.Serializer):
	username = serializers.CharField()
	password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
	token = serializers.CharField(allow_blank=True, read_only=True)

	def validate(self, data):
		username = data.get('username')
		password = data.get('password')

		if username == '':
			raise serializers.ValidationError("A username is required to login.")

		user = User.objects.filter(username=username)
		if user.exists():
			user_obj = user.first()
		else:
			raise serializers.ValidationError("This username is not valid. *facepalm*")

		if user_obj:
			if not user_obj.check_password(password):
				raise serializers.ValidationError("This credentials, please try again.")

		jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
		jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

		payload = jwt_payload_handler(user_obj)
		token = jwt_encode_handler(payload)
		data["token"] = token
		return data

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ['email', 'username', 'first_name', 'last_name']

class UserCreateSerializer(serializers.ModelSerializer):
	password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
	class Meta:
		model = User
		fields = ['username', 'password', 'email']

	def create(self, validated_data):
		username = validated_data['username']
		password = validated_data['password']
		new_user = User(username=username)
		new_user.set_password(password)
		new_user.save()
		return validated_data

class CommentListSerializer(serializers.ModelSerializer):
	class Meta:
		model = Comment
		fields = ['object_pk','user','comment','submit_date']

class CommentCreateSerializer(serializers.ModelSerializer):
	class Meta:
		model = Comment
		fields = ['object_pk','comment']


class PostListSerializer(serializers.ModelSerializer):
	author = UserSerializer()
	detail_page = serializers.HyperlinkedIdentityField(
			view_name = "api:detail",
			lookup_field = "slug",
			lookup_url_kwarg = "post_slug"
		)
	class Meta:
		model = Post
		fields =['title', 'author', 'publish_date', 'detail_page', 'author']

	def get_author(self, obj):
		return str(obj.author.username)

class PostDetailSerializer(serializers.ModelSerializer):
	author = UserSerializer()
	update_page = serializers.HyperlinkedIdentityField(
			view_name = "api:update",
			lookup_field = "slug",
			lookup_url_kwarg = "post_slug"
		)
	delete_page = serializers.HyperlinkedIdentityField(
			view_name = "api:delete",
			lookup_field = "slug",
			lookup_url_kwarg = "post_slug"
		)
	class Meta:
		model = Post
		fields ="__all__"

	def get_author(self, obj):
		return str(obj.author.username)

	def get_comments(self, obj):
		comment_list = Comment.objects.filter(object_pk=obj.id)
		comments = CommentListSerializer(comment_list, many=True).data
		return comments

class PostCreateUpdateSerializer(serializers.ModelSerializer):
	class Meta:
		model = Post
		fields =['title', 'content', 'publish_date', 'draft', 'img']
		