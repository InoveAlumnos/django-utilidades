from django.test import TestCase
from e_commerce import models
from django.test import Client
from django.contrib.auth.models import User


class MiClaseDePrueba(TestCase):
    '''
    Clase de prueba para hacer Unit Test sobre las entidades de la base de datos.
    '''
    titulo = 'Título de prueba'
    descripción = 'Descripción de prueba'
    precio = 10.99
    stock = 100
    imagen = 'https://www.inove.com.ar'

    def setUp(self):
        '''
        Aquí configuramos las condiciones de la prueba, por lo general insertamos a la DB
        NOTE: Aquí debemos crear los objetos para la base de datos de prueba, 
        de lo contrario, se insertarán en la base de datos del sistema.
        '''
        comic = models.Comic.objects.create(
            marvel_id=1,
            title=self.titulo,
            description=self.descripción,
            price=self.precio,
            stock_qty=self.stock,
            picture=self.imagen
        )

    def test_pruebas_de_integridad_de_datos(self):
        '''
        Este método realiza la prueba de integridad de los dato insertados en la base de datos, 
        aprovechando "self.atributo" para verificarlos. 
        '''
        # Llamamos al objeto seteado:
        comic = models.Comic.objects.get(marvel_id=1)
        # Extraemos sus atributos:
        titulo = comic.title
        descripción = comic.description
        precio = comic.price
        stock = comic.stock_qty
        imagen = comic.picture
        # Generamos dos listas para compararlas, una con los datos extraidos del modelo
        # y otra con los datos que fueron insertados en el modelo
        object_values = [titulo, descripción, precio, stock, imagen]
        test_values = [self.titulo, self.descripción,
                       self.precio, self.stock, self.imagen]
        # Comparamos uno a uno los datos:
        for index in range(len(test_values)):
            if object_values[index] != test_values[index]:
                # Si los datos son distintos, hacemos que la prueba de fallida:
                self.assertEqual(object_values[index], test_values[index])
        # Si los datos son iguales, verificamos que las pruebas son exitosas:
        self.assertTrue(True)


class PruebaDeAPIs(TestCase):
    '''
    Test para las APIs del sistema, utilizaremos una DB y un server de prueba.
    '''
    # NOTE: Configuramos los atributos de la clase para utilizarlos en todos los métodos:
    username = 'root'
    password = '12345'
    email = 'algo@algo.com'
    user = None
    comic = None

    # Client() es un objeto que gestiona la conexión con los endpoints, como lo haría un request
    client = Client()

    def setUp(self):
        '''
        Aquí configuramos las condiciones de la prueba, 
        creamos un comic y generamos la conexión al server de prueba
        NOTE: Aquí debemos crear los objetos para la base de datos de prueba, 
        de lo contrario, se insertarán en la base de datos del sistema.
        '''

        # NOTE: Creamos un superusuario para las pruebas:
        self.user = User.objects.create_superuser(
            self.username, self.email, self.password)
        # Ahora lo autenticamos en el servidor de pruebas:
        self.client.login(username=self.username, password=self.password)

        # Insertamos un comic en la DB de prueba:
        self.comic = models.Comic.objects.create(
            marvel_id=2,
            title='Título de prueba 2',
            description='Descripción de prueba 2',
            price=10.99,
            stock_qty=100,
            picture='www.algo.com/imagen.jpg'
        )

    def test_api_comics(self):
        '''
        Test de endpoint: comics/get-post
        Pruebas sobre todos los métodos.
        '''
        # Preparamos los datos:
        endpoint = '/e-commerce/comics/get-post'
        data = {
            'marvel_id': 3,
            'title': 'Título de prueba 3',
            'description': 'Descripción de prueba 3',
            'price': 10.99,
            'stock_qty': 100,
            'picture': 'https://www.inove.com.ar'
        }

        # GET test:
        resp = self.client.get(endpoint)
        self.assertEqual(resp.status_code, 200)

        # POST test:
        resp = self.client.post(
            endpoint, data, content_type="application/json")
        self.assertEqual(resp.status_code, 201)

        # PUT test:
        resp = self.client.put(endpoint, data, content_type="application/json")
        self.assertEqual(resp.status_code, 405)

        # PATCH test:
        resp = self.client.patch(
            endpoint, data, content_type="application/json")
        self.assertEqual(resp.status_code, 405)

        # DELETE test:
        resp = self.client.delete(
            endpoint, data, content_type="application/json")
        self.assertEqual(resp.status_code, 405)