from .exceptions import ServiceException
from threading import Thread

import re

class BaseService:
    modelo = None
    objeto = None

    def __init__(self, id=None):
        if id is not None:
            self.set_objeto(id)
            
    def set_objeto(self, id):
        try:
            self.objeto = self.modelo.objects.get(id=id)

        except self.modelo.DoesNotExist:
            raise ServiceException(f"El {self.modelo.__name__} con id '{id}' no existe.")
            

    def asincrono(self, funcion, *args):
        thread = Thread(target=funcion, args=args)
        thread.start()

    def get_serializado(self):
        if self.objeto is None:
            raise ServiceException(f"El {self.modelo.MODELO_SINGULAR.lower()} no ha sido definido.")

        data = {
            'id': self.objeto.id
        }

        for atributo in self.modelo.ATRIBUTOS:
            if 'serializar' in atributo and atributo['serializar']:
                etiqueta = atributo['etiqueta'].lower()
                if 'es_relacion' in atributo and atributo['es_relacion']:
                    relacion = getattr(self.objeto, atributo['campo'])

                    valor = None

                    if relacion:
                        valor = {
                            'id': relacion.id,
                            'to_str': valor.__str__()
                        }

                    data[etiqueta] = valor

                else:
                    campo = str(atributo['campo'])
                    data[etiqueta] = getattr(self.objeto, campo)

        return data

    def listar(self, **kwargs):
        data = []

        filtros = {}

        for kw in kwargs:
            if kw not in list(map(lambda x: x['etiqueta'].lower(), self.modelo.ATRIBUTOS)):
                raise ServiceException(f"El campo '{kw}' no existe.")
            
            atributo = list(filter(lambda x: x['etiqueta'].lower() == kw, self.modelo.ATRIBUTOS))[0]

            if 'es_filtrable' not in atributo or not atributo['es_filtrable']:
                raise ServiceException(f"El campo '{kw}' no es filtrable.")

            campo = str(atributo['campo'])
            valor = kwargs[kw]

            filtros[campo] = valor

        objetos = self.modelo.objects.filter(**filtros)



        for objeto in objetos:
            service = self.__class__()
            service.objeto = objeto

            data.append(service.get_serializado())

        return data
    
    def validar_formato(self, atributo, etiqueta, valor):
        if 'expresion_regular' in atributo:
            expresion_regular = atributo['expresion_regular']

            if not re.match(expresion_regular, valor):
                raise ServiceException(f"El campo '{etiqueta}' no cumple con el formato requerido.")
                    
    def validar_unicidad(self, atributo, etiqueta, valor):
        if 'unico' in atributo:
            campo = str(atributo['campo'])

            if self.modelo.objects.filter(**{campo: valor}).exists():
                raise ServiceException(f"El campo '{etiqueta}' con valor '{valor}' ya existe.")

    def crear(self, **kwargs):
        objeto = self.modelo()

        for atributo in self.modelo.ATRIBUTOS:
            if 'requerido_crear' in atributo and atributo['requerido_crear']:
                etiqueta = atributo['etiqueta'].lower()

                if etiqueta not in kwargs:
                    raise ServiceException(f"El campo '{etiqueta}' es requerido.")
                
                campo = str(atributo['campo']) 
                valor = kwargs[etiqueta]

                
                self.validar_formato(atributo, etiqueta, valor)
                self.validar_unicidad(atributo, etiqueta, valor)

                if 'es_relacion' in atributo:
                    campo = campo + '_id'
                
                setattr(objeto, campo, valor)

        objeto.save()
        self.objeto = objeto

    def actualizar(self, **kwargs):
        if self.objeto is None:
            raise ServiceException(f"El {self.modelo.MODELO_SINGULAR.lower()} no ha sido definido.")
        
        for atributo in kwargs:
            if atributo not in list(map(lambda x: x['etiqueta'].lower(), self.modelo.ATRIBUTOS)) + ['id']:
                raise ServiceException(f"El campo '{atributo}' no existe.")
            
        else:
            for kw in kwargs:
                if kw == 'id':
                    continue

                atributo = list(filter(lambda x: x['etiqueta'].lower() == kw, self.modelo.ATRIBUTOS))[0]
                etiqueta = atributo['etiqueta'].lower()
                campo = str(atributo['campo'])
                valor = kwargs[etiqueta]

                self.validar_formato(atributo, etiqueta, valor)
                self.validar_unicidad(atributo, etiqueta, valor)

                setattr(self.objeto, campo, valor)

        self.objeto.save()

    def eliminar(self):
        if self.objeto is None:
            raise ServiceException(f"El {self.modelo.MODELO_SINGULAR.lower()} no ha sido definido.")

        self.objeto.delete()
        self.objeto = None

        