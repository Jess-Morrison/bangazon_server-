from bangazonapi.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['POST'])
def check_user(request):
    '''Checks to see if User has associated Profile
    First function that checks inside of the database to see if the user in the dB
    if it is not finding the uid, you get redirectred to the reg user function 
 
    Method arguments:
    request -- The full HTTP request object
    '''
    uid = request.data['uid']

    # Use the built-in authenticate method to verify
    # authenticate returns the user object or None if no user is found
    bangazon_user = User.objects.filter(uid=uid).first()

    # If authentication was successful, respond with their token
    if bangazon_user is not None:
        data = {
            'id': bangazon_user.id,
            'first_name': bangazon_user.first_name,
            'last_name': bangazon_user.last_name,
            'created_on': bangazon_user.created_on,
            'image_url': bangazon_user.image_url,
            'uid': bangazon_user.uid,
        }
        return Response(data)
    else:
        # Bad login details were provided. So we can't log the user in.
        data = {'valid': False}
        return Response(data)


@api_view(['POST'])
def register_user(request):
    '''Handles the creation of a new user for authentication

    Method arguments:
      request -- The full HTTP request object
    '''

    # Now save the user info in the bangazonapi_user table
    bangazon_user = User.objects.create(
        first_name=request.data['first_name'],
        last_name=request.data['last_name'],
        created_on=request.data['created_on'],
        image_url=request.data['image_url'],
        uid=request.data['uid']
    )

    # Return the user info to the client
    data = {
        'id': bangazon_user.id,
        'first_name': bangazon_user.first_name,
        'last_name': bangazon_user.last_name,
        'created_on': bangazon_user.created_on,
        'image_url': bangazon_user.image_url,
        'uid': bangazon_user.uid,
    }
    return Response(data)
