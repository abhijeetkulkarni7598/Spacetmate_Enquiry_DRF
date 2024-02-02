# views.py
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from . models import *
from api.models import Quotation, Item
from . serializers import *
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User

from api.mypagination import MyLimit
from django.db.models import Q


class EnquireViewSet(viewsets.ModelViewSet):
    queryset = Enquire.objects.all()
    serializer_class = EnquireSerializer
    pagination_class = MyLimit
    permission_classes = [permissions.AllowAny]
    parser_classes = (MultiPartParser, FormParser)
    def get_queryset(self):
       from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from django.db.models import Q
from .models import Enquire
from .serializers import EnquireSerializer
from api.serializers import QuotationSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from api.mypagination import MyLimit

class EnquireViewSet(viewsets.ModelViewSet):
    queryset = Enquire.objects.all()
    serializer_class = EnquireSerializer
    pagination_class = MyLimit
    permission_classes = [permissions.AllowAny]
    parser_classes = (MultiPartParser, FormParser)

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.query_params.get("user")
        name = self.request.query_params.get("name")
        status = self.request.query_params.get("status")

        if name:
            queryset = queryset.filter(
                Q(name__icontains=name)
            )

        if user:
            queryset = queryset.filter(user=user)
        if status:
            queryset = queryset.filter(status=status)

        return queryset
    @action(detail=True, methods=['GET'], url_path='get_prospect_enquiry')
    def get_prospect_enquiry(self, request, pk=None):
        enquire_instance = self.get_object()

        # Check if the status is 'Prospect'
        if enquire_instance.status == 'Prospect':
            serializer = self.get_serializer(enquire_instance)
            latest_quotation = enquire_instance.quotation_set.order_by('-id').first()
            quotation_data = QuotationSerializer(latest_quotation).data if latest_quotation else []

            enquire_data = serializer.data
            enquire_data['quotations'] = quotation_data

            return Response(enquire_data, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Enquire is not a Prospect'}, status=status.HTTP_404_NOT_FOUND)
    def post(self, request, *args, **kwargs):
        # Extract data from the request
        name = request.data.get('name', None)
        mobile = request.data.get('mobile', None)
        email = request.data.get('email', None)
        address = request.data.get('address', None)
        requirement = request.data.get('requirement', None)
        floor_plain = request.data.get('floor_plain', None)
        user = request.data.get('user', None)
       
        # Validate that required fields are present
        if not all([name, mobile, email, address, requirement, floor_plain]):
            return Response({'error': 'Incomplete data provided'}, status=status.HTTP_400_BAD_REQUEST)

        # Create a new Enquire instance with the provided data
        enquire = Enquire(
            name=name,
            mobile=mobile,
            email=email,
            address=address,
            requirement=requirement,
            floor_plain=floor_plain,
            user=user,
        )

        enquire.full_clean()  # Validate model fields
        enquire.save()

        serializer = EnquireSerializer(enquire)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance.floor_plain:
            instance.floor_plain.delete()

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['DELETE'], url_path='delete_quotations_items')
    def delete_quotations_items(self, request, pk=None):
        enquire_instance = self.get_object()

        # Delete associated quotations and items
        quotations = Quotation.objects.filter(enquiry=enquire_instance)
        for quotation in quotations:
            # Delete associated items for each quotation
            items = Item.objects.filter(quotation=quotation)
            for item in items:
                try:
                    if item.image:
                        item.image.delete()
                except Exception as e:
                    # Handle the exception here
                    print(f"An error occurred while deleting the item image: {e}")
                item.delete()

            quotation.delete()

        return Response({'detail': 'Quotations and items deleted successfully'}, status=status.HTTP_200_OK)     
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        # Extract data from the request
        name = request.data.get('name', instance.name)
        mobile = request.data.get('mobile', instance.mobile)
        email = request.data.get('email', instance.email)
        address = request.data.get('address', instance.address)
        requirement = request.data.get('requirement', instance.requirement)
        floor_plain = request.data.get('floor_plain', instance.floor_plain)
        status2 = request.data.get('status', instance.status)
        # user = request.data.get('user', instance.user)
        user = request.data.get('user', instance.user)
   
        # Validate that required fields are present
        if not all([name, mobile, email, address,status2]):
            return Response({'error': 'Incomplete data provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            if(user):
                user_instance = UserAccount.objects.get(id=user)
                instance.user = user_instance

        except UserAccount.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        # Update the Enquire instance with the provided data
        instance.name = name
        instance.mobile = mobile
        instance.email = email
        instance.address = address
        instance.requirement = requirement
        instance.status = status2
        # Set the new floor_plain image
        #instance.floor_plain = floor_plain

        # Check if the 'floor_plain' field is present in the request data
        if 'floor_plain' in request.data:
        # Set the new floor_plain image
            instance.floor_plain = request.data['floor_plain']

            # Only update 'floor_plain' if a new file is provided
            if 'floor_plain' in request.data:
                instance.floor_plain = floor_plain

        instance.full_clean()  # Validate model fields
        instance.save()

        serializer = EnquireSerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DesignViewSet(viewsets.ModelViewSet):
    queryset = Design.objects.all()
    serializer_class = DesignSerializer
    permission_classes = [permissions.AllowAny]
    parser_classes = (MultiPartParser, FormParser)

    pagination_class = MyLimit

    def get_queryset(self):
        queryset = super().get_queryset()
        enquiry = self.request.query_params.get("enquiry")
        approval = self.request.query_params.get("approval")

    
        if enquiry:
            queryset = queryset.filter(enquiry=enquiry)
        if approval:
            queryset = queryset.exclude(approval=approval)
     

        return queryset
    def create(self, request, *args, **kwargs):
        # Initialize lists to store titles, images, and designs
        titles = []
        images = []
        designs = []

        # Loop through form data keys and separate titles and images
        for key, value in request.data.items():
            if key.startswith('title'):
                titles.append(value)
            elif key.startswith('image'):
                images.append(value)

        # Validate that required fields are present
        if not all([titles, images]):
            return Response({'error': 'Incomplete data provided'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the associated User instance exists
        enquiry_id = request.data.get('enquiry', None)
        enquiry = get_object_or_404(Enquire, id=enquiry_id)

        # Create a new Design instance for each title and image pair
        for title, image in zip(titles, images):
            design = Design(
                title=title,
                image=image,
                enquiry=enquiry,
                approval=request.data.get('Approved', 'Rejected')  # You may adjust the default value
            )

            design.full_clean()  # Validate model fields
            design.save()
            designs.append(design)

        # Serialize all Design instances
        serializer = DesignSerializer(designs, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        # Delete associated files
        try:
                    if instance.image:
                        instance.image.delete()
        except Exception as e:
                    # Handle the exception here
                    print(f"An error occurred while deleting the image: {e}")

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        # Initialize lists to store titles and images
        titles = []
        images = []

        # Loop through form data keys and separate titles and images
        for key, value in request.data.items():
            if key.startswith('title'):
                titles.append(value)
            elif key.startswith('image'):
                images.append(value)

        # Validate that required fields are present
        if not all([titles, images]):
            return Response({'error': 'Incomplete data provided'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the associated User instance exists
        enquiry_id = request.data.get('enquiry', instance.enquiry_id)
        enquiry = get_object_or_404(Enquire, id=enquiry_id)

        # Handle the case where a new image is provided
        new_image = request.data.get('image', None)

        if new_image is not None:
            if isinstance(new_image, str):
                pass
            else:    # Delete existing image if it exists
                try:
                    if instance.image:
                        instance.image.delete()
                except Exception as e:
                    # Handle the exception here
                    print(f"An error occurred while deleting the image: {e}")
    # You may want to log the error, return a specific response, or take other appropriate actions.

                # Set the new image
                instance.image = new_image

        # Update other fields
        instance.title = titles[0]  # Assuming you only want to update the first title
        instance.approval = request.data.get('approval', instance.approval)
        instance.enquiry = enquiry

        instance.full_clean()  # Validate model fields
        instance.save()

        serializer = DesignSerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
from rest_framework import viewsets, status

class DesignaViewSet(viewsets.ModelViewSet):
    queryset = Design.objects.all()
    serializer_class = DesignSerializer