from django.contrib import admin
from .models import User
from .models import News
from .models import Statement
from .models import Cup
from .models import ConstructorsCup
from .models import Schedule
from .models import Posts
from .models import Comments
from .models import Group
from .models import GroupMembership
from .models import DiscussionTopic
from .models import Meme
from .models import Tag

admin.site.register(User)
admin.site.register(News)
admin.site.register(Statement)
admin.site.register(Cup)
admin.site.register(ConstructorsCup)
admin.site.register(Schedule)
admin.site.register(Posts)
admin.site.register(Comments)
admin.site.register(Group)
admin.site.register(GroupMembership)
admin.site.register(DiscussionTopic)
admin.site.register(Meme)
admin.site.register(Tag)


