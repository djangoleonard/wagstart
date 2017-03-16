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