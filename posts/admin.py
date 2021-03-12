from django import forms
from django.contrib import admin
from django.utils.safestring import mark_safe
from ckeditor.widgets import CKEditorWidget

from .models import Follow, Group, Post, Comment, Tag


class PostAdminForm(forms.ModelForm):
    text = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = Post
        fields = '__all__'


class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm
    list_display = ('id', 'text', 'pub_date', 'author',
                    'group', 'get_image')
    search_fields = ('text',)
    list_filter = ('pub_date', 'group')
    readonly_fields = ('get_image', 'pub_date')
    fields = ('author', 'text', 'image', 'get_image',
              'pub_date', 'tags', 'likes', 'dislikes')
    save_on_top = True
    save_as = True
    list_per_page = 30
    empty_value_display = '-пусто-'

    def get_image(self, obj):
        if obj.image:
            return mark_safe(
                f'<img src="{obj.image.url}" width="50">'
            )
        return '-пусто-'

    get_image.short_description = 'Миниатюра'


class GroupAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'slug', 'description')
    prepopulated_fields = {'slug': ('title',)}
    empty_value_display = '-пусто-'


class FollowAdmin(admin.ModelAdmin):
    list_display = ('user', 'author')
    empty_value_display = '-пусто-'


class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'get_text', 'created')
    search_fields = ('text',)
    list_filter = ('created',)
    empty_value_display = '-пусто-'

    def get_text(self, obj):
        return obj.text[:300]

    get_text.short_description = "Текст"


class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'slug')
    search_fields = ('title',)
    list_filter = ('title',)


admin.site.register(Follow, FollowAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Tag, TagAdmin)
