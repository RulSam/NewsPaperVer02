from django.forms import DateTimeInput
from django_filters import FilterSet, DateTimeFilter, CharFilter, ChoiceFilter
from .models import Post

class PostFilter(FilterSet):
    dateTimeCreation = DateTimeFilter(
        field_name='dateCreation',
        lookup_expr='gt',
        label='Дата позже',
        widget=DateTimeInput(
            format='%Y-%m-%dT%H:%M',
            attrs={'type': 'datetime-local'},
        )

    )
    title = CharFilter(
        field_name='title',
        label='Заголовок'
    )

    categoryType = ChoiceFilter(
        field_name='categoryType',
        label='Категория',
        choices=Post.CATEGORY_CHOICES
    )

    class Meta:
        model = Post
        fields = {
            'title': ['exact'],
            'categoryType': ['exact'],
        }

