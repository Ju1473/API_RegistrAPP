import firebase_admin.auth
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from .serielizers import *
import firebase_admin
from firebase_admin import firestore, credentials, auth
from google.cloud.firestore_v1.base_query import FieldFilter
from google.cloud.firestore_v1.field_path import FieldPath
import locale
from django.utils import timezone

cred = credentials.Certificate('erviceAccountKey.json')
app = firebase_admin.initialize_app(cred)
db = firestore.client()

# Create your views here.
def verify_token(token):
    try:
        decoded_token = auth.verify_id_token(token)
        return decoded_token
    except:
        return None

class SeccionesView(APIView):
    def get(self, request, id=None):
        auth_header = request.headers.get('Authorization')

        if not auth_header:
            return Response({'error': 'Unauthorized request to get secciones'}, status=status.HTTP_401_UNAUTHORIZED)

        token = auth_header.split(' ')[1]
        decoded_token = verify_token(token)
        if not decoded_token:
            return Response({'error': 'Unauthorized request to get secciones'}, status=status.HTTP_401_UNAUTHORIZED)

        asistencias = None
        secciones = None
        secciones_ids = []
        usuarios_ids = []
        if decoded_token.get('email').split('@')[1] == 'duocuc.cl':
            asistencias = db.collection('asistencias').where(filter=FieldFilter('uid_usuario', '==', decoded_token.get('user_id'))).get()
            secciones_ids = [asistencia.get('uid_seccion') for asistencia in asistencias] if not id else [id]
            secciones = db.collection('secciones').document(id).get() if id else db.collection('secciones').where(FieldPath.document_id(), 'in', secciones_ids).get()
            usuarios_ids = [seccion.get('uid_profesor') for seccion in secciones] if not id else [secciones.get('uid_profesor')]
        elif decoded_token.get('email').split('@')[1] == 'profesor.duoc.cl':
            secciones = db.collection('secciones').document(id).get() if id else db.collection('secciones').where(filter=FieldFilter('uid_profesor', '==', decoded_token.get('user_id'))).get()
            secciones_ids = [secciones.id] if id else [seccion.id for seccion in secciones]
            asistencias = db.collection('asistencias').where(filter=FieldFilter('uid_seccion', 'in', secciones_ids)).get()
            usuarios_ids = [asistencia.get('uid_usuario') for asistencia in asistencias]
        asignaturas_ids = [seccion.get('uid_asignatura') for seccion in secciones] if not id else [secciones.get('uid_asignatura')]
        asignaturas = db.collection('asignaturas').where(FieldPath.document_id(), 'in', asignaturas_ids).get()
        clases_ids = [seccion.get('uid_clase') for seccion in secciones] if not id else [secciones.get('uid_clase')]
        clases = db.collection('clases').where(FieldPath.document_id(), 'in', clases_ids).get()
        horarios_ids = list(set(hora for clase in clases for hora in clase.get('horarios')))
        horarios = db.collection('horarios').where(FieldPath.document_id(), 'in', horarios_ids).get()
        salas_ids = list(set(horario.get('uid_sala') for horario in horarios))
        salas = db.collection('salas').where(FieldPath.document_id(), 'in', salas_ids).get()
        usuarios_ids.append(decoded_token.get('user_id'))
        usuarios = db.collection('usuarios').where(FieldPath.document_id(), 'in', usuarios_ids).get()
        """ ------------ """
        secciones_list = []
        if id:
            secciones_list.append(getS(secciones, asistencias, asignaturas, clases, usuarios, horarios, salas, decoded_token))
        else:
            for seccion in secciones:
                secciones_list.append(getS(seccion, asistencias, asignaturas, clases, usuarios, horarios, salas, decoded_token))
            secciones_list.sort(key=lambda x: x['asignatura']['nombre'])

        serializer = SeccionSerializer(secciones_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def options(self, request, id=None):
        options_data = {
            'GET': 'Retrieve a list of all secciones',
            'POST': 'Create a new seccion',
            'PUT': 'Update an existing seccion',
            'DELETE': 'Delete an existing seccion'
        }
        return Response(options_data, status=status.HTTP_200_OK)
    
class QRView(APIView):
    def get(self, request, id=None):
        auth_header = request.headers.get('Authorization')

        if not auth_header:
            return Response({'error': 'Unauthorized request to get secciones'}, status=status.HTTP_401_UNAUTHORIZED)

        token = auth_header.split(' ')[1]
        decoded_token = verify_token(token)
        if not decoded_token:
            return Response({'error': 'Unauthorized request to get secciones'}, status=status.HTTP_401_UNAUTHORIZED)

        if decoded_token.get('email').split('@')[1] != 'profesor.duoc.cl':
            return Response({'error': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        
        locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
        local_time = timezone.now()
        
        secciones = db.collection('secciones').where(filter=FieldFilter('uid_profesor', '==', decoded_token.get('user_id'))).get()
        clases_ids = [seccion.get('uid_clase') for seccion in secciones]
        clases = db.collection('clases').where(FieldPath.document_id(), 'in', clases_ids).get()
        horarios_ids = list(set(hora for clase in clases for hora in clase.get('horarios')))
        horarios = db.collection('horarios').where(FieldPath.document_id(), 'in', horarios_ids).get()
        for seccion in secciones:
            clase = next((clase for clase in clases if clase.id == seccion.get('uid_clase')), None)
            if clase and local_time.strftime('%d-%m-%Y') in [clase for clase in clase.get('clases')]:
                for horario in horarios:
                    if local_time.strftime('%A').capitalize() == horario.get('dia') and local_time.strftime('%H:%M') >= horario.get('hora_ini') and local_time.strftime('%H:%M') < horario.get('hora_ter'):
                        serializer = QRSerializer([{ 'uid_clase': clase.id, 'uid_seccion': seccion.id }], many=True)
                        return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'error': 'No se encontró ninguna clase actual'}, status=status.HTTP_404_NOT_FOUND)
    
class UserView(APIView):
    def get(self, request, id=None):
        auth_header = request.headers.get('Authorization')

        if not auth_header:
            return Response({'error': 'Unauthorized request to get secciones'}, status=status.HTTP_401_UNAUTHORIZED)
        
        token = auth_header.split(' ')[1]
        decoded_token = verify_token(token)
        if not decoded_token:
            return Response({'error': 'Unauthorized request to get secciones'}, status=status.HTTP_401_UNAUTHORIZED)
        
        user = db.collection('usuarios').document(decoded_token.get('user_id')).get()
        data = user.to_dict()
        data = {**data, 'email': decoded_token.get('email'), 'uid': user.id}
        serializer = UsuarioSerializer(data, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

""" FUNCIONES """

def getS(seccion, asistencias, asignaturas, clases, usuarios, horarios, salas, decoded_token):
    """ ------------ """
    data = {**seccion.to_dict(), 'uid': seccion.id}
    asignatura = next((asignatura for asignatura in asignaturas if asignatura.id == seccion.get('uid_asignatura')), None)
    clase = next((clase for clase in clases if clase.id == seccion.get('uid_clase')), None)
    profesor = next((profesor for profesor in usuarios if profesor.id == seccion.get('uid_profesor')), None)
    if decoded_token.get('email').split('@')[1] == 'duocuc.cl':
        asistencia = next((asistencia for asistencia in asistencias if asistencia.get('uid_seccion') == seccion.id), None)
        if asistencia:
            data = {**data, 'asistencia': {'asistidas': asistencia.get('clases').count(2), 'clases': asistencia.get('clases'), 'faltas': asistencia.get('clases').count(1), 'justificadas': asistencia.get('clases').count(3), 'porcentaje': asistencia.get('clases').count(2) / clase.get('clases_realizadas').count(1), 'uid': asistencia.id}}
    elif decoded_token.get('email').split('@')[1] == 'profesor.duoc.cl':
        asistencias_list = []
        for asistencia in asistencias:
            if asistencia.get('uid_seccion') == seccion.id:
                usuario_data = next((usuario for usuario in usuarios if usuario.id == asistencia.get('uid_usuario')), None)
                asistencias_list.append({'asistidas': asistencia.get('clases').count(2), 'clases': asistencia.get('clases'), 'faltas': asistencia.get('clases').count(1), 'justificadas': asistencia.get('clases').count(3), 'porcentaje': asistencia.get('clases').count(2) / clase.get('clases_realizadas').count(1), 'usuario': {**usuario_data.to_dict(), 'uid': usuario_data.id}, 'uid': asistencia.id})
        data = {**data, 'asistencias': asistencias_list}
    if asignatura:
        data = {**data, 'asignatura': {'nombre': asignatura.get('nombre'), 'codigo': asignatura.get('codigo'), 'uid': asignatura.id}}
    if clase:
        data = {**data, 'clase': {'clases': clase.get('clases'), 'clasesTotales': len(clase.get('clases')), 'clases_realizadas': clase.get('clases_realizadas'), 'uid': clase.id}}
        if horarios:
            hora = []
            for h in set(clase.get('horarios')):
                horario_data = next((horario for horario in horarios if horario.id == h), None)
                sala_data = next((sala for sala in salas if sala.id == horario_data.get('uid_sala')), None)
                if horario_data:
                    hora.append({'dia': horario_data.get('dia'), 'hora_ini': horario_data.get('hora_ini'), 'hora_ter': horario_data.get('hora_ter'), 'sala': sala_data.get('codigo'), 'uid': horario_data.id})
            dia_orden = {'Lunes': 0, 'Martes': 1, 'Miércoles': 2, 'Jueves': 3, 'Viernes': 4}
            hora.sort(key=lambda x: (dia_orden.get(x['dia'], 5), x['hora_ini']))
            data = {**data, 'horario': hora}
    if profesor:
        data = {**data, 'profesor': {**profesor.to_dict(), 'uid': profesor.id}}
    if decoded_token.get('email').split('@')[1] == 'duocuc.cl':
        estudiante = next((estudiante for estudiante in usuarios if estudiante.id == decoded_token.get('user_id')), None)
        if estudiante:
            data = {**data, 'estudiante': {**estudiante.to_dict(), 'uid': estudiante.id}}

    if decoded_token.get('email').split('@')[1] == 'profesor.duoc.cl':
        total_porcentajes = sum(alumno['porcentaje'] for alumno in data['asistencias'])
        porcentaje_general_curso = total_porcentajes / len(data['asistencias'])
        data = {**data, 'porcentaje': porcentaje_general_curso}
    """ ------------ """
    return data