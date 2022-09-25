from django.contrib import admin
from polls.models import Question, Choice


# Register your models here.


# class ChoiceInline(admin.StackedInline):
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 1


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]

    list_display = ('id', 'question_text', 'pub_date', 'was_published_recently')
    list_filter = ["pub_date"]
    # list_filter = ["question_text"]
    search_fields = ['question_text']
    ordering = ["-id"]


admin.site.register(Question, QuestionAdmin)
