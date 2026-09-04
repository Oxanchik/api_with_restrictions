from django_filters import rest_framework as filters

from listings.models import Advertisement


class AdvertisementFilter(filters.FilterSet):
    """Фильтры для объявлений."""

    # DateFromToRangeFilter для фильтрации по дате
    created_at = filters.DateFromToRangeFilter()

    class Meta:
        model = Advertisement
        fields = ['status', 'created_at']
