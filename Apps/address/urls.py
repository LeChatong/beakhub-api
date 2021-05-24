from django.urls import path

from Apps.address.views import CountryListView, CountryDetailView, CityListView, CityDetailView, ZoneListView, \
    ZoneDetailsView, AddressListCreateView, AddressDetailsView

urlpatterns = [
    path(r'', AddressListCreateView.as_view(), name='address-list'),
    path(r'<str:pk>/', AddressDetailsView.as_view(), name='address-detail'),
    path(r'country/', CountryListView.as_view(), name='country-list'),
    path(r'country/<str:pk>/', CountryDetailView.as_view(), name='country-detail'),
    path(r'city/', CityListView.as_view(), name='city-list'),
    path(r'city/<str:pk>/', CityDetailView.as_view(), name='city-detail'),
    path(r'zone/', ZoneListView.as_view(), name='zone-list'),
    path(r'zone/<str:pk>/', ZoneDetailsView.as_view(), name='zone-detail'),
]
