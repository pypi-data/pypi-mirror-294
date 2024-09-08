from rest_framework.views import APIView
from rest_framework.response import Response

from .services import BaseService
from .exceptions import HandleExceptionsMixin

class BaseView(HandleExceptionsMixin, APIView, BaseService): pass

class BaseSearchView(HandleExceptionsMixin, APIView, BaseService):
    def get(self, request):
        objetos = self.listar()

        return Response({
            "mensaje": f"Se encontraron {len(objetos)} {self.modelo.MODELO_PLURAL}.",
            "data": objetos
            })

    def post(self, request):
        data = request.data

        objetos = self.listar(**data)

        return Response({
            "mensaje": f"Se encontraron {len(objetos)} {self.modelo.MODELO_PLURAL}.",
            "data": objetos
            })

class BaseABMView(HandleExceptionsMixin, APIView, BaseService):
    def get(self, request, id):
        self.set_objeto(id)

        return Response(self.get_serializado())

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
    