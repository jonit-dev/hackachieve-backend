from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from apps.goals.models import Goal
from apps.labels.models import Label
from .serializers import LabelSerializer


class LabelView(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):

        print('Triggering labels from goals')

        labels = Label.objects.filter(user=request.user, goal=pk)
        serializer = LabelSerializer(labels, many=True)

        return Response(serializer.data)

    def post(self, request, pk):
        json_data = request.data

        # check if goal exists
        goal_exists = Goal.objects.filter(pk=pk, user=request.user).exists()

        if not goal_exists:
            return Response({"error": "This goal does not exist or its not yours"})

        # Create an label from the above data
        serializer = LabelSerializer(data=json_data, context={'request': request, 'pk': pk})
        if serializer.is_valid(raise_exception=True):
            serializer.save()

        return Response({"success": "Label saved successfully"})

    def put(self, request, pk):
        user = request.user

        label = get_object_or_404(Label.objects.all(), pk=pk)

        # check if user own's the label he's trying to edit
        if user.id is not label.user_id:
            return Response({"error": "You cannot edit a label that's not yours"})

        # partial=True means were only updating some fields that were passed. Not all at once
        data = request.data
        serializer = LabelSerializer(instance=label, data=data, partial=True, context={'request': request})

        if serializer.is_valid(raise_exception=True):
            serializer.save()

        return Response({"success": "Label '{}' updated successfully".format(label.name)})

    def delete(self, request, pk):
        # Get object with this pk
        label = get_object_or_404(Label.objects.all(), pk=pk)

        # check if the request origin is coming from the owner
        if request.user.id is not label.user.id:
            return Response({"error": "You cannot delete a label that's not yours"}, status=204)
        else:
            label.delete()
            return Response({"success": "Label with id `{}` deleted.".format(pk)})
