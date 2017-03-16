# Parents and Children
Much of the work you’ll be doing inWagtail revolves around the concept of hierarchical “tree” structures consisting of
nodes and leaves (see Theory). In this case, the BlogIndexPage is a “node” and individual BlogPage instances
are the “leaves”.
Take another look at the guts of blog_index_page.html:

{% for post in page.get_children %}
<h2><a href="{% pageurl post %}">{{ post.title }}</a></h2>
{{ post.specific.intro }}
{{ post.specific.body|richtext }}
{% endfor %}

Every “page” in Wagtail can call out to its parent or children from its own position in the hierarchy. But why do we
have to specify post.specific.intro rather than post.intro? This has to do with the way we defined our
model:

class BlogPage(Page):
The get_children() method gets us a list of instances of the Page base class. When we want to reference
properties of the instances that inherit from the base class, Wagtail provides the specific method that retrieves the
actual BlogPage record. While the “title” field is present on the base Page model, “intro” is only present on the
BlogPage model, so we need .specific to access it.

# Given a page object 'somepage':
MyModel.objects.descendant_of(somepage)
child_of(page) / not_child_of(somepage)
ancestor_of(somepage) / not_ancestor_of(somepage)
parent_of(somepage) / not_parent_of(somepage)
sibling_of(somepage) / not_sibling_of(somepage)
# ... and ...
somepage.get_children()
somepage.get_ancestors()
somepage.get_descendants()
somepage.get_siblings()

# Images
Inheriting from Orderable adds a sort_order field to the model, to keep track of the ordering of images in the
gallery.

The ParentalKey to BlogPage is what attaches the gallery images to a specific page. A ParentalKey works
similarly to a ForeignKey, but also defines BlogPageGalleryImage as a “child” of the BlogPage model, so
that it’s treated as a fundamental part of the page in operations like submitting for moderation, and tracking revision
history.

image is a ForeignKey to Wagtail’s built-in Image model, where the images themselves are stored. This comes
with a dedicated panel type, ImageChooserPanel, which provides a pop-up interface for choosing an existing
image or uploading a new one. This way, we allow an image to exist in multiple galleries - effectively, we’ve created
a many-to-many relationship between pages and images.

Specifying on_delete=models.CASCADE on the foreign key means that if the image is deleted from the system,
the gallery entry is deleted as well. (In other situations, it might be appropriate to leave the entry in place - for
example, if an “our staff” page included a list of people with headshots, and one of those photos was deleted, we’d
rather leave the person in place on the page without a photo. In this case, we’d set the foreign key to blank=True,
null=True, on_delete=models.SET_NULL.)

Finally, adding the InlinePanel to BlogPage.content_panels makes the gallery images available on the
editing interface for BlogPage.

Since our gallery images are database objects in their own right, we can now query and re-use them independently
of the blog post body. Let’s define a main_image method, which returns the image from the first gallery item (or
None if no gallery items exist):


Note that this Page-based model defines no fields of its own. Even without fields, subclassing Page makes it a part of
theWagtail ecosystem, so that you can give it a title and URL in the admin, and so that you can manipulate its contents
by returning a queryset from its get_context() method.
Migrate this in, then create a new BlogTagIndexPage in the admin. You’ll probably want to create the new
page/view under Homepage, parallel to your Blog index. Give it the slug “tags” on the Promote tab.
Access /tags and Django will tell you what you probably already knew: you need to create a template
blog/blog_tag_index_page.html:

First, we define a BlogCategory model. A category is not a page in its own right, and so we define it as a standard
Django models.Model rather than inheriting from Page. Wagtail introduces the concept of “snippets” for reusable
pieces of content that need to be managed through the admin interface, but do not exist as part of the page tree
themselves; a model can be registered as a snippet by adding the @register_snippet decorator. All the field
types we’ve used so far on pages can be used on snippets too - here we’ll give each category an icon image as well as
a name. Add to blog/models.py:

Note: Note that we are using panels rather than content_panels here - since snippets generally have no need
for fields such as slug or publish date, the editing interface for them is not split into separate ‘content’ / ‘promote’ /
‘settings’ tabs as standard, and so there is no need to distinguish between ‘content panels’ and ‘promote panels’.