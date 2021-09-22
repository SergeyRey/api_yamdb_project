from django_filters import rest_framework as filt

from reviews.models import Title


class TitlesFilter(filt.FilterSet):
    category = filt.CharFilter(
        field_name='category__slug',
        lookup_expr='icontains',
    )
    genre = filt.CharFilter(
        field_name='genre__slug',
        lookup_expr='icontains',
    )
    name = filt.CharFilter(
        field_name='name',
        lookup_expr='icontains',
    )

    class Meta:
        model = Title
        fields = ('category', 'genre', 'name', 'year')
