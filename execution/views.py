from rest_framework.decorators import action
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework import status
from . models import *
from . serializers import *
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404
from django.core.files.storage import default_storage
from django.core.files import File
from django.http import Http404
from django.db.models import Case, When, Value, CharField

class StepsModelViewSet(viewsets.ModelViewSet):
    queryset = stepsModel.objects.all()
    serializer_class = StepsModelSerializer
    permission_classes = [permissions.AllowAny]
    parser_classes = [MultiPartParser, FormParser]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()

    @action(detail=False, methods=['GET'], url_path='user')
    def user_info(self, request, *args, **kwargs):
        user_id = self.request.query_params.get('id', None)

        if not user_id:
            return Response({'error': 'Please provide user id in the query parameters.'}, status=status.HTTP_400_BAD_REQUEST)

        # Define the order based on the model_name choices
        ordering_conditions = [
            Case(
                When(model_name=stepsModel.PROJECT_START, then=Value(1)),
                When(model_name=stepsModel.STRUCTURAL_WORK, then=Value(2)),
                When(model_name=stepsModel.LAMINATE_WORK, then=Value(3)),
                When(model_name=stepsModel.HARDWARE_INSTALL, then=Value(4)),
                When(model_name=stepsModel.FURNISHING_WORK, then=Value(5)),
                When(model_name=stepsModel.HAND_OVER_AND_FINALIZING, then=Value(6)),
                default=Value(0),  # default case, if any model_name doesn't match
                output_field=CharField(),
            )
        ]

        # Filter stepsModel instances by the provided user ID and apply custom ordering
        user_steps = stepsModel.objects.filter(user__id=user_id).order_by(*ordering_conditions)

        # Serialize the data
        serializer = StepsModelSerializer(user_steps, many=True)

        # Return the response
        return Response(serializer.data)

    

class ImageViewSet(viewsets.ModelViewSet):
    queryset = imgTitleStructuralWork.objects.all()
    serializer_class = ImgTitleStructuralWorkSerializer
    permission_classes = [permissions.AllowAny]
    parser_classes = [MultiPartParser, FormParser]

    def create(self, request, *args, **kwargs):
        # Check if the associated stepsModel allows image and title creation
        steps_model_id = request.data.get('stepsmodel', None)
        if steps_model_id:
            steps_model = get_object_or_404(stepsModel, id=steps_model_id)
            if steps_model.model_name == stepsModel.PROJECT_START:
                return Response({'detail': 'Cannot upload image and title for Project Start step.'}, status=status.HTTP_400_BAD_REQUEST)

        return super().create(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        # Get the file path of the image
        file_path = instance.img.path

        # Call the parent class method to perform the deletion
        response = super().destroy(request, *args, **kwargs)

        # If the deletion was successful, delete the corresponding image file
        if response.status_code == status.HTTP_204_NO_CONTENT:
            try:
                # Delete the image file from storage
                default_storage.delete(file_path)
            except FileNotFoundError:
                # Handle file not found error if needed
                pass

        return response
    
    @action(detail=False, methods=['GET'], url_path='stepsmodel')
    def retrieve_by_stepsmodel(self, request, *args, **kwargs):
        # Get the 'stepsmodel' query parameter from the request
        steps_model_id = request.query_params.get('id', None)
        print(f"Steps Model ID: {steps_model_id}")

        if not steps_model_id:
            return Response({'error': 'Please provide the stepsModel id using the "stepsmodel" query parameter.'}, status=status.HTTP_400_BAD_REQUEST)

        # Try to get the associated stepsModel instance
        try:
            steps_model = stepsModel.objects.get(id=steps_model_id)
        except stepsModel.DoesNotExist:
            raise Http404("stepsModel does not exist")

        # Retrieve only the associated imgTitleStructuralWork instances with stepsmodel=3
        img_instances = imgTitleStructuralWork.objects.filter(stepsmodel=steps_model)

        # Serialize the data in the desired format
        response_data = []

        for img_instance in img_instances:
            img_dict = {
                'img': request.build_absolute_uri(img_instance.img.url),
                'title': img_instance.title,
                'model': steps_model.id,
                'id':img_instance.id
            }
            response_data.append(img_dict)

        return Response(response_data)

    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        # Check if a new image file is provided in the request
        new_img_file = request.data.get('img', None)

        if new_img_file:
            # If a new image is provided, create a new imgTitleStructuralWork instance
            new_instance = imgTitleStructuralWork(
                title=instance.title,  # You might want to update other fields if needed
                img=new_img_file,
                stepsmodel=instance.stepsmodel,
            )

            # Save the new instance to the database
            new_instance.save()

            # Serialize the new instance and return the response
            serializer = ImgTitleStructuralWorkSerializer(new_instance)
            return Response(serializer.data, status=status.HTTP_200_OK)

        # If no new image is provided, call the parent class's update method
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)
from django.db import transaction

class UserViewSet(viewsets.ModelViewSet):
    queryset = UserAccount.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        # Filter users who have associated stepsModel
        print("hello")
        return UserAccount.objects.filter(stepsmodel__isnull=False).distinct()
    
    def create(self, request, *args, **kwargs):
        # Extract user ID from the request data
        user_id = request.data.get('id', None)

        if not user_id:
            return Response({'error': 'Please provide user id in the request data.'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the user already has any stepsModel instances
        existing_steps_models = stepsModel.objects.filter(user__id=user_id)

        if existing_steps_models.exists():
            # If stepsModel instances exist, return an error response
            return Response({'error': 'User already has stepsModel instances registered.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # If no stepsModel instances exist, create six instances for the user
        step_names = [
            stepsModel.PROJECT_START,
            stepsModel.STRUCTURAL_WORK,
            stepsModel.LAMINATE_WORK,
            stepsModel.HARDWARE_INSTALL,
            stepsModel.FURNISHING_WORK,
            stepsModel.HAND_OVER_AND_FINALIZING,
        ]

        for step_name in step_names:
            stepsModel.objects.create(model_name=step_name, user_id=user_id)

        # Return a success response
        return Response({'success': f'Six stepsModel instances created for user with ID {user_id}.'}, status=status.HTTP_201_CREATED)


    @transaction.atomic
    def destroy(self, request, *args, **kwargs):
        # Extract user ID from the URL parameters
        user_id = self.kwargs.get('pk', None)

        if not user_id:
            return Response({'error': 'Please provide user id in the URL parameters.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Use a transaction to ensure atomicity
            with transaction.atomic():
                # Get the user
                user = UserAccount.objects.get(id=user_id)

                print(f"Deleting data for user with ID: {user_id}")

                # Get all associated stepsModel instances
                steps_models = stepsModel.objects.filter(user=user)

                # Loop through each stepsModel instance
                for steps_model in steps_models:
                    print(f"Deleting stepsModel instance with ID: {steps_model.id}")

                    # Delete associated images and titles
                    img_instances = imgTitleStructuralWork.objects.filter(stepsmodel=steps_model)
                    for img_instance in img_instances:
                        print(f"Deleting imgTitleStructuralWork instance with ID: {img_instance.id}")

                        # Delete the image file from storage
                        default_storage.delete(img_instance.img.path)
                        # Delete the imgTitleStructuralWork instance
                        img_instance.delete()

                    # Delete the stepsModel instance
                    steps_model.delete()

            # Return a success response
            return Response({'success': f'All stepsModel instances, images, and titles deleted for user with ID {user_id}.'}, status=status.HTTP_200_OK)

        except UserAccount.DoesNotExist as e:
            print(e)
            return Response({'error': f'User with ID {user_id} does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            return Response({'error': 'An error occurred during deletion.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)