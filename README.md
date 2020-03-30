# Django Avanzado



## Herencia de modelos()

La herencia de modelos puede ser útil porque podemos tener datos generales que pueden ser heredados por otras que no necesariamente tienen su propia tabla, porque queremos que haya herencia de múltiples tablas que se reflejan en la base de datos o porque queremos extender la funcionalidad de un modelo.

- Las clases heredan de django.db.models.
- Extender la funcional de un modelo.
- Múltiple herencia de modelos.



### Clase Abstracta.

```python
from django.db import models

class CRideModel(models.Model):

    created = models.DateTimeField(
        'created at',
        auto_now_add=True,
        help_text='Date time on which the object was created.'
    )

    modified = models.DateTimeField(
        'modified at',
        auto_now=True,
        help_text='Date time on which the object was last modified'
    )

    class Meta:

        abstract = True
        get_latest_by = 'created'
        ordering = ['-created', '-modifield']
```



### Herencia de Clase Abstracta.

```python
class Student(CRideModel):
		name = models.CharField()
		
		class Meta(CRideModel.META):
		db_table = 'student_role'
```



## Proxy models (Solo extienden la funcionalidad)

Los **Proxys** nos permiten extender la funcionalidad de un modelo sin crear una nueva tabla en la base de datos, la diferencia con los Abstract Models es que estas solo exponen un molde de atributos y las **proxys** extienden de una tabla ya existente.

```
class Person(models.Model):
		first_name = model.CharField()
		last_name = model.CharField()
		
class MyPerson(Person):
		class Meta:
				proxy = True
				
		def say_hi(name):
			pass
	
ricardo = MyPerson.objects.get(pk=1)
ricardo.say_hi('pablo')



```

## Creación de un APP.

Una app es un modulo especializado.

Los módulos están compuesto por los siguientes archivos.

### apps.py

- Cada app debe ser especificada.
- Extienden de **App.Config** proveniente de django.apps
- Debe tener por default el **name** y el **verbose_name**
- Se debe especificar en el modulo de configuración como un app instalada(La ruta va con respecto al **manage.py**).

```python
"""Users App Config"""

# Django
from django.apps import AppConfig

class UsersAppConfig(AppConfig):
    """Users app config """

    name = 'cride.users'
    verbose_name = 'Users'

```

### migrations(Modulo que cada app necesita)

Se crea como un folder y se asigna un archivo de inicializacion de modulo.

### models.py

Es donde se especifican los modelos para la base de datos.

## AbstractUser Model

Es el modelo del cual extiende la clase **User** de **django.contrib.auth.models**. Se especifica que cuando iniciamos un nuevo modelo es mejor extender de **AbstractUser** ya que después seria muy complicado. 

```python
"""Users Model."""

from django.db import models
from django.contrib.auth.models import AbstractUser

# Utilities
from cride.utils.models import CRideModel


class User(CRideModel, AbstractUser):
    """User model.

    Extend from Django's Abstract User, change the username field
    to email and add some extra fields.
    """

    email = models.EmailField(
        'email addres',
        unique=True,
        error_message={
            'unique': 'A User with the same email already exists.'
        }
    )

    phone_number = models.CharField(max_length=17, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','first_name','last_name']

    if_client = models.BooleanField(
        'client status',
        default=True,
        help_text=(
            'Help easily distinguish users and perform queries'
            'Clients are the main type of user.'
        )
    )

    is_verified = models.BooleanField(
        'verified',
        default=True,
        help_text='Set to true when the user have verified its email address.'
    )
```



### Validators

Los validators nos sirven para validad una Field. Provienen de  **django.core.validators** como **RegexValidator** el cual en este caso es una validador de expresiones regulares.



#### RegexValidator

1. Importamos el validador.
2. Dentro del modelo se crea el validador como una variable.
3. Asignación del validador al Field correspondiente. Esto va dentro de un parametro llamado **validators** el cual es una lista de validadores. Siempre cuando se guarde un elemento este va a validar antes que corresponda.

```python
# 1 Validators.
from django.core.validators import RegexValidator

class User(CRideModel, AbstractUser):
   
# 2 Creacion de validador.
    phone_regex = RegexValidator( 
        regex=r'\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: +999999999. Up to 15 digits allowed."
    )
    
# Asignacion a Field.
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)

   


```

### Registro de Modelo custom User.

Cuando creamos un nuevo modelo de User se debe especificar en la configuración el nuevo modelo de Usuario, esto se logra de la siguiente forma.

```python
# Users & Authentication
# SINTAXIS Modulo.Model
AUTH_USER_MODEL = 'users.User'
```

