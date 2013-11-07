from django.db import models
from django.template.defaultfilters import slugify

from athumb.fields import ImageWithThumbsField


def upload_image_name(instance, filename):
    result = 'hhgallery/uploads/'
    result += slugify(instance.gallery.name)+'-'
    return result+str(ImageUpload.objects.count())+'-'+filename


class Gallery(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(default='slug')

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)
        super(Gallery, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name

class ImageUpload(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    email = models.EmailField()
    artist = models.CharField(max_length=100)
    gallery = models.ForeignKey(Gallery, blank=False, null=False, related_name='images')
    approved = models.BooleanField(default=False, blank=True)
    image = ImageWithThumbsField(
        upload_to=upload_image_name,
        thumbs=(
            ('galthumb', {'size': (192, 192)}),
            #('blog_huge', {'size': (588, 1200)}),
            ('massive', {'size': (1280, 720)})
        ))

    def __unicode__(self):
        return self.image.name

