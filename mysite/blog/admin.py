from django.contrib import admin
from .models import Post, Comment, Summary, Connections, Exchanges


admin.site.site_url = "/blog"


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'publish', 'status')
    list_filter = ('status', 'created', 'publish', 'author')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'post', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email', 'body')


@admin.register(Summary)
class Summary(admin.ModelAdmin):
    list_display = ('status', 'czas', 'timestamp', 'zapotrzebowanie', 'generacja', 'czestotliwosc', 'cieplne', 'PV', 'wiatrowe', 'wodne', 'inne')


@admin.register(Connections)
class Connections(admin.ModelAdmin):
    list_display = ('timestamp_id', 'status', 'czas', 'timestamp',)


@admin.register(Exchanges)
class Exchanges(admin.ModelAdmin):
    list_display = ('status', 'czas', 'timestamp', 'importt', 'eksport', 'saldo')

# Register your models here.
