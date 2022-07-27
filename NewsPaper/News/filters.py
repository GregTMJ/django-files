from django_filters import FilterSet
from .models import Posts


# Adding a filter query to the search view
class SearchFilter(FilterSet):
    class Meta:
        model = Posts
        fields = ('Author',
                  'text',
                  'time_in',
                  'category',
                  'rating',
                  )
