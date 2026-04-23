import django_filters
from rest_framework import filters
from api.models import (
    Usuario, Caballo, Paciente, Sesion, BitacoraEquina,
    Tutor, Terapeutas, ContactosEmergencia, Pagos,
    CaballoEstadoSalud, EstatusSesion, EstadosPago
)


class UsuarioFilter(django_filters.FilterSet):
    """Filtros para Usuario: búsqueda por nombres, usuario, correo."""
    nombres = django_filters.CharFilter(field_name='nombres', lookup_expr='icontains')
    apellidos = django_filters.CharFilter(field_name='apellidos', lookup_expr='icontains')
    usuario = django_filters.CharFilter(field_name='usuario', lookup_expr='icontains')
    correo = django_filters.CharFilter(field_name='correo', lookup_expr='icontains')
    
    class Meta:
        model = Usuario
        fields = ['nombres', 'apellidos', 'usuario', 'correo']


class CaballoFilter(django_filters.FilterSet):
    """Filtros para Caballo: nombre, raza, estado de salud, activo."""
    nombre = django_filters.CharFilter(field_name='nombre', lookup_expr='icontains')
    raza = django_filters.CharFilter(field_name='raza', lookup_expr='icontains')
    estado_salud = django_filters.ModelChoiceFilter(queryset=CaballoEstadoSalud.objects.all())
    activo = django_filters.BooleanFilter(field_name='activo')
    edad_min = django_filters.NumberFilter(field_name='edad', lookup_expr='gte')
    edad_max = django_filters.NumberFilter(field_name='edad', lookup_expr='lte')
    peso_max_min = django_filters.NumberFilter(field_name='peso_max', lookup_expr='gte')
    peso_max_max = django_filters.NumberFilter(field_name='peso_max', lookup_expr='lte')
    
    class Meta:
        model = Caballo
        fields = ['nombre', 'raza', 'estado_salud', 'activo', 'edad_min', 'edad_max']


class PacienteFilter(django_filters.FilterSet):
    """Filtros para Paciente: nombre, edad, tutor, activo."""
    nombre = django_filters.CharFilter(field_name='nombre', lookup_expr='icontains')
    edad_min = django_filters.NumberFilter(field_name='edad', lookup_expr='gte')
    edad_max = django_filters.NumberFilter(field_name='edad', lookup_expr='lte')
    tutor_id = django_filters.ModelChoiceFilter(field_name='tutor_id', queryset=Tutor.objects.all())
    activo = django_filters.BooleanFilter(field_name='activo')
    
    class Meta:
        model = Paciente
        fields = ['nombre', 'edad_min', 'edad_max', 'tutor_id', 'activo']


class SesionFilter(django_filters.FilterSet):
    """Filtros para Sesion: terapeuta, paciente, caballo, rango de fecha, estatus."""
    terapeuta_id = django_filters.ModelChoiceFilter(field_name='terapeuta_id', queryset=Terapeutas.objects.all())
    paciente_id = django_filters.ModelChoiceFilter(field_name='paciente_id', queryset=Paciente.objects.all())
    caballo_id = django_filters.ModelChoiceFilter(field_name='caballo_id', queryset=Caballo.objects.all())
    estatus_id = django_filters.ModelChoiceFilter(
        field_name='estatus_id', 
        queryset=EstatusSesion.objects.all()
    )
    fecha_hora_desde = django_filters.DateTimeFilter(
        field_name='fecha_hora', 
        lookup_expr='gte'
    )
    fecha_hora_hasta = django_filters.DateTimeFilter(
        field_name='fecha_hora', 
        lookup_expr='lte'
    )
    
    class Meta:
        model = Sesion
        fields = ['terapeuta_id', 'paciente_id', 'caballo_id', 'estatus_id']


class BitacoraEquinaFilter(django_filters.FilterSet):
    """Filtros para BitacoraEquina: paciente, caballo, rango de fecha."""
    paciente_id = django_filters.ModelChoiceFilter(field_name='paciente_id', queryset=Paciente.objects.all())
    caballo_id = django_filters.ModelChoiceFilter(field_name='caballo_id', queryset=Caballo.objects.all())
    fecha_sesion_desde = django_filters.DateTimeFilter(
        field_name='fecha_sesion', 
        lookup_expr='gte'
    )
    fecha_sesion_hasta = django_filters.DateTimeFilter(
        field_name='fecha_sesion', 
        lookup_expr='lte'
    )
    
    class Meta:
        model = BitacoraEquina
        fields = ['paciente_id', 'caballo_id']


class PagosFilter(django_filters.FilterSet):
    """Filtros para Pagos: tutor, sesion, estatus."""
    tutor_id = django_filters.ModelChoiceFilter(field_name='tutor_id', queryset=Tutor.objects.all())
    sesion_id = django_filters.ModelChoiceFilter(field_name='sesion_id', queryset=Sesion.objects.all())
    estatus_id = django_filters.ModelChoiceFilter(
        field_name='estatus_id',
        queryset=EstadosPago.objects.all()
    )
    monto_min = django_filters.NumberFilter(field_name='monto', lookup_expr='gte')
    monto_max = django_filters.NumberFilter(field_name='monto', lookup_expr='lte')
    
    class Meta:
        model = Pagos
        fields = ['tutor_id', 'sesion_id']


class ContactosEmergenciaFilter(django_filters.FilterSet):
    """Filtros para ContactosEmergencia: paciente, parentesco."""
    paciente_id = django_filters.ModelChoiceFilter(field_name='paciente_id', queryset=Paciente.objects.all())
    nombre = django_filters.CharFilter(field_name='nombre', lookup_expr='icontains')
    
    class Meta:
        model = ContactosEmergencia
        fields = ['paciente_id', 'nombre']


class TerapeutasFilter(django_filters.FilterSet):
    """Filtros para Terapeutas: usuario (nombres), especialidad."""
    usuario_nombres = django_filters.CharFilter(
        field_name='usuario__nombres', 
        lookup_expr='icontains'
    )
    usuario_apellidos = django_filters.CharFilter(
        field_name='usuario__apellidos', 
        lookup_expr='icontains'
    )
    especialidad = django_filters.CharFilter(
        field_name='especialidad', 
        lookup_expr='icontains'
    )
    
    class Meta:
        model = Terapeutas
        fields = ['especialidad']


class TutorFilter(django_filters.FilterSet):
    """Filtros para Tutor: usuario (nombres), teléfono."""
    usuario_nombres = django_filters.CharFilter(
        field_name='usuario__nombres', 
        lookup_expr='icontains'
    )
    usuario_apellidos = django_filters.CharFilter(
        field_name='usuario__apellidos', 
        lookup_expr='icontains'
    )
    telefono = django_filters.CharFilter(
        field_name='telefono', 
        lookup_expr='icontains'
    )
    
    class Meta:
        model = Tutor
        fields = ['telefono']
