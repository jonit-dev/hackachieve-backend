from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from apps.labels.models import Label
from hackachieve.classes.API import API
from django.apps import apps

@csrf_exempt
@api_view(['get'])
@permission_classes((IsAuthenticated,))
def attach(request, label_id, resource_name, resource_id):
    if resource_name in ['goal']:  # for now, only goal //todo: add label to other resources

        model = apps.get_model('{}s'.format(resource_name), resource_name.capitalize()).objects.get(
            pk=resource_id)  # get resource dinamycally. First we get the model and the we find the particular resource by using the primary key

        label = Label.objects.get(pk=label_id)

        # check if the resource is owned by the request owner

        if label.user.id is not request.user.id:
            return API.json_response({
                'status': 'error',
                'message': 'You cannot attach a label that is not yours.'
            })

        if model.user.id is request.user.id:

            model.labels.add(label)
            model.save()

            return API.json_response({
                'status': 'success',
                'message': 'Your label was attached successfully!'
            })
        else:
            return API.json_response({
                'status': 'error',
                'message': 'This {} is not yours.'.format(resource_name)
            })

    else:
        return API.json_response({
            'status': 'error',
            'message': 'Sorry. You cant attach a label to a/an {}'.format(resource_name)
        })
