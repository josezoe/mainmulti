



from rest_framework import viewsets
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from ..models import CustomUser, Vendor, Country, State, City, Timezone
from ..serializers import CustomUserSerializer, VendorSerializer, CountrySerializer, StateSerializer, CitySerializer, TimezoneSerializer
from rest_framework import generics
from rest_framework.authtoken.models import Token



class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    
class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
             'user_id':user.unique_id,
              'user_type': user.user_type,
        })

class CountryList(generics.ListAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = [AllowAny]

class CountryDetail(generics.RetrieveAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = [AllowAny]

class CountryCreate(generics.CreateAPIView):
    serializer_class = CountrySerializer
    permission_classes = [AllowAny]
    
class CountryUpdate(generics.UpdateAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = [AllowAny]

class CountryDelete(generics.DestroyAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = [AllowAny]


class StateList(generics.ListAPIView):
    queryset = State.objects.all()
    serializer_class = StateSerializer
    permission_classes = [AllowAny]

class StateDetail(generics.RetrieveAPIView):
    queryset = State.objects.all()
    serializer_class = StateSerializer
    permission_classes = [AllowAny]

class StateCreate(generics.CreateAPIView):
    serializer_class = StateSerializer
    permission_classes = [AllowAny]
    
class StateUpdate(generics.UpdateAPIView):
    queryset = State.objects.all()
    serializer_class = StateSerializer
    permission_classes = [AllowAny]

class StateDelete(generics.DestroyAPIView):
    queryset = State.objects.all()
    serializer_class = StateSerializer
    permission_classes = [AllowAny]

class CityList(generics.ListAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = [AllowAny]

class CityDetail(generics.RetrieveAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = [AllowAny]

class CityCreate(generics.CreateAPIView):
    serializer_class = CitySerializer
    permission_classes = [AllowAny]
    
class CityUpdate(generics.UpdateAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = [AllowAny]

class CityDelete(generics.DestroyAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = [AllowAny]

class TimezoneList(generics.ListAPIView):
    queryset = Timezone.objects.all()
    serializer_class = TimezoneSerializer
    permission_classes = [AllowAny]

class TimezoneDetail(generics.RetrieveAPIView):
    queryset = Timezone.objects.all()
    serializer_class = TimezoneSerializer
    permission_classes = [AllowAny]
    
class TimezoneCreate(generics.CreateAPIView):
    serializer_class = TimezoneSerializer
    permission_classes = [AllowAny]

class TimezoneUpdate(generics.UpdateAPIView):
    queryset = Timezone.objects.all()
    serializer_class = TimezoneSerializer
    permission_classes = [AllowAny]

class TimezoneDelete(generics.DestroyAPIView):
    queryset = Timezone.objects.all()
    serializer_class = TimezoneSerializer
    permission_classes = [AllowAny]

class CustomUserList(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]

class CustomUserDetail(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]

class VendorList(generics.ListAPIView):
     queryset = Vendor.objects.all()
     serializer_class = VendorSerializer
     permission_classes = [IsAuthenticated]

class VendorDetail(generics.RetrieveAPIView):
     queryset = Vendor.objects.all()
     serializer_class = VendorSerializer
     permission_classes = [IsAuthenticated]