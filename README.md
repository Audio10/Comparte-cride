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

## Importar datos de un Fixtures

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



## Buenas prácticas para el diseño de un API REST

Uno de los prerequisitos para crear APIs es conocer el protocolo HTTP. Verbos, métodos, estados y las cabeceras.

Van a estar diseñando una interfaz **para programadores** para que otros programadores puedan interactuar, nos olvidaremos de los templates para que un equipo de Frontend se encargue de eso. Debemos tener la perspectiva de un usuario de API y no la de un diseñador de API.

El **objetivo** es algo que siempre se deben preguntar qué problema deben de resolverle al usuario final nuestra API. El **éxito** de nuestra API se mide por qué tan rápido nuestros compañeros pueden usarla.

**REST**: Es una serie de principio de cómo diseñar una web service. Un estilo de arquitectura.

### **HTTP Status Code**:

- 201: Creado
- 304: No modificado
- 400: Bad request( Hiciste algo mal.)
- 404: No encontrado
- 401: No autorizado
- 403: Prohibido o restringido.
- 500: Internal Server Error (Yo hice algo mal.)

### **Pro tips**:

- SSL
- Caché
- Valida
- CSRF o Cross-Site Request Forgery
- Limita los requests
- Complementa tu API con un SDK

## Parsers

Ayudan a recibir datos de diferentes tipos, validan que esos datos son del tipo que dicen ser y pasan como data a nuestro request.

## Renderes

Especifican como sale el contenido y especifican esto con el Header **Accept**



## APIView

Es una clase especializada de la cual heredamos, esta ocupa por default el **request** de Django REST Framework y no el **HttpRequest** de Django.

Para la implementacion es recomendable crear un modulo de **views** el cual contendra los siguientes archivos.

- __init__.py: Donde se importan los archivos que contienen las vistas. Y realizar un import mas general.

- Archivos.py: Los cuales contienen las vistas  y se importan en el init.

  

## App de usuarios.

Esta APP va orientada a realizar las siguientes funciones.

1. Login
2. SignUp
3. Verify User from email confirmation.



#### __init__.py

En este archivo se importan las vistas provenientes de los archivos que contiene el modulo **views**,

```python
from .users import *
```

#### Users.py

Este archivo es nombrado como la APP, por lo general los serializer, modelos llevan el mismo nombre que la app y llevan la misma secuencia.

**APIView.**

- Las vistas basadas en clases son extensiones de clases especializadas, en este caso **APIView** es la vista de la cual debemos extender para generar una View basada en clase para Rest Framework. En esta ya estan creados los metodos HTTP para las peticiones y solo hay que sobre escribirlos.
- Este ya ocupa el request de Django REST Framework.

```python
"""Users views."""

# Django REST Framework

# This is the import for inherit the functionality for the Class based view.
from rest_framework.views import APIView
from rest_framework import status
# You need to import de Response from rest_framework.
from rest_framework.response import Response

# Serializers
from cride.users.serializers import (
    UserLoginSerializer,
    UserModelSerializer,
    UserSignUpSerializer,
    AccountVerificationSerializer
)


class UserLoginAPIView(APIView):
    """1.- User login API view.
    When create a User's Login return the user and a token.
    And if the User's data is incorrect return the error.
    """
    
    def post(self, request, *args, **kwargs):
        """Handle HTTP POST request."""
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, token = serializer.save()
        data = {
            'user': UserModelSerializer(user).data,
            'access_token': token
        }
        return Response(data, status=status.HTTP_201_CREATED)


class UserSignUpAPIView(APIView):
    """User signup API view.
    It register a new User if the data is not duplicate.
    """
    
    def post(self, request, *args, **kwargs):
        """Handle HTTP POST request."""
        serializer = UserSignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Extract the data from the UserModelSerializer.
        data = UserModelSerializer(user).data,
            
        return Response(data, status=status.HTTP_201_CREATED)


class AccountVerificationAPIView(APIView):
    """Account verification API view."""
    
    def post(self, request, *args, **kwargs):
        """Handle HTTP POST request."""
        serializer = AccountVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {'message': 'Congratulations, now go share some rides!'}
            
        return Response(data, status=status.HTTP_200_OK)
    
```



#### Serializers.

