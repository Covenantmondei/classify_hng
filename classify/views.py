from .models import User
from .serializers import UserSerializer, GetUserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import httpx

GENDER_URL = 'https://api.genderize.io'
AGE_URL = 'https://api.agify.io'
COUNTRY_URL = 'https://api.nationalize.io'

class UserClassificationView(APIView):
    def post(self, request):
        try:
            name = request.data.get('name')
            if not name:
                return Response({'status': 'error', 'message': 'Name is required'}, status=status.HTTP_400_BAD_REQUEST)
            
            name = name.strip().lower()
            if name.isdigit():
                return Response({'status': 'error', 'message': 'Name cannot be a number'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
            
            stored_name = User.objects.filter(name__iexact=name).first()
            if stored_name:
                return Response({'status': 'success', 'message': 'Profile already exists', 'data': UserSerializer(stored_name).data}, status=status.HTTP_200_OK)
            
            # call external apis, get data and save to database
            try:
                gender_api_url = f"{GENDER_URL}?name={name}"
                age_api_url = f"{AGE_URL}?name={name}"
                country_api_url = f"{COUNTRY_URL}?name={name}"

                gender_response = httpx.get(gender_api_url)
                age_response = httpx.get(age_api_url)
                country_response = httpx.get(country_api_url)

                if gender_response.status_code != 200:
                    return Response({'status': 'error', 'message': 'Genderize returned an invalid response'}, status=status.HTTP_502_BAD_GATEWAY)
                if age_response.status_code != 200:
                    return Response({'status': 'error', 'message': 'Agify returned an invalid response'}, status=status.HTTP_502_BAD_GATEWAY)
                if country_response.status_code != 200:
                    return Response({'status': 'error', 'message': 'Nationalize returned an invalid response'}, status=status.HTTP_502_BAD_GATEWAY)
                
                gender_data = gender_response.json()
                age_data = age_response.json()
                country_data = country_response.json()

                # extract data from responses
                gender = gender_data.get('gender')
                gender_probability = gender_data.get('probability')
                sample_size = gender_data.get('count')

                if not gender or sample_size == 0:
                    return Response(
                        {'status': 'error', 'message': 'Genderize returned an invalid response'}, status=status.HTTP_502_BAD_GATEWAY)
                age = age_data.get('age')

                if age is None:
                    return Response(
                        {'status': 'error', 'message': 'Agify returned an invalid response'}, status=status.HTTP_502_BAD_GATEWAY)
                
                if age <= 12:
                    age_group = 'child'
                elif age <= 19:
                    age_group = 'teenager'
                elif age <= 59:
                    age_group = 'adult'
                else:
                    age_group = 'senior'    
                # age_group = 'child' if age < 18 else 'adult'

                                
                countries = country_data.get('country', [])
                if not countries:
                    return Response(
                        {'status': 'error', 'message': 'Nationalize returned an invalid response'},
                        status=status.HTTP_502_BAD_GATEWAY
                    )

                top_country = max(countries, key=lambda x: x['probability'])

                country_id = top_country['country_id']
                country_probability = top_country['probability']
                # country_id = country_data.get('country')[0].get('country_id') if country_data.get('country') else None
                # country_probability = country_data.get('country')[0].get('probability') if country_data.get('country') else None


                # save to database
                user = User.objects.create(
                    name=name,
                    gender=gender,
                    gender_probability=gender_probability,
                    sample_size=sample_size,
                    age=age,
                    age_group=age_group,
                    country_id=country_id,
                    country_probability=country_probability
                )

                return Response({'status': 'success', 'data': UserSerializer(user).data}, status=status.HTTP_201_CREATED)

            except Exception as e:
                return Response({'status': 'error', 'message': f'External API Error: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        except Exception as e:
            return Response({'status': 'error', 'message': f'Internal Server Error: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

    def get(self, request):
        try:
            users = User.objects.all()

            gender = request.query_params.get('gender')
            country_id = request.query_params.get('country_id')
            age_group = request.query_params.get('age_group')

            if gender:
                users = users.filter(gender__iexact=gender)
            if country_id:
                users = users.filter(country_id__iexact=country_id)
            if age_group:
                users = users.filter(age_group__iexact=age_group)

            serializer = GetUserSerializer(users, many=True)
            return Response({'status': 'success', 'count': users.count(), 'data': serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status': 'error', 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class GetSingleUserView(APIView):
    def get(self, request, user_id):
        try:
            user = User.objects.filter(id=user_id).first()
            if not user:
                return Response({'status': 'error', 'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
            serializer = UserSerializer(user)
            return Response({'status': 'success', 'data': serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status': 'error', 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

    def delete(self, request, user_id):
        try:
            user = User.objects.filter(id=user_id).first()
            if not user:
                return Response({'status': 'error', 'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({'status': 'error', 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)