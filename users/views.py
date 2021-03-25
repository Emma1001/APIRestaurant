from io import BytesIO

import imghdr
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from users.models import User
from users.serializers import UserModelSerializer


class UserModelViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserModelSerializer

    @action(methods=['POST'], detail=True,
            url_path='upload-image', url_name='upload_image')
    def upload_image(self, request, pk=None):
        user = User.objects.get(id=self.kwargs['pk'])
        image = request.data['image']

        if imghdr.what(image) != 'jpeg' and imghdr.what(image) != 'png':
            return Response("Image format must be .jpg or .png",
                            status=status.HTTP_400_BAD_REQUEST)

        if image.size > 5 * 1024 * 1024:
            return Response("Image file too large ( > 5mb )",
                            status=status.HTTP_400_BAD_REQUEST)

        user.image = image
        user.save()
        return Response("Uploaded image", status=status.HTTP_200_OK)

    @action(methods=['GET'], detail=True,
            url_path='fetch-image', url_name='fetch_image')
    def fetch_image(self, request, pk=None):
        user = User.objects.get(id=self.kwargs['pk'])
        if user.image == 'null':
            return Response("User doesn\'t have an image.", status=status.HTTP_204_NO_CONTENT)

        serializer = UserModelSerializer(user)
        return Response(serializer.data['image'], status=status.HTTP_200_OK)