```python
"""Users serializers."""

# Django 
# authentica: provide the authenticate for username and password.
# password_validation: validate that the password is correct.
from django.contrib.auth import authenticate, password_validation

# Django REST Framework
from rest_framework import serializers
# Model for create a Token.
from rest_framework.authtoken.models import Token

# Validators
from rest_framework.validators import UniqueValidator
from django.core.validators import RegexValidator

# Models
from cride.users.models import User, Profile

# Email
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

# JWT
import jwt

# Utilities
from django.conf import settings
from django.utils import timezone
from datetime import timedelta


class UserModelSerializer(serializers.ModelSerializer):
    """User model serializer.
     ModelSerializer is a class that implements the Model and fields for Us.
    """
    
    class Meta:
        """Meta class.
        In this method we override the class Meta and implements the model and de fields 				 that we are goint to use.
        """
        
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'phone_number'
        )


class UserSignUpSerializer(serializers.Serializer):
    """User sign up serializer.
    
    Handle sign up data validation and user/profile creation.
    """
    
    email = serializers.EmailField(
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ]
    )
    
    username = serializers.CharField(
        min_length=4,
        max_length=20,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    
    # Phone number
    phone_regex = RegexValidator(
        regex=r'\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: +999999999. Up to 15 digits allowed."
    )
    
    phone_number = serializers.CharField(
        validators=[phone_regex]
    )
    
    # Password
    password = serializers.CharField(min_length=8, max_length=64)
    password_confirmation = serializers.CharField(min_length=8, max_length=64)
    
    # Name 
    first_name = serializers.CharField(min_length=2, max_length=30)
    last_name = serializers.CharField(min_length=2, max_length=30)
    
    def validate(self, data):
        """Verify passwords match."""
        passwd = data['password']
        passwd_conf = data['password_confirmation']
        if passwd != passwd_conf:
            raise serializers.ValidationError("Passwords don't match.")
        
        # Django's Validator for passwords.
        password_validation.validate_password(passwd)
        return data
    
    def create(self, data):
        """Handle user and profile creation.
        It is called when yout user the save method.
        Delete the password_confirmation field from the data after validate.
        This Create a User, and put is_verified False for default, create a Prifile for 				the user and implements the send_confirmation_email method.
        """
        data.pop('password_confirmation')
        user = User.objects.create_user(**data, is_verified=False)
        Profile.objects.create(user=user)
        self.send_confirmation_email(user)
        return user
    
    def send_confirmation_email(self, user):
        """Send account verification link to given user."""
        verification_token = self.gen_verification_token(user)
        subject = 'Welcome @{}! Verify your account to start using Comparte Ride'.format(user.username)
        from_email = 'Comparte Ride <noreply@comparteride.com>'
        content = render_to_string(
            'emails/users/account_verification.html',
            {'token': verification_token, 'user': user}
        )
        msg = EmailMultiAlternatives(subject, content, from_email, [user.email])
        msg.attach_alternative(content, "text/html")
        msg.send()

    def gen_verification_token(self, user):
        """Create JWT token that the user can use to verify its account."""
        exp_date = timezone.now() + timedelta(days=3)
        payload = {
            'user': user.username,
            'exp': int(exp_date.timestamp()), # Expiration date Timestamp integer.
            'type': 'email_confirmation'
        }
        
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
        return token.decode()
    

class UserLoginSerializer(serializers.Serializer):
    """User login serializer.
    
    Handle the login request data.
    """
    
    email = serializers.EmailField()
    password = serializers.CharField(min_length=8, max_length=64)
    
    def validate(self, data):
        """Check credentials."""
        user = authenticate(username=data['email'], password=data['password'])
        if not user:
            raise serializers.ValidationError('Invalid credentials')
        if not user.is_verified:
            raise serializers.ValidationError('Account is not active yet :(')
        self.context['user'] = user
        return data
    
    def create(self, data):
        """Generate or retrieve new token."""
        token, created = Token.objects.get_or_create(user=self.context['user'])
        return self.context['user'], token.key
    
    
class AccountVerificationSerializer(serializers.Serializer):
    """Account verification serializer."""
        
    token = serializers.CharField()
        
    def validate_token(self, data):
        """Verify token is valid."""
        try:
            payload = jwt.decode(data, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise serializers.ValidationError('Verification link has expired.')
        except jwt.PyJWTError:
            raise serializers.ValidationError('Invalid token2')   
        if payload['type'] != 'email_confirmation':
            raise serializers.ValidationError('Invalid token')
            
        self.context['payload'] = payload
        return data
        
    def save(self):
        """Update user's verified status."""
        payload = self.context['payload']
        user = User.objects.get(username=payload['user'])
        user.is_verified=True
        user.save()
    
    
```

