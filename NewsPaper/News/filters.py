from django_filters import FilterSet
from .models import Posts


class SearchFilter(FilterSet):
    class Meta:
        model = Posts
        fields = ('Author',
                  'text',
                  'time_in',
                  'category',
                  'rating',
                  )
