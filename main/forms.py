from typing import Any
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import categoria_pm, producto_pm, cupones, recets, bitacors, datos_envio

 
class log_user (AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({'class': 'camp1'})
        self.fields['password'].widget.attrs.update({'class': 'camp1'})


class reg_user (forms.Form):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class' : 'camp'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'class' : 'camp '}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class' : 'camp'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class' : 'camp'}))

class categoria_Pf (forms.ModelForm):
    name = forms.CharField (required=True, label= 'Nombre de la categoria:')
    descripcion = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'cols': 35}))

    class Meta:
        model = categoria_pm
        fields = ['name', 'descripcion']

class producto_Pf (forms.ModelForm):
    name = forms.CharField (required=True)
    descripcion = forms.CharField(required=True, widget=forms.Textarea(attrs={'rows': 5, 'cols': 35}))
    precio = forms.DecimalField (required=True)
    img = forms.ImageField (required = False)
    categoria = forms.ModelChoiceField(queryset=categoria_pm.objects.all(), 
                empty_label="Selecciona una categoría",  
                label="Categoría", required=True) 

    class Meta:
        model = producto_pm
        fields = ['name', 'descripcion', 'precio', 'img', 'categoria']

class cuponn (forms.ModelForm):
    codigo = forms.CharField (required=True, max_length=30)
    descuento = forms.IntegerField(required=True)
    fecha_i = forms.DateField(required=True, widget=forms.DateInput(attrs={'type' : 'date'}))
    fecha_f = forms.DateField(required=True, widget=forms.DateInput(attrs={'type' : 'date'}))
    limite = forms.IntegerField (required=True)

    class Meta:
        model = cupones
        fields = ['codigo', 'descuento', 'fecha_i', 'fecha_f', 'limite']

class recetass (forms.ModelForm):
    nombre = forms.CharField (required=True, widget=forms.TextInput(attrs={'placeholder' : 'Nombre Receta...'}))
    tipo = forms.CharField (required=False)
    ingre = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 5, 'cols': 35}))
    proce = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 5, 'cols': 35}))
    video = forms.FileField (required=False)
    imagen = forms.ImageField (required=True)
    
    #Categorias Existentes
    catt_cap = recets.objects.values_list('categoria', flat=True).distinct()
    catt_record = [(cat, cat) for cat in catt_cap]
    catt_record.insert(0, ('', 'Seleccione la categoria'))
    cat_si = forms.ChoiceField(
        choices=catt_record,
        required=False,
    )
    #Categoria nueva
    categoria = forms.CharField (required=False, widget=forms.TextInput(attrs={'placeholder': 'Categoria...'}))

    class Meta:
        model = recets
        fields = ['nombre', 'ingre', 'proce', 'video', 'imagen', 'categoria', 'cat_si']


class bitacora_D (forms.ModelForm):
    fecha = forms.DateField (required=True, widget=forms.DateInput(attrs={'type': 'date'}))
    comentario = forms.CharField (required=True, widget=forms.Textarea(attrs={'placeholder' : 'Ingrese su apunte diario', 'row' : 5, 'cols' : 35}))

    class Meta:
        model = bitacors
        fields = ['nombre', 'fecha', 'comentario']


class traking_datos (forms.ModelForm):

    cel = forms.IntegerField(required=True)
    cedula = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'placeholder': 'Cedula...'}))
    ciudad = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder' : 'Ciudad...'}))
    provincia = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder' : 'Provincia...'}))
    barrio = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder' : 'Barrio...'}))
    
    class Meta:
        model = datos_envio
        fields = ['cel', 'cedula', 'ciudad', 'provincia', 'barrio']