from django_filters import FilterSet
from .models import Post


class SearchFilter(FilterSet):
    class Meta:
        model = Post
        fields = ('author',
                  'text',
                  'time_in',
                  'category',
                  'rating',
                  )
