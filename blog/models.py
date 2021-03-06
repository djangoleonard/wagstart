from __future__ import absolute_import, unicode_literals

# New imports added for forms and ParentalManyToManyField
from django import forms
from django.db import models

# New imports added for ClusterTaggableManager, TaggedItemBase, MultiFieldPanel

from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase

from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailsnippets.models import register_snippet
from wagtail.wagtailsearch import index


# ... (Keep the definition of BlogIndexPage)

class BlogIndexPage(Page):
    intro = RichTextField(blank=True)
    api_fields = ['intro']

    def get_context(self, request, *args, **kwargs):
        # Update context to include only published posts, ordered by reverse-chron
        context = super(BlogIndexPage, self).get_context(request)
        blogpages = BlogPage.objects.live().descendant_of(self)
        blogpagesspe = BlogPage.objects.live().descendant_of(self)
        blogparent = BlogIndexPage.objects.live().parent_of(self)    #.order_by('-name')
        blogdescen = BlogIndexPage.objects.live().child_of(self)
        # blogchild = BlogIndexPage.objects.live().descendant_of(self)
        context['blogpages'] = blogpages
        context['blogparent'] = blogparent
        context['blogdescen'] = blogdescen
        context['blogpagesspe'] = blogpagesspe
        return context

    # subpage_types = ['BlogPage']

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full")
    ]


class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey('BlogPage', related_name='tagged_items')


class BlogPage(Page):
    date = models.DateField("Post date")
    intro = models.CharField(max_length=250)
    body = RichTextField(blank=True)
    tags = ClusterTaggableManager(through=BlogPageTag, blank=True)
    categories = ParentalManyToManyField('blog.BlogCategory', blank=True)

    api_fields = ['date', 'intro', 'body', 'tags', 'categories']

    # ... (Keep the main_image method and search_fields definition)

    def main_image(self):
        gallery_item = self.gallery_images.first()
        if gallery_item:
            return gallery_item.image
        else:
            return None

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]
    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('date'),
            FieldPanel('tags'),
            FieldPanel('categories', widget=forms.CheckboxSelectMultiple),
        ], heading="Blog information"),
        FieldPanel('intro'),
        FieldPanel('body', classname="full"),
        InlinePanel('gallery_images', label="Gallery images"),
    ]

    # Specifies parent to BlogPage as being BlogIndexPages
    # parent_page_types = ['BlogIndexPage']

    # Specifies what content types can exist as children of BlogPage.
    # Empty list means that no child content types are allowed.
    # subpage_types = []


class BlogPageGalleryImage(Orderable):
    page = ParentalKey(BlogPage, related_name='gallery_images')
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
    )
    caption = models.CharField(blank=True, max_length=250)

    api_fields = ['page', 'image', 'caption']

    panels = [
        ImageChooserPanel('image'),
        FieldPanel('caption'),
    ]


class BlogTagIndexPage(Page):
    def get_context(self, request, *args, **kwargs):
        # Filter by tag
        tag = request.GET.get('tag')
        blogpages = BlogPage.objects.filter(tags__name=tag)
        # Update template context
        context = super(BlogTagIndexPage, self).get_context(request)
        context['blogpages'] = blogpages
        return context


@register_snippet
class BlogCategory(models.Model):
    name = models.CharField(max_length=255)
    icon = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='+'
    )

    api_fields = ['name', 'icon']

    panels = [
        FieldPanel('name'),
        ImageChooserPanel('icon'),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'blog categories'