### Empaquetado de Modelos.

Para hacer un empaquetado es como hacer un modulo cualquiera.

- En este caso el nombre del modulo sera **models**

- Lleva su **init** file y en este mismo se especifican los Modelos a exportar, en este caso todos los modelos que contendrá nuestra app.

  ```python
  # Modelos dentro de __init__.py
  from .users import User
  from .profiles import Profile
  ```

### Registro del Admin de nuestro modelo Custom.

Ya que estendimos de **AbstractUserModel** para el registro del admin se puede extender de **UserAdmin**, este modelo proviene de **contrib.auth.admin** y ya se encuentra registrado, por lo cual es necesario sobre escribirlo.

```python
"""User models admin."""

# Django
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Models
from cride.users.models import User, Profile


class CustomUserAdmin(UserAdmin):
    """User model admin."""

    list_display = ('email', 'username', 'first_name', 'last_name', 'is_staff', 'is_client')
    list_filter = ('is_client', 'is_staff', 'created', 'modified')


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Profile model admin."""

    list_display = ('user', 'reputation', 'rides_taken', 'rides_offered')
    search_fields = ('user__username', 'user__email', 'user__first_name', 'user__last_name')
    list_filter = ('reputation',)


# El modelo UserAdmin ya esta registrado y se registra de esta forma
admin.site.register(User, CustomUserAdmin)
```



## Correr un shell de Python en docker.

Utilizaremos una herramienta instalada la cual es **django_extensions**.

### Importar datos de un Fixtures

Para importar los datos se crea una carpeta **Fixtures** la cual contiene un archivo json del cual se sacara la data.

**Ejecutar el siguiente comando:**

```shell
docker-compose run --rm django python manage.py loaddata cride/circles/fixtures/circles.json
```



## Cliente HTTPie



### Instalación

```
pip install httpie
```

### Comandos

```
http

# request
http localhost:8000/circles/

# Solo el body
http localhost:8000/circles/ -b

# Verboso
http localhost:8000/circles/ -v

# request con verbo
http POST localhost:8000/circles/ -b
```



## Ejemplo sin DjangoRestFramework

**Views.py**

En este caso se crearía una vista similar a la siguiente.

```python
"""Circles views"""

# Django
from django.http import JsonResponse

# Models
from cride.circles.models import Circle


def list_circles(request):
    """List circles."""
    circles = Circle.objects.all()
    public = circles.filter(is_public=True)
    data = []
    for circle in public:
        data.append({
            'name': circle.name,
            'slug_name': circle.slug_name,
            'rides_taken': circle.rides_taken,
            'rides_offered': circle.rides_offered,
            'members_limit': circle.members_limit,
        })

    return JsonResponse(data, safe=False)
```



**urls.py**

Mapeada de la siguiente forma en el modulo **Circles**

```python
"""Circles URLs."""

# Django
from django.urls import path 

# Views
from cride.circles.views import list_circles

urlpatterns = [
  path('circles/', list_circles)
]
```



**urls.py**

Mapeo en el urls.py general.

```django
"""Main URLs module."""

from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
from django.contrib import admin

urlpatterns = [
    # Django Admin
    path(settings.ADMIN_URL, admin.site.urls),

    path('', include(('cride.circles.urls', 'circles'), namespace='circle'))

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```



## Vistas, URLs y Parsers DRF

