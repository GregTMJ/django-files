from django_filters import FilterSet
from .models import Comments

"""
define the name of your filter, and don't forget the imported father 
class (FilterSet)
"""


class SearchFilter(FilterSet):

    class Meta:
        """
           Meta is used to create a class that stores optional information,
           not main, ex. here from model Post, you get the field author,
           text and etc...
        """

        model = Comments
        fields = ('post',)
