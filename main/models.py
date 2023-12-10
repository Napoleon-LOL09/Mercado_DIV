from django.db import models
from django.contrib.auth.models import User
# Create your models here.
  
class categoria_pm (models.Model):
    class Meta:
        verbose_name_plural = 'Categorias'
        verbose_name = 'Categoria'
        db_table = 'categoria_pm'
        
    name = models.CharField(max_length=20, blank=False, null=False, unique=True)
    descripcion = models.TextField(max_length=100, blank=False, null=False, unique=True)
    
    def __str__(self):
        return self.name
    
class producto_pm (models.Model):
    class Meta:
        verbose_name_plural = 'Productos'
        verbose_name = 'Producto'
        db_table = 'producto_pm'
        
    
    name = models.CharField(max_length=100, blank=False, null=False)
    descripcion = models.TextField(max_length=100, blank=False, null=False)
    precio = models.DecimalField (blank=False, null=False, decimal_places=2, max_digits=20)
    img = models.ImageField (upload_to='productos/', blank=True)
    categoria = models.ForeignKey(categoria_pm, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name

class coment_pro (models.Model):
    class Meta:
        db_table='coment_pro'
    
    productos = models.ForeignKey(producto_pm, on_delete=models.CASCADE)
    user = models.ForeignKey (User, on_delete=models.CASCADE) 
    fecha = models.DateTimeField()
    comentario = models.TextField (null=True, blank=True)

class coment_user (models.Model):
    class Meta:
        db_table='coment_user'

    TIPOS_S = (
        ('LIKE', 'Like'),
        ('DISLIKE', 'Dislike'),
        ('COMENTARIO', 'Comentario'),
    )

    coment_proo = models.ForeignKey(coment_pro, on_delete=models.CASCADE)
    comentario = models.TextField (null=True, blank=True)
    fecha = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey (User, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=10, choices=TIPOS_S)
    
class Carrito (models.Model):
    
    class Meta:
        db_table = 'Carrito'

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    total = models.DecimalField(default=0.0, blank=True, null=True, decimal_places=2, max_digits=20)

class ProCarrito(models.Model):

    class Meta:
        db_table = 'ProCarrtio'
        
    carrito = models.ForeignKey('Carrito', on_delete=models.CASCADE)
    producto = models.ForeignKey('producto_pm', on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

class cupones(models.Model):

    class Meta:
        db_table = 'cupones'
    
    codigo = models.CharField (max_length=20,null=True, blank=True)
    descuento = models.IntegerField(null=True, blank=True)
    fecha_i = models.DateField(null=True, blank=True)
    fecha_f = models.DateField(null=True, blank=True)
    limite = models.IntegerField (null=True, blank=True)
    usado = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.codigo

class recets (models.Model):
    class Meta:
        db_table = 'recets'
    
    nombre = models.CharField (null=True, blank=True, max_length=100)
    tipo = models.CharField (null=True, blank=True, max_length=20)
    ingre = models.TextField(null=True, blank=True)
    proce = models.TextField(null=True, blank=True)
    videoo = models.FileField (null=True, blank=True, upload_to='videos/')
    imagen = models.ImageField (null=True, blank=True, upload_to='recetas/')
    categoria = models.CharField (null=True, blank=True, max_length=30)

    def __str__(self):
        return self.nombre

class bitacors (models.Model):
    class Meta:
        db_table = 'bitacors'
    
    nombre = models.CharField (null=True, blank=True, max_length=200)
    fecha = models.DateTimeField()
    comentario = models.TextField (null=True, blank=True)

class Interaccion(models.Model):
    class Meta:
        db_table = 'interacciones'
    
    TIPO_INTERACCION = (
        ('LIKE', 'Like'),
        ('DISLIKE', 'Dislike'),
        ('COMENTARIO', 'Comentario'),
    )
    
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    bitacor = models.ForeignKey(bitacors, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=10, choices=TIPO_INTERACCION)
    fecha = models.DateTimeField(auto_now_add=True)
    comentarios = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.usuario.username} - {self.tipo} - {self.fecha}"
    
class datos_envio(models.Model):
    class Meta:
        db_table = 'datos_envio'
    
    guardado = models.CharField(null=True, blank=True, max_length=50)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField(max_length=30, null=True, blank=True)
    cel = models.IntegerField(null=True, blank=True)
    cedula = models.CharField (null=True, blank=True, max_length=50)
    ciudad = models.CharField(null=True, blank=True, max_length=50) 
    provincia = models.CharField(null=True, blank=True, max_length=50)
    barrio = models.CharField (null=True, blank=True, max_length=50)
    pago = models.CharField (null=True, blank=True, max_length=40)
    tarjeta = models.CharField (null=True, blank=True, max_length=20)
    mesaño = models.CharField (null=True, blank=True, max_length=10)
    segu = models.IntegerField (null=True, blank=True)
    titular = models.CharField (null=True, blank=True, max_length=50)
    latitud = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitud = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    def __str__(self):
        return f"{self.ciudad} - {self.provincia} - {self.pago} - {self.barrio}" 

class Totales (models.Model):
    class Meta:
        db_table = 'Totales'
    
    total = models.CharField(null=True, blank=True, max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.total