1. **ModelSerializer** es una clase especializada que te permite convertir un modelo a un Serializer, lo cual facilita la creación del serializer basado en un Modelo previamente establecido. Se debe especificar el modelo del cual se creara el template y los fields que se usaran.

2. Para la autenticación se ocupara la que viene con Django usando authenticate, la cual compara con nuestro modelo de Usuario especificado para el admin.

   -  Se  valida metiante el authenticate, el cual retorna un usuario si este es authenticado correctamente.

   - Si no existe el usuario o no coinciden los datos regresa none.

   - Todos los serializers tienen un objeto llamado **contex**, en el cual se guardan argumentos. En este caso se creo un argumento llamado user para poder guardar el usuario en caso de que sea encontrado.

   - Se genera un Token basado en el usuario, este se guarda en base de datos y en caso de ya existir lo reenvia, es decir siempre sera el mismo.

   - Para acceder al valor del token se utiliza el atributo **key**.

     

## Extra fields on many-to-many relationships. 



### Membership model

```python
"""Membership model."""

# Django
from django.db import models

# Utilities
from cride.utils.models import CRideModel


class Membership(CRideModel):
    """Membership model.
    
    A membership is the table that holds the relationship between
    a user and a circle.
    """
    
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    profile = models.ForeignKey('users.Profile', on_delete=models.CASCADE)
    circle = models.ForeignKey('circles.Circle', on_delete=models.CASCADE)
    
    is_admin = models.BooleanField(
        'circle admin',
        default=False,
        help_text="Circle admins can update the circle's data and manage its members."
    )
    
    # Invitations
    used_invitations = models.PositiveSmallIntegerField(default=0)
    remaining_invitation = models.PositiveSmallIntegerField(default=0)
    invited_by = models.ForeignKey(
        'users.User',
        null=True,
        on_delete=models.SET_NULL,
        related_name='invited_by'
    )
    
    # Stats
    rides_taken = models.PositiveIntegerField(default=0)
    rides_offered = models.PositiveIntegerField(default=0)
    
    # Status
    is_active = models.BooleanField(
        'active status',
        default=True,
        help_text='Only active users are allowed to interact in the circle.'
    )
    
    def __str__(self):
        """Return username and circle."""
        return '@{} at #{}'.format(
            self.user.username,
            self.circle.slug_name
        )
    
    
```



### Circle model.

```python
"""Circle model."""

# Django
from django.db import models

# Utilities
from cride.utils.models import CRideModel


class Circle(CRideModel):
    """Circle model.

    A circle is a private group where rides are offered and taken
    by its members. To join a circle a user must receive an unique
    invitation code from an existing circle member.
    """

    name = models.CharField('circle name', max_length=140)
    slug_name = models.SlugField(unique=True, max_length=40)

    about = models.CharField('circle description', max_length=255)
    picture = models.ImageField(upload_to='circles/pictures', blank=True, null=True)
    
    members= models.ManyToManyField(
        # Referencia
        'users.User',
        # Atravez de.
        through='circles.Membership',
        # Atravez de que campos estas definiendo la relacion?
        through_fields=('circle','user')
    )

    # Stats
    rides_offered = models.PositiveIntegerField(default=0)
    rides_taken = models.PositiveIntegerField(default=0)

    verified = models.BooleanField(
        'verified circle',
        default=False,
        help_text='Verified circles are also known as official communities.'
    )

    is_public = models.BooleanField(
        default=True,
        help_text='Public circles are listed in the main page so everyone know about their existence.'
    )

    is_limited = models.BooleanField(
        'limited',
        default=False,
        help_text='Limited circles can grow up to a fixed number of members.'
    )
    members_limit = models.PositiveIntegerField(
        default=0,
        help_text='If circle is limited, this will be the limit on the number of members.'
    )

    def __str__(self):
        """Return circle name."""
        return self.name

    class Meta(CRideModel.Meta):
        """Meta class."""

        ordering = ['-rides_taken', '-rides_offered']
```