[Request Documentacion](https://www.django-rest-framework.org/api-guide/requests/)







## Serializers

Los **serializers** son contenedores que nos permiten tomar tipos de datos complejos, convertirlos en datos nativos de python para después poderlos usar como JSON o XML. Son contenedores que amoldan datos para que cumplan con las condiciones de los serializers y sean llevados a un tipo de estos y después estos puedan ser transformados en otra cosa.

**Serializers** are containers that allow us to take complex data types, convert them into native Python data and then use them as JSON or XML. They are containers that mold data so that they meet the conditions of the serializers and are taken to one of these types and then they can be transformed into something else.



### Serializers form Circles

```python
""" Circle serializers."""

# Djangon
from rest_framework import serializers

# Validators
from rest_framework.validators import UniqueValidator

# Model
from cride.circles.models import Circle


class CircleSerializer(serializers.Serializer):
    """Circle serializers."""

    name = serializers.CharField()
    slug_name = serializers.SlugField()
    rides_taken = serializers.IntegerField()
    rides_offered = serializers.IntegerField()
    members_limit = serializers.IntegerField()


class CreateCircleSerializer(serializers.Serializer):
    """Create circle serializer."""
    name = serializers.CharField(max_length=140)
    slug_name = serializers.SlugField(
        max_length=40,
        validators=[
            UniqueValidator(queryset=Circle.objects.all())
        ]
    )
    about = serializers.CharField(
        max_length=255,
        required=False
    )

    # Recibe los datos ya validados
    def create(self, data):
        """Create circle."""
        return Circle.objects.create(**data)

```



## Obtención de datos mediante Serializers.



### 1.-  Obtener lista de objetos.

Forma menos practica.

```python
@api_view(['GET'])
def list_circles(request):
    """List circles."""
    circles = Circle.objects.filter(is_public=True)
    data = []
    for circle in circles:
        serializer = CircleSerializer(circle)
        data.append(serializer.data)

    return Response(data)
```

### 2.- Obtener lista de objetos.

Los **serializers** nos permiten transformar listas de objetos, siempre y cuando especifiquemos que llevan muchos datos.

```json
@api_view(['GET'])
def list_circles(request):
    """List circles."""
    circles = Circle.objects.filter(is_public=True)
    serializer = CircleSerializer(circles, many=True)
    return Response(serializer.data)
```

## Guardado de datos mediante serializers.

### 1.- Guardar Objetos Forma 1

```python
@api_view(['POST'])
def create_circle(request):
    """Create a circle."""
    serializer = CreateCircleSerializer(data=request.data)
    # Valida que la informacion es correcta y si no envia una exception
    serializer.is_valid(raise_exception=True)
    data = serializer.data
    circle = Circle.objects.create(**data)
    
    return Response(CircleSerializer(circle).data)
```



### 2.- Sobre escritura del método save.(Guardar objetos)

Para facilitar el guardado de modelos mediante serializers se debe sobre escribir el método **create()** el cual dará un nuevo comportamiento, recibiendo los datos ya validados y guardándolos  con el Modelo.

- Se sobre escribe el método **create**
- Se anexan los validadores, esto evita que los errores se propaguen hasta el modelo.

**Serializer**

```python
""" Circle serializers."""

# Djangon
from rest_framework import serializers

# Validators
from rest_framework.validators import UniqueValidator

# Model
from cride.circles.models import Circle


class CreateCircleSerializer(serializers.Serializer):
    """Create circle serializer."""
    name = serializers.CharField(max_length=140)
    slug_name = serializers.SlugField(
        max_length=40,
       	# Se aplica  la validacion para evitar que el slug que es un dato unico se repita.
        validators=[
            UniqueValidator(queryset=Circle.objects.all())
        ]
    )
    about = serializers.CharField(
        max_length=255,
        required=False
    )

    # Recibe los datos ya validados
    def create(self, data):
        """Create circle."""
        return Circle.objects.create(**data)
```



**View**

```python
"""Circles views"""

# Django REST Framework
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Serializer
from cride.circles.serializers import CircleSerializer, CreateCircleSerializer

# Models
from cride.circles.models import Circle


@api_view(['POST'])
def create_circle(request):
    """Create a circle."""
    serializer = CreateCircleSerializer(data=request.data)
    # Valida que la informacion es correcta y si no envia una exception
    serializer.is_valid(raise_exception=True)
    # Despues de generar el serializer lo guarda mediante el metodo create dentro del serializer
    circle = serializer.save()
    
    # Retorna el modelo creado ya con todos sus datos.
    return Response(CircleSerializer(circle).data)
```





## Parsers

Ayudan a recibir datos de diferentes tipos, validan que esos datos son del tipo que dicen ser y pasan como data a nuestro request.

## Renderes

Especifican como sale el contenido y especifican esto con el Header **Accept**



## APIView





































## DOCKER COMANDOS



### Cuando cambiamos alguna dependencia

1. `export COMPOSE_FILE=local.yml`
2. `docker-compose build`



### Hacer Migraciones

1. Con los servicios de docker abajo.

2. Si no están abajo ` docker-compose down`

3. `docker volume ls`

4. `docker volume rm cride_local_postgres_data`

5. `docker-compose run --rm django python manage.py makemigrations`

6. `docker-compose run --rm django python manage.py migrate`

   

### Bajar Django

1. `docker rm -f cride-platzi_django_1`
2. ` docker-compose run --rm --service-ports django`
3. 



### Correr servicio

1. export COMPOSE_FILE=local.yml
2. docker-compose build
3. docker-compose up
4. docker-compose ps
5. docker rm -f cride_django
6. docker compose run --rm --service -ports django



### Importar datos de fixtures.

`docker-compose run --rm django python manage.py loaddata cride/circles/fixtures/circles.json`