from django.db import models
from django.core.urlresolvers import reverse

class Post(models.Model):
	title = models.CharField(max_length=255)
	content = models.TextField()
	updated = models.DateTimeField(auto_now=True)
	timestamp = models.DateTimeField(auto_now_add=True)
	img = models.ImageField(null=True, blank=True, upload_to="post_images")

	def __str__(self):
		return self.title


	def get_absolute_url(self):
		return reverse("detail", kwargs={"post_id":self.id})

	class Meta:
		ordering =['title']