## ViewSet

Clase especializada que implementa todas las operaciones CRUD. Esta basada en la recopilación de mixins. Y en caso de querer cambiar la funcionalidad o aplicar filtros a **queryset** se pueden sobre escribir los métodos de ViewSet.



### Mixin

Una clase que expone métodos y estos métodos pueden ser llamados por otras clases eventualmente.



### Serializer

Se debe crear un **Serializer** que extienda de **ModelSerializer**, el cual ya es una clase especializada en la cual solo se especifica el **modelo** y los **fields**.

```python
"""Circle serializers."""

# Django REST Framework
from rest_framework import serializers

# Model
from cride.circles.models import Circle


class CircleModelSerializer(serializers.ModelSerializer):
    """Circle model serializer."""
    
    class Meta:
        """Meta class."""
        
        model = Circle
        fields = (
            'id', 'name','slug_name',
            'about', 'picture',
            'rides_offered', 'rides_taken',
            'verified', 'is_public',
            'is_limited', 'members_limit'
        )
```



### ViewSet (View)

Un ViewSet es una Vista basa de Clase que extiende la funcionalidad de un CRUD, sin necesidad de sobre extender el modelo. En este solo se especifica el **queryset**, **serializer_class**.

```python
"""Circle views."""

# Django REST Framework
from rest_framework import viewsets

# Models 
from cride.circles.models import Circle

# Serializers
from cride.circles.serializers import CircleModelSerializer


class CircleViewSet(viewsets.ModelViewSet):
    """Circle view set."""
    
    queryset = Circle.objects.all()
    serializer_class = CircleModelSerializer
```



### URLs

Dentro de las URL se aplica el registro de un router, el cual es capas de registrar mediante expresiones regulares un **ViewSet**.

```python
"""Circles URLs."""

# Django
from django.urls import path, include

# Django REST Framework
from rest_framework.routers import DefaultRouter

# Views importando el archivo circles en la carpeta views.
from .views import circles as circle_views

router = DefaultRouter()
router.register(r'circles', circle_views.CircleViewSet, basename='circle')

urlpatterns = [
    path('', include(router.urls))
]
```



## Definir Autorización (Token)

Para agregar autorización a nuestros EndPoints debemos usar implementar en **settings** una configuración especial.

```python
# Django REST Framework
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication'
    ]
}
```

Mientras que en la vista se debe definir la variable **permission_classes**.

```python
"""Circle views."""

# Django REST Framework
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

# Models 
from cride.circles.models import Circle

# Serializers
from cride.circles.serializers import CircleModelSerializer


class CircleViewSet(viewsets.ModelViewSet):
    """Circle view set."""
    
    queryset = Circle.objects.all()
    serializer_class = CircleModelSerializer
    permission_classes = (IsAuthenticated,)
```



## Paginación



```python
# Django REST Framework
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication'
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 3,
}
```



## Creación de circulos



```python
"""Circle views."""

# Django REST Framework
from rest_framework import viewsets

# Permissions
from cride.circles.permissions import IsCircleAdmin
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import MethodNotAllowed

# Serializers
from cride.circles.serializers import CircleModelSerializer

# Models
from cride.circles.models import Circle, Membership


class CircleViewSet(viewsets.ModelViewSet):
    """Circle view set."""

    serializer_class = CircleModelSerializer
    # Field to Research a circle, ID is the Default field if you don't specify this field.
    lookup_field = 'slug_name'

    def get_queryset(self):
        """Restrict list to public-only."""
        queryset = Circle.objects.all()
        # Introspective action allowance.
        if self.action == 'list':
            return queryset.filter(is_public=True)
        return queryset
    
    def get_permissions(self):
        """Assign permissions based on action."""
        permissions = [IsAuthenticated]
        if self.action in ['update', 'partial_update']:
            permissions.append(IsCircleAdmin)
        return [permission() for permission in permissions]

    def perform_create(self, serializer):
        """Assign circle admin."""
        circle = serializer.save()
        # The user is in the request.user
        user = self.request.user
        profile = user.profile
        # Create a Membership.
        Membership.objects.create(
            user=user,
            profile=user.profile,
            circle=circle,
            is_admin=True,
            remaining_invitations=10
        )
    
    def destroy(self, request, pk=None):
        raise MethodNotAllowed('DELETE')
```

### get_queryset.

Es el metodo donde se define el queryset. Dentro de este se puede especificar la logica especial en este caso el queryset cuando el action es list, solo se mostraran los círculos que son publicos.

### perform_create

**ModelViewSet** implementa el metodo **create** el cual especifica el serializer y lo valida, pero dentro de este metodo se llama **perform_create** que es el lugar en donde se debe escribir la lógica, su unica funcionalidad antes de sobreescribirlo es llamar el metodo **save** del serializer.

### destroy

Metodo del **ModelViewSet** en el se escribe la logica del **Delete** pero en este caso se va a establecer que es un metodo no permitido ya que nadie puede eliminar los circulos. Se implementa **MethodNotAllowed** proveniente de **rest_framework.exceptions** para establecer el raise de que este metodo no es permitido.

### get_permissions





## Validacion Circulo es limitado.

Dentro del serializer se crea una validacion en la cual se especifica que si un circulo es limitado, debe establecer cual es el limite. Y si alguno de los dos esta presente el circulo es limitado y deben proporcionar ambos campos.

```python
"""Circle serializers."""

# Django REST Framework
from rest_framework import serializers

# Model
from cride.circles.models import Circle


class CircleModelSerializer(serializers.ModelSerializer):
    """Circle model serializer."""
    
    members_limit = serializers.IntegerField(
        required=False,
        min_value=10,
        max_value=32000
    )
    
    is_limited = serializers.BooleanField(default=False)
    
    class Meta:
        """Meta class."""
        
        model = Circle
        fields = (
            'id', 'name','slug_name',
            'about', 'picture',
            'rides_offered', 'rides_taken',
            'verified', 'is_public',
            'is_limited', 'members_limit'
        )
        
        read_only_fields = (
            'is_public',
            'verified',
            'rides_offered',
            'rides_taken',
        )
    
    def validate(self, data):
        """Ensure both members_limit and is_limited are present."""
        members_limit = data.get('members_limit', None)
        is_limited = data.get('is_limited', False)
        if is_limited ^ bool(members_limit):
            raise serializers.ValidationError('If circle is limited, a member limit must be provided')
        
        return data
```



## Update de círculo, custom permissions y DRF Mixins

Creacion de un permiso custom, limitar update a solo administradores y eliminacion de posibilidad de borrar un Circulo.



### Evitar metodo Delete.

Hay dos formas de delimitar los metodos HTTP permitidos.

1. En vez de importar ModelViewSet, solo se extienden los Mixins que lo componen y queremos utilizar.

2. Sobre escribir los metodos e implementar excepción NotAllowed.

   ```python
       def destroy(self, request, pk=None):
           raise MethodNotAllowed('DELETE')
   ```



### Creacion Permiso Custom.

Se crea un modulo de permisos y se generan estos mismos.

Para crear un permiso Custom se implementa la clase BasePermission, proveniente de **rest_framework.permissions**. 

Se sobre escribe el metodo **has_object_permission**. Este permiso valida que eres administrador y estas activo.

```python
"""Circles permission classes."""

# Django REST Framework
from rest_framework.permissions import BasePermission

# Models
from cride.circles.models import Membership

class IsCircleAdmin(BasePermission):
    """Allow acces. only to circle admins."""
    
    def has_object_permission(self, request, view, obj):
        """Verify user have a membership in the obj."""
        try:
            Membership.objects.get(
                user=request.user,
                circle=obj,
                is_admin=True,
                is_active=True
            )
        except Membership.DoesNotExist:
            return False
        return True
```



#### Asignacion de permisos 



```python
def get_permissions(self):
        """Assign permissions based on action."""
    	
      	# Array for permissions
        permissions = [IsAuthenticated]
        # filter for Introspective actions. When is update or partial you need to be a Adminsitrador de circulo. If you are a admin append the permission for admin.
        if self.action in ['update', 'partial_update']:
            permissions.append(IsCircleAdmin)
        
        # Execute the permissions.
        return [permission() for permission in permissions]
```



## Creacion de acciones extra para routing.

Existen dos tipos de acciones las que son de detalle y las que no lo son.

**De detalle:** Parten apartir de un ID o lookup_field.

### Actualizando APP Usuarios a ViewSet.

En este caso se ocupara **GenericViewSet** ya que no tenemos preferencia en algun modelo de este mismo.

```python
"""Users views."""

# Django REST Framework we use viewsets form implements actions.
from rest_framework import status, viewsets
from rest_framework.response import Response

# Actions
from rest_framework.decorators import action

# Serializers
from cride.users.serializers import (
    UserLoginSerializer,
    UserModelSerializer,
    UserSignUpSerializer,
    AccountVerificationSerializer
)

class UserViewSet(viewsets.GenericViewSet):
    """User view set.
    Handle sign up, login and account verification.
    """

    # It's not a detail action, and we are using post verb.
    @action(detail=False, methods=['POST'])
    def login(self, request):
        """User login. """
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, token = serializer.save()
        data = {
            'user': UserModelSerializer(user).data,
            'access_token': token
        }
        return Response(data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['POST'])
    def signup(self, request):
        """User signup."""
        serializer = UserSignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = UserModelSerializer(user).data,
            
        return Response(data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['POST'])
    def verify(self, request):
        """Account verification."""
        serializer = AccountVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {'message': 'Congratulations, now go share some rides!'}
            
        return Response(data, status=status.HTTP_200_OK)
```

#### Routing

En este caso como en el **ModelViewSet** ocupamos el routing por medio de **DefaultRouter**, Pero el path sera **users/NombreFuncion/**. En este caso con el codigo escrito anteriormente tendremos las siguientes URL.

1. localhost:8000/users/signup/
2. localhost:8000/users/login/
3. localhost:8000/users/verify/

```python
"""Users URLs."""

# Django
from django.urls import path, include

# Django REST Framework
from rest_framework.routers import DefaultRouter

# Views
from .views import users as user_views

router = DefaultRouter()

router.register(r'users', user_views.UserViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls))
]
```



## Retrive User

En este caso se reescribe el metodo retrieve. Se recibe la response por defecto y se agrega al la respuesta los circulos a los que pertenece el Usuario aplicando el Serializer correspondiente.

**NOTA:** Recordar que **.data** retorna la informacion preconstruida por el serializer.

```python
def retrieve(self, request, *args, **kwargs):
        """Add extra data to the response."""
        response = super(UserViewSet, self).retrieve(request, *args, **kwargs)
        circles = Circle.objects.filter(
            members=request.user,
            membership__is_active=True
        )
        data = {
            'user': response.data,
            'circles': CircleModelSerializer(circles, many=True).data
        }
    
        response.data = data
        return response
```



## Update User Data

Para actualizar datos de algun usuario es necesario aplicar **mixins.UpdateModelMixin** la cual es una clase especializada para actualizaciones. Se aplica la regla dentro de los permisos para que solo  el propietario de la cuenta pueda actualizar los datos del mismo usuario. 

```python
class UserViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.UpdateModelMixin):
    """User view set.
    Handle sign up, login and account verification.
    """

    queryset = User.objects.filter(is_active=True, is_client=True)
    serializer_class = UserModelSerializer
    lookup_field = 'username'

    def get_permissions(self):
        """Assign permissions based on action."""
        if self.action in ['signup', 'login', 'verify']:
            permissions = [AllowAny]
        elif self.action in ['retrieve', 'update', 'partial_update']:
            permissions = [IsAuthenticated, IsAccountOwner]
        else:
            permissions = [IsAuthenticated]
        return [p() for p in permissions]
        

```



## Update Profile Data.

Se anexa la URL: {{host}}/users/juan/profile/ la cual esta destinada a actualizar el profile del usuario mediante el lookup_field. Aplica la recollecion



```python
    @action(detail=True, methods=['PUT','PATCH'])
    def profile(self, request, *args, **kwargs):
        """Update  profile data."""
        user = self.get_object()
        profile = user.profile
        partial = request.method = 'PATCH'
        serializer = ProfileModelSerializer(
            profile,
            data=request.data,
            partial=partial
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = UserModelSerializer(user).data
        return Response(data)
```





































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


