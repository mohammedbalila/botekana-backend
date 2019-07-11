from distutils.util import strtobool
from django_filters import rest_framework
from rest_framework.filters import SearchFilter

from . import models


class ProductFilter(rest_framework.FilterSet):
    color = rest_framework.CharFilter(
        field_name='colors', lookup_expr='contains')
    brand = rest_framework.NumberFilter()
    price_min = rest_framework.NumberFilter(
        field_name="price", lookup_expr="gte"
    )
    price_max = rest_framework.NumberFilter(
        field_name="price", lookup_expr="lte"
    )
    quantity_min = rest_framework.NumberFilter(
        field_name="quantity", lookup_expr="gte"
    )
    quantity_max = rest_framework.NumberFilter(
        field_name="quantity", lookup_expr="lte"
    )

    class Meta:
        model = models.Product
        fields = ['category', 'sub_category']


class ProductSearchFilter(SearchFilter):
    search_field_prefix = "search_"

    def get_search_terms(self, request):
        # Get search fields from the class
        search_fields = getattr(request.resolver_match.func.view_class,
                                'search_fields', list())

        params = []

        # Iterate over each query parameter in the url
        for query_param in request.query_params:
            # Check if query parameter is a search parameter
            if query_param.startswith(self.search_field_prefix):
                # Extrapolate the field name while handling cases where
                # <ProductSearchFilter.search_field_prefix> is in
                # the field name.
                field = self.search_field_prefix.join(
                    query_param.split(self.search_field_prefix)[1:]
                )

                # Only apply search filter for fields that are in the view's
                # search_fields
                if field in search_fields:
                    params.append(request.query_params.get(query_param, ''))
        return params
