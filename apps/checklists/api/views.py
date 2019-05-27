from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.utils import json
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from apps.checklists.api.serializers import ChecklistSerializer
from apps.checklists.models import Checklist


class ChecklistView(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):  # get checklists from user
        checklists = Checklist.objects.filter(user=request.user)

        # the many param informs the serializer that it will be serializing more than a single article.
        serializer = ChecklistSerializer(checklists, many=True)

        return Response(serializer.data)

    def post(self, request):
        json_data = request.data.get('checklist')

        # Create an article from the above data
        serializer = ChecklistSerializer(data=json_data)
        if serializer.is_valid(raise_exception=True):
            article_saved = serializer.save()

        return Response({"success": "Checklist saved successfully"})

    def put(self, request, pk):

        checklist = get_object_or_404(Checklist.objects.all(), pk=pk)
        data = request.data.get('checklist')
        # partial=True means were only updating some fields that were passed. Not all at once
        serializer = ChecklistSerializer(instance=checklist, data=data, partial=True)

        if serializer.is_valid(raise_exception=True):
            article_saved = serializer.save()

        return Response({"success": "Checklist '{}' updated successfully".format(checklist.description)})

    def delete(self, request, pk):
        # Get object with this pk
        article = get_object_or_404(Checklist.objects.all(), pk=pk)
        article.delete()
        return Response({"message": "Checklist with id `{}` has been deleted.".format(pk)}, status=204)

