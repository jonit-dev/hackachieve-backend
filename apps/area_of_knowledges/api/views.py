from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from apps.area_of_knowledges.api.serializers import AreaOfKnowledgeSerializer
from apps.area_of_knowledges.models import Area_of_knowledge


class AreaOfKnowledgeView(APIView):
    # authentication_classes = (JWTAuthentication,)
    # permission_classes = (IsAuthenticated,)

    def get(self, request):  # get checklists from user
        aoks = Area_of_knowledge.objects.all()

        # the many param informs the serializer that it will be serializing more than a single article.
        serializer = AreaOfKnowledgeSerializer(aoks, many=True)

        return Response(serializer.data)

    def post(self, request):
        json_data = request.data.get('areas_of_knowledge')

        # Create an article from the above data

        for data in json_data:

            serializer = AreaOfKnowledgeSerializer(data=json_data, context={'request': request}, many=True)

            if serializer.is_valid(raise_exception=True):
                saved = serializer.save()

        return Response({"success": "Areas of knowledge saved successfully"})
