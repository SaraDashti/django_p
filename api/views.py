from rest_framework.generics import ListAPIView, RetrieveAPIView, DestroyAPIView, CreateAPIView, RetrieveUpdateAPIView
from .serializers import UserLoginSerializer, UserCreateSerializer, PostListSerializer, PostDetailSerializer, PostCreateUpdateSerializer, CommentListSerializer, CommentCreateSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from dj_p.models import Post
from .permissions import IsAuthor
from django.db.models import Q
from rest_framework.filters import SearchFilter, OrderingFilter
from django_comments.models import Comment
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.utils import timezone
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST


class UserLoginView(APIView):
	permission_classes = [AllowAny]
	serializer_class = UserLoginSerializer

	def post(self, request, format=None):
		data = request.data
		serializer = UserLoginSerializer(data=data)
		if serializer.is_valid(raise_exception=True):
			new_data = serializer.data
			return Response(new_data, status=HTTP_200_OK)
		return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class UserCreateView(CreateAPIView):
	queryset = User.objects.all()
	serializer_class = UserCreateSerializer

class CommentListView(ListAPIView):
	queryset = Comment.objects.all()
	serializer_class = CommentListSerializer
	permission_classes = [AllowAny]

	def get_queryset(self, *args, **kwargs):
		queryset = Comment.objects.all()
		query = self.request.GET.get("query")
		if query:
			queryset = queryset.filter(
				Q(object_pk=query)|
				Q(user=query)
				).distinct()
		return queryset

class CommentCreateView(CreateAPIView):
	queryset = Comment.objects.all()
	serializer_class = CommentCreateSerializer
	permission_classes=[IsAuthenticated]

	def perform_create(self, serializer):
		serializer.save(
			content_type=ContentType.objects.get_for_model(Post),
			site=Site.objects.get(id=1),
			user = self.request.user,
			user_name = self.request.user.username,
			submit_date = timezone.now()
		)

class PostListView(ListAPIView):
	queryset = Post.objects.all()
	serializer_class = PostListSerializer
	filter_backends = [SearchFilter, OrderingFilter]
	search_fields = ['title', 'content', 'author__username']
	permission_classes=[AllowAny]

	def get_queryset(self, *args, **kwargs):
		x = Post.objects.all()
		query = self.request.GET.get("query")
		if query:
			x = x.filter(
					Q(title__icontains=query)|
					Q(content__icontains=query)|
					Q(author__first_name__icontains=query)|
					Q(author__last_name__icontains=query)
				).distinct()
		return x

class PostCreateView(CreateAPIView):
	queryset = Post.objects.all()
	serializer_class = PostCreateUpdateSerializer
	permission_classes=[IsAuthenticated]

	def perform_create(self, serializer):
		serializer.save(author=self.request.user)


class PostDetailView(RetrieveAPIView):
	queryset = Post.objects.all()
	serializer_class = PostDetailSerializer
	lookup_field = 'slug'
	lookup_url_kwarg = 'post_slug'
	permission_classes=[AllowAny]



class PostDeleteView(DestroyAPIView):
	queryset = Post.objects.all()
	serializer_class = PostListSerializer
	lookup_field = 'slug'
	lookup_url_kwarg = 'post_slug'
	permission_classes=[IsAuthenticated, IsAdminUser]


class PostUpdateView(RetrieveUpdateAPIView):
	queryset = Post.objects.all()
	serializer_class = PostCreateUpdateSerializer
	lookup_field = 'slug'
	lookup_url_kwarg = 'post_slug'
	permission_classes=[IsAuthenticated, IsAuthor]
