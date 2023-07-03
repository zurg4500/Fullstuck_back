from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .serializers import WineSerializer
from .models import Wine
from permissions.permissions import IsOwnerOrIsAdminUser


class WineViewSet(ModelViewSet):
    queryset = Wine.objects.prefetch_related('images', 'description', 'title', 'price', 'year', 'excerpt').all()
    serializer_class = WineSerializer

    def get_permissions(self):
        if self.request.method in ["PUT", "PATCH", "DELETE"]:
            self.permission_classes = [IsOwnerOrIsAdminUser]
        else:
            self.permission_classes = [IsAuthenticatedOrReadOnly]
        return super().get_permissions()

