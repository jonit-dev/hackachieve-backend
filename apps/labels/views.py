from django.forms import model_to_dict
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny

from apps.labels.models import Label
from hackachieve.classes.API import API
from django.apps import apps


@csrf_exempt
@api_view(['post', 'get', 'put', 'delete'])
@permission_classes((IsAuthenticated,))
def REST(request, label_id=None):
    if request.method == 'POST':

        # create goal for the auth user only
        json_data = API.json_get_data(request)

        label = Label(name=json_data['name'], user=request.user)
        label.save()

        if label:
            return API.json_response({
                'status': 'success',
                'message': 'Your label was created successfully'
            })
        else:
            return API.json_response({
                'status': 'error',
                'message': 'Error while trying to create your label'
            })

    elif request.method == 'GET':

        if label_id:
            label = Label.objects.get(pk=label_id, user=request.user)
            label = model_to_dict(label)
            return JsonResponse(label, safe=False)
        else:

            labels = Label.objects.filter(user=request.user)
            # get this model using a filter
            labels = list(labels.values())
            return JsonResponse(labels, safe=False)


    elif request.method == 'PUT':

        json_data = API.json_get_data(request)

        try:
            label = Label.objects.get(pk=label_id, user=request.user)
            label.name = json_data['name']
            label.save()

            return API.json_response({
                'status': 'success',
                'message': 'Your label was updated successfully!'
            })
        except Exception:
            return API.json_response({
                'status': 'erro',
                'message': 'Error while trying to update your label'
            })



    elif request.method == 'DELETE':

        try:
            label = Label.objects.get(pk=label_id, user=request.user)
            label.delete()

            return API.json_response({
                'status': 'success',
                'message': 'Your label was deleted successfully!'
            })

        except Exception:
            return API.json_response({
                'status': 'erro',
                'message': 'Error while trying to delete your label'
            })


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
