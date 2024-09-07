from rest_framework.views import APIView
from rest_framework.response import Response

from .services import BaseService
from .exceptions import HandleExceptionsMixin

class BaseAPIView(HandleExceptionsMixin, APIView, BaseService):
    def get(self, request):
        return Response({
            "mensaje": f"Listado de {self.modelo.MODELO_PLURAL.lower()}.",
            "data": self.listar(),
            })

    def post(self, request):
        self.crear(**request.data)

        return Response({
            "mensaje": f"{self.modelo.MODELO_SINGULAR} creado con éxito.", 
            "data": self.get_serializado()
            })

    def put(self, request):
        objeto_id = request.data.get('id')
        self.set_objeto(objeto_id)
        self.actualizar(**request.data)

        return Response({
            "mensaje": f"{self.modelo.MODELO_SINGULAR} actualizado con éxito.", 
            "data": self.get_serializado()
            })

    def delete(self, request):
        objeto_id = request.data.get('id')
        self.set_objeto(objeto_id)
        self.eliminar()

        return Response({
            "mensaje": f"{self.modelo.MODELO_SINGULAR} eliminado con éxito."
            })
    