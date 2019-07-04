
# Create your views here.
from rest_framework import mixins, viewsets, status
from rest_framework.response import Response

from apps.projects.models import Project
from apps.projects.serializer import ProjectCreateSerializer, ProjectDetailSerializer, ProjectUpdateSerializer


class ProjectViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    """  Project ViewSet  """

    queryset = Project.objects.all()
    serializer_class = ProjectCreateSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = ProjectDetailSerializer(instance)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance:
            if instance.user == request.user:
                self.perform_destroy(instance)
                return Response({'status': 'success', 'message': 'Record Deleted Successfully'},
                                status=status.HTTP_200_OK)
            else:
                return Response({'status': 'fail', 'message': 'You have not permission to delete this record '},
                                status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = ProjectUpdateSerializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        if instance.user == request.user:
            self.perform_update(serializer)
            if getattr(instance, '_prefetched_objects_cache', None):
                instance._prefetched_objects_cache = {}

            return Response(serializer.data)
        else:
            return Response({'status': 'fail', 'message': 'You have not permission to update this record '},
                            status=status.HTTP_200_OK)




