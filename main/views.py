from django.shortcuts import render, redirect, get_object_or_404
from django.db import IntegrityError
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q, Count
from django.utils import timezone
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth import login, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import ObjectDoesNotExist
from random import sample
from .models import User, categoria_pm, producto_pm, Carrito, ProCarrito, cupones, recets, bitacors, Interaccion, coment_pro, coment_user, datos_envio, Totales
from .forms import reg_user, log_user, categoria_Pf, producto_Pf, cuponn, recetass, bitacora_D, traking_datos


# Create your views here.
def register_login (request):
    formR = None
    formL = None
    Erro_U = None  
    Erro_UC = None
    Erro_C = None
    Erro_E = None
    info = ""

    if request.method == 'POST':
        if 'register' in request.POST:
            formR = reg_user(request.POST)
            if formR.is_valid():
                username = formR.cleaned_data['username']
                email = formR.cleaned_data['email']
                password = formR.cleaned_data['password1']
                password2 = formR.cleaned_data['password2']

                if not User.objects.filter(username=username).exists():
                    if not User.objects.filter (email=email).exists():
                        if password == password2:
                            try:
                                user = User.objects.create_user(username=username, email=email, password=password)
                                user.save()
                                info = "Se ha registrado con exito"
                                formR = reg_user()
                                formL = log_user()
                            except IntegrityError:
                                messages.error (None, "Ocurrió un error al registrar el usuario.")
                        else:
                            Erro_C = "Las contraseñas no coinciden"
                            formL = log_user()  
                    else:
                        Erro_E = "El correo electronico ya esta en uso"
                        formL = log_user()  
                else: 
                    Erro_U =  "Usuario ya registrado"
                    formL = log_user()
            else:
                Erro_E = "Coloque una direccion de correo valida"
                formL = log_user

        elif 'login' in request.POST:
            formL = log_user(request, data=request.POST)
            if formL.is_valid():
                user = formL.get_user()
                login(request, user)
                
                if user.is_staff:
                    return redirect('Admin_v/menu')
                else:
                    return redirect('User_v/menu')
            else:
                Erro_UC = "Usuario o Contraseña Incorrecta"
                formL = log_user()
                formL.fields['username'].initial = request.POST['username']
                formR = reg_user()      
    else:
        formR = reg_user()
        formL = log_user()
        

    return render(request, 'base.html', {'formR': formR, 'formL': formL, 
                "Erro_UC" : Erro_UC, "Erro_U": Erro_U, "Erro_C": Erro_C, "Erro_E" : Erro_E,
                "info" : info })

def reset_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = get_user_model().objects.get(email=email)
        except get_user_model().DoesNotExist:
            user = None

        if user:
            uidb64 = urlsafe_base64_encode(user.pk.to_bytes(4, byteorder='big'))
            token = default_token_generator.make_token(user)
            return redirect('new_password', uidb64=uidb64, token=token)
        else:
            messages.error (request, "El correo no se encuentra registrado")
            return render (request, 'reset_password.html')
    
    return render(request, 'reset_password.html')

def new_password(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).hex()
        user = get_user_model().objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            # Actualizar la contraseña del usuario
            new_password = request.POST.get('new_password')
            rept_password = request.POST.get ('repet_password')
            if new_password == rept_password:
                user.set_password(new_password)
                user.save()
                return redirect('password_reset_complete')
            else:
                messages.error (request, 'Las contraseñas no coinciden')
                return render(request, 'new_password.html')
    
    return render(request, 'new_password.html')

def password_reset_complete (request):
    return render(request, 'password_reset_complete.html')

#Vistas de Administrador
@login_required
def menu_a (request):
    ids_remo = [30,31] #Valores para filtrar)
    bd_productos = producto_pm.objects.exclude(id__in=ids_remo) #Todos los productos menos los de ids_remo
    bd_recetas = recets.objects.all()

    promo = producto_pm.objects.filter(id__in=ids_remo) #Solo los productos del Ids_remo

    img_promos = [  #Imagenes para el carrusel
        'imagenes/menu_ae/promo1.png',
        'imagenes/menu_ae/promo2.png'
    ]

    #Muestra los productos y su cantidad en el carrito del header
    try:
        carrito = Carrito.objects.get(usuario=request.user)
        pro_carrito = ProCarrito.objects.filter(carrito=carrito)
    except ObjectDoesNotExist:
        carrito = None
        pro_carrito = None
    
    #Funcion del buscador
    if request.GET.get('search_P'):
        search_term = request.GET.get('search_P')
        bd_pro = bd_productos.filter(name__icontains=search_term)
        filtrado = list(bd_pro.values('name', 'id'))
        return JsonResponse({'filtrado': filtrado})
    
    return render(request, 'Admin_v/menu.html', {'bd_productos' : bd_productos,
                                                 'bd_recetas' : bd_recetas, 
                                                 'pro_carrito' : pro_carrito,
                                                 'promo' : promo, 'img_promos' : img_promos})

@login_required
def usuarios (request):
    usuarios = User.objects.all()

    #Mostrar productos hasta ahora
    try:
        carrito = Carrito.objects.get(usuario=request.user)
        pro_carrito = ProCarrito.objects.filter(carrito=carrito)
    except ObjectDoesNotExist:
        carrito = None
        pro_carrito = None

    if request.method == 'POST':
        user_id = request.POST.get('user_id')

        try:
            user = User.objects.get(pk=user_id)
            user.is_staff = not user.is_staff  # Cambia el estado de is_staff
            user.save()
            return render (request,'Admin_v/usuarios.html', {"usuarios": usuarios ,"is_staff": user.is_staff})
        except User.DoesNotExist:
            return JsonResponse({"error": "Usuario no encontrado"}, status=404)

    return render(request, 'Admin_v/usuarios.html', {"usuarios": usuarios, 
                                                     "pro_carrito" : pro_carrito})

@login_required
def eliminar_usuario(request, registro_id):
    usuario = get_object_or_404(User, pk=registro_id)
    usuario.delete()
    return redirect('Admin_v/usuarios')

@login_required
def categoria(request):
    catego = categoria_pm.objects.all()
    
    Error1 = None
    Error2 = None

    #Mostrar los productos en el header
    try:
        carrito = Carrito.objects.get(usuario=request.user)
        pro_carrito = ProCarrito.objects.filter(carrito=carrito)
    except ObjectDoesNotExist:
        carrito = None
        pro_carrito = None


    paginador = Paginator(catego, 6)
    page = request.GET.get('page')

    try:
        catego = paginador.page(page)
    except PageNotAnInteger:
        catego = paginador.page(1)
    except EmptyPage:
        catego = paginador.page(paginador.num_pages)

    if request.method == 'POST':
        form = categoria_Pf(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            descripcion = form.cleaned_data['descripcion']

            # Verificar si ya existe un registro con el mismo nombre (ignorando mayúsculas y minúsculas)
            existing = categoria_pm.objects.filter(Q(name__iexact=name) | Q(descripcion__iexact=descripcion))
            if existing.exists():
                if existing.filter(name__iexact=name).exists():
                    Error1 = 'La categoría ya está registrada.'
                if existing.filter(descripcion__iexact=descripcion).exists():
                    Error2 = 'La descripción ya existe.'
            else:
                form.save()
                form = categoria_Pf()
        else:
            if 'name' in form.errors:
                Error1 = 'La categoría ya está registrada.'
            if 'descripcion' in form.errors:
                Error2 = 'La descripción ya existe'
    else:
        form = categoria_Pf()
        
    return render(request, 'Admin_v/categorias.html', {"form": form,
                                                       "Error1" : Error1, "Error2" : Error2, 
                                                       'pro_carrito' : pro_carrito, 'catego' : catego})

def actualizar_categorias (request):
    if request.method == 'POST' and request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        columna = request.POST.get('columna')
        valor = request.POST.get('valor')
        id = request.POST.get('id')

        cat = categoria_pm.objects.get(id=id)
        setattr(cat, columna, valor)
        cat.save()

        return JsonResponse({'message': 'Datos actualizados correctamente'})
    else:
        return JsonResponse({'error': 'Error en la solicitud'}, status=400)

@login_required
def eliminar_categoria(request, categoria_id):
    categoria = get_object_or_404(categoria_pm, pk=categoria_id)
    categoria.delete()
    return redirect('Admin_v/categorias')

@login_required
def productos(request):
    ids_remo = [30,31]
    bd_pro = producto_pm.objects.exclude(id__in=ids_remo)
    bd_pro_a = producto_pm.objects.exclude(id__in=ids_remo)
    Error_P = None
    Error_PD = None
    
    #Para el carrito del header muestre que hay en el carrito
    try:
        carrito = Carrito.objects.get(usuario=request.user)
        pro_carrito = ProCarrito.objects.filter(carrito=carrito)
    except ObjectDoesNotExist:
        carrito = None
        pro_carrito = None


    if request.method == 'POST':
        form = producto_Pf(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data['name']
            descripcion = form.cleaned_data['descripcion']
            existe = producto_pm.objects.filter(Q(name__iexact=name) | Q(descripcion__iexact=descripcion))

            if existe.exists():
                if existe.filter(name__iexact=name).exists():
                    Error_P = "El producto ya esta registrado."
                    form = producto_Pf()
                elif existe.filter(descripcion__iexact=descripcion).exists():
                    Error_PD = "La descripcion es indentica a otra."
                    form = producto_Pf()
            else:
                form.save()
                return redirect('Admin_v/productos')
    else:
        form = producto_Pf()

    #Tabla
    paginator1 = Paginator (bd_pro, 12)
    page1 = request.GET.get('page1')

    try:
        bd_pro2 = paginator1.page(page1)
    except PageNotAnInteger:
        bd_pro2 = paginator1.page(1)
    except EmptyPage:
        bd_pro2 = paginator1.page(paginator1.num_pages)

    #Productos
    paginator = Paginator(bd_pro, 12)
    page = request.GET.get('page')

    try:
        bd_pro = paginator.page(page)
    except PageNotAnInteger:
        bd_pro = paginator.page(1)
    except EmptyPage:
        bd_pro = paginator.page(paginator.num_pages)

 
    if request.GET.get('search'):
        search_term = request.GET.get('search')
        bd_pro_a = bd_pro_a.filter(name__icontains=search_term)
        filtered_products = list(bd_pro_a.values('name', 'id'))
        return JsonResponse({'filtered_products': filtered_products})

    return render(request, 'Admin_v/productos.html', {'form': form,
                                                     'bd_pro': bd_pro,
                                                     'bd_pro2' : bd_pro2,
                                                     'Error_P' : Error_P,
                                                     'Error_PD' : Error_PD,
                                                     'pro_carrito' : pro_carrito})
@login_required
def vertodos_productos (request, productos_id):
    pro = get_object_or_404(producto_pm, pk=productos_id)
    coments_p = coment_pro.objects.filter(productos=pro)

    try:
        carrito = Carrito.objects.get(usuario=request.user)
        pro_carrito = ProCarrito.objects.filter(carrito=carrito)
    except ObjectDoesNotExist:
        carrito = None
        pro_carrito = None

    
    if request.method == 'POST':
        comentario = request.POST.get ('comentario')
        user_id = request.POST.get ('user')

        userr = User.objects.get(pk=user_id)

        if comentario and userr:
            nuevo_comentario = coment_pro(
                productos = pro,
                user = userr,
                fecha = timezone.now(),
                comentario = comentario
            )
            nuevo_comentario.save()
    
    coment_pro_s = []
    for comment in coments_p:
        comments = coment_user.objects.filter(coment_proo_id = comment.id)
        coment_pro_s.append(comments)

    for like_dislike in coments_p:
        like = coment_user.objects.filter(coment_proo_id=like_dislike.id, tipo='LIKE').count()
        dislike = coment_user.objects.filter(coment_proo_id=like_dislike.id, tipo='DISLIKE').count()

        like_dislike.like = like
        like_dislike.dislike = dislike

    coment_totP = coment_pro.objects.exclude(comentario__isnull=True).exclude(comentario__exact='').filter(productos_id=productos_id).count()
    coment_totP += coment_user.objects.exclude(comentario__isnull=True).exclude(comentario__exact='').filter(coment_proo_id__in=coments_p.values_list('id', flat=True)).count()
    
    paginador = Paginator(coments_p, 8)
    page = request.GET.get('page')

    try:
        coments_p = paginador.page(page)
    except PageNotAnInteger:
        coments_p = paginador.page(1)
    except EmptyPage:
        coments_p = paginador.page(paginador.num_pages)


    return render (request, 'Admin_v/ver_productos.html', {'pro' : pro, 'coments_p' : coments_p,
                                                           'coment_pro_s' : coment_pro_s,
                                                           'coment_totP' : coment_totP, 
                                                           'pro_carrito' : pro_carrito})

def comnetPro_S(request):

    if request.method == 'POST':
        id_coment = request.POST.get('comentario_id')
        tipo = request.POST.get('tipo')
        texto_comentario = request.POST.get('texto_comentario')
        producto_id = request.POST.get('producto_id')

        if tipo == 'LIKE' or tipo == 'DISLIKE':
            exist_like = coment_user.objects.filter(
                user_id=request.user.id,
                coment_proo_id=id_coment,
                tipo='LIKE'
            ).exists()

            exist_dislike = coment_user.objects.filter(
                user_id=request.user.id,
                coment_proo_id=id_coment,
                tipo='DISLIKE'
            ).exists()

            if exist_like:
                like_delete = coment_user.objects.filter(user_id=request.user.id, tipo='LIKE', coment_proo_id=id_coment)
                like_delete.delete()
            elif exist_dislike:
                dislike_delete = coment_user.objects.filter(user_id=request.user.id, tipo='DISLIKE', coment_proo_id=id_coment)
                dislike_delete.delete()

            comentario_s = coment_user.objects.create(
                user_id=request.user.id,
                coment_proo_id=id_coment,
                tipo=tipo
            )
            comentario_s.save()

        elif tipo == 'COMENTARIO':
            comentario_s = coment_user.objects.create(
                user_id=request.user.id, 
                coment_proo_id=id_coment,
                tipo=tipo,
                comentario=texto_comentario
            )
            comentario_s.save()

    return redirect(f'/Admin_v/ver_productos.html/{producto_id}/')

@login_required
def eliminar_comentP (request, coments_id, pro_id):
    eliminar_c = get_object_or_404 (coment_pro, pk=coments_id)
    eliminar_c.delete()

    return redirect (f'/Admin_v/ver_productos.html/{pro_id}/')

@login_required
def editar_producto(request, producto_id):
    pro = get_object_or_404(producto_pm, pk=producto_id)

    if request.method == 'POST':
        form = producto_Pf(request.POST, request.FILES, instance=pro)
        if form.is_valid():
            form.save()
            return redirect('Admin_v/productos') 
    else:
        form = producto_Pf(instance=pro)
 
    return render(request, 'Admin_v/editar_producto.html', {'form': form, 'pro': pro})

@login_required
def eliminar_producto(request, producto_id):
    producto = get_object_or_404(producto_pm, pk=producto_id)
    producto.delete()
    return redirect('Admin_v/productos')


def agregar_al_carrito(request):
    if request.method == 'POST' and request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        producto_id = request.POST.get('producto_id')
        cantidad = int(request.POST.get('cantidad', 1))  

        cantidad = 1 if producto_id in ['30', '31'] else int(request.POST.get('cantidad', 1))

        producto = get_object_or_404(producto_pm, id=producto_id)

        carrito, created = Carrito.objects.get_or_create(usuario=request.user)

        # Verificar si el producto ya está en el carrito del usuario
        producto_en_carrito, created = ProCarrito.objects.get_or_create(
            carrito=carrito,
            producto=producto,
            defaults={'cantidad': cantidad}  # Si es la primera vez, se crea con la cantidad especificada
        )

        if not created:
            if producto_id in ['30', '31']:
                ProCarrito.objects.filter(
                    carrito=carrito,
                    producto=producto,
                ).update(cantidad=1)
            else:
                producto_en_carrito.cantidad += cantidad  # Incrementar la cantidad si ya está en el carrito
                producto_en_carrito.save()
        return JsonResponse({'message': 'Éxito'})
    else:
        return JsonResponse({'error': 'Solicitud no válida'}, status=400)

def actualizar_cantidad(request, producto_id):
    if request.method == 'POST' and request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        cantidad = int(request.POST.get('cantidad', 0))
        pro_carrito = get_object_or_404(ProCarrito, id=producto_id)
        
        # Actualizar la cantidad del producto en el carrito
        pro_carrito.cantidad = cantidad
        pro_carrito.save()
        
        return JsonResponse({'message': 'Cantidad actualizada correctamente'})
    else:
        return JsonResponse({'error': 'Solicitud no válida'}, status=400)

def eliminar_del_carrito(request, producto_id):
    if request.method == 'POST' and request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        pro_carrito = get_object_or_404(ProCarrito, id=producto_id)
        
        # Eliminar el producto del carrito
        pro_carrito.delete()
        
        return JsonResponse({'message': 'Producto eliminado correctamente'})
    else:
        return JsonResponse({'error': 'Solicitud no válida'}, status=400)

@login_required
def carrito(request):
    try:
        carrito = Carrito.objects.get(usuario=request.user)
        pro_carrito = ProCarrito.objects.filter(carrito=carrito)
        
        if request.method == 'POST' and request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            cod_cupon = request.POST.get('cod_cupon')
            cupon_bd = get_object_or_404(cupones, Q(codigo__iexact=cod_cupon))
            
            descuento = cupon_bd.descuento
            limite = cupon_bd.limite
            usado = cupon_bd.usado
            fecha_f = cupon_bd.fecha_f

            return JsonResponse({'existe' : True, 'descuento' : descuento, 
                                'usado' : usado, 'limite' : limite, 'fecha_f' : fecha_f})
        
        return render(request, 'Admin_v/carrito.html', {'pro_carrito': pro_carrito})

    except ObjectDoesNotExist:

        return render(request, 'Admin_v/carrito.html')

def updatelimit_cupon(request):
    if request.method == 'POST' and request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        try:
            #Actualizar el uso del cupon
            cod_cupon = request.POST.get('cod_cupon')
            cupon_bd = get_object_or_404(cupones, Q(codigo__iexact=cod_cupon))

            #Actualizar el total final del usuario
            usuario = request.POST.get('usuario')
            carro = get_object_or_404(Carrito, usuario_id=usuario)
            total_final = request.POST.get('total')

            #Actualizacion del Cupon
            cupon_bd.usado += 1
            cupon_bd.save()     

            #Actualizacion del Total
            carro.total = total_final
            carro.save()   

            return JsonResponse({"success": "Valor actualizado"}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Bad request"}, status=400)


def car_sindes_val (request):
    if request.method == 'POST' and request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        try:
            usuario = request.POST.get('usuario')
            carro = get_object_or_404(Carrito, usuario_id=usuario)
            total_final = request.POST.get('total')

            carro.total = total_final
            carro.save()
            return JsonResponse({"success": "Exito"}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Bad request"}, status=400)


@login_required
def cupon(request):
    bd_cupon = cupones.objects.all()

    #Para mostrar los productos en el header
    try:
        carrito = Carrito.objects.get(usuario=request.user)
        pro_carrito = ProCarrito.objects.filter(carrito=carrito)
    except ObjectDoesNotExist:
        carrito = None
        pro_carrito = None


    if request.method == 'POST':
        form = cuponn(request.POST)
        if form.is_valid():
            form.save()
            return redirect ('Admin_v/cupon')
    else:
        form = cuponn()

    return render(request, 'Admin_v/cupon.html', {'form': form, 'bd_cupon': bd_cupon, 
                                                  'pro_carrito' : pro_carrito})

def actualizar_cupones (request):
    if request.method == 'POST' and request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        columna = request.POST.get('columna')
        valor = request.POST.get('valor')
        id = request.POST.get('id')

        # Obtener el objeto correspondiente y actualizar el campo
        cup = cupones.objects.get(id=id)
        setattr(cup, columna, valor)
        cup.save()

        return JsonResponse({'message': 'Datos actualizados correctamente'})
    else:
        return JsonResponse({'error': 'Error en la solicitud'}, status=400)
    
@login_required
def eliminar_cupon(request, cupon_id):
    cupon = get_object_or_404(cupones, pk=cupon_id)
    cupon.delete()
    return redirect('Admin_v/cupon')

@login_required
def recetas(request):
    bd_recetas = recets.objects.all()
    bd_recetasS = recets.objects.all()
    unico_catego = recets.objects.values('categoria').annotate(total=Count('categoria'))
    error = None

    #Mostrar los pructos en el heasder
    try:
        carrito = Carrito.objects.get(usuario=request.user)
        pro_carrito = ProCarrito.objects.filter(carrito=carrito)
    except ObjectDoesNotExist:
        carrito = None
        pro_carrito = None


    #paginador de la tabla
    page = request.GET.get('page')
    paginator = Paginator(bd_recetas, 6)

    try:
        bd_recetas = paginator.page(page)
    except PageNotAnInteger:
        bd_recetas = paginator.page(1)
    except EmptyPage:
        bd_recetas = paginator.page(paginator.num_pages)

    #paginador de las recetas
    page1 = request.GET.get('page1')
    paginator1 = Paginator(bd_recetasS, 6)

    try:
        bd_recetas2 = paginator1.page(page1)
    except PageNotAnInteger:
        bd_recetas2 = paginator1.page(1)
    except EmptyPage:
        bd_recetas2 = paginator1.page(paginator1.num_pages)

    if request.method == 'POST':
        form = recetass(request.POST, request.FILES)

        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            catego = form.cleaned_data['categoria']
            cat_si = form.cleaned_data['cat_si']
            opcion = form.cleaned_data['tipo']
            video_file = request.FILES.get('video')

            if cat_si != '':
                catego = cat_si
            else:
                catego = catego
            

            if opcion == 'Video':
                if video_file is not None:
                    if not recets.objects.filter(nombre__iexact=nombre).exists():
                        recetaa = form.save(commit=False)
                        recetaa.tipo = form.cleaned_data['tipo']
                        recetaa.categoria = catego
                        if video_file:
                            recetaa.videoo = video_file
                        recetaa.save()
                        return redirect ('Admin_v/recetas')
                    else:
                        error = "El nombre ya esta registrado"
                        return render(request, 'Admin_v/recetas.html', {'form': recetass(), 'bd_recetas': bd_recetas, 
                                                        'bd_recetas2' : bd_recetas2,'error' : error,
                                                        'unico_catego' : unico_catego, 
                                                        'pro_carrito' : pro_carrito})
                else:
                    error = "El campo de video esta vacio"
                    return render(request, 'Admin_v/recetas.html', {'form': recetass(), 'bd_recetas': bd_recetas, 
                                                        'bd_recetas2' : bd_recetas2,
                                                        'unico_catego' : unico_catego, 
                                                        'pro_carrito' : pro_carrito, 'error2' : error})
            else:
                ingre = form.cleaned_data['ingre']
                proce = form.cleaned_data['proce']
                if ingre == "" or proce == "":
                    error = "Llene los campos faltantes de la opcion Escrita"
                    return render(request, 'Admin_v/recetas.html', {'form': recetass(), 'bd_recetas': bd_recetas, 
                                                        'bd_recetas2' : bd_recetas2,
                                                            'unico_catego' : unico_catego, 
                                                            'pro_carrito' : pro_carrito, 'error3' : error})
                else:
                    if not recets.objects.filter(nombre__iexact=nombre).exists():
                        recetaa = form.save(commit=False)
                        recetaa.tipo = form.cleaned_data['tipo']
                        recetaa.categoria = catego
                        if video_file:
                            recetaa.videoo = video_file
                        recetaa.save()
                        return redirect ('Admin_v/recetas')
                    else:
                        error = "El nombre ya esta registrado"
                        return render(request, 'Admin_v/recetas.html', {'form': recetass(), 'bd_recetas': bd_recetas, 
                                                        'bd_recetas2' : bd_recetas2,'error' : error,
                                                        'unico_catego' : unico_catego, 
                                                        'pro_carrito' : pro_carrito})
                
    else:
        form = recetass()
    
    if request.GET.get('search_R'):
        search_term = request.GET.get('search_R')
        bd_recetasS = bd_recetasS.filter(nombre__icontains=search_term)
        filtrado = list(bd_recetasS.values('nombre', 'id'))
        return JsonResponse({'filtrado': filtrado})
    
    return render(request, 'Admin_v/recetas.html', {'form': form, 'bd_recetas': bd_recetas, 
                                                   'bd_recetas2' : bd_recetas2,'error' : error,
                                                   'unico_catego' : unico_catego, 
                                                   'pro_carrito' : pro_carrito})

@login_required
def filtrar_recetas(request):
    slect_ca = request.GET.get('categoria')

    if slect_ca:
        rec_fil = recets.objects.filter(categoria=slect_ca)
        data = [{
        'nombre': rec.nombre,
        'imagen': rec.imagen.url,
        'categoria': rec.categoria,
        'id' : rec.id
        } for rec in rec_fil]

        return JsonResponse({'recetas': data}) 
    
    return JsonResponse({'error': 'No se proporcionó una categoría válida'})

@login_required
def editar_recetas(request, receta_id):
    recetas = get_object_or_404(recets, pk=receta_id)

    #Muestra los productos del header
    try:
        carrito = Carrito.objects.get(usuario=request.user)
        pro_carrito = ProCarrito.objects.filter(carrito=carrito)
    except ObjectDoesNotExist:
        carrito = None
        pro_carrito = None

    if request.method == 'POST':
        form = recetass(request.POST, request.FILES, instance=recetas)
        if form.is_valid():
            video_file = request.FILES.get('video')

            recetaa = form.save(commit=False)
            if video_file:
                    recetaa.videoo = video_file
            recetaa.save()
            return redirect ('Admin_v/recetas') 
    else:
        form = recetass(instance=recetas)
 
    return render(request, 'Admin_v/editar_recetas.html', {'form': form, 'recetas' : recetas, 
                                                           'pro_carrito' : pro_carrito})

def get_random_recipes(all_recetas, receta_actual):
    recetas_disponibles = [rec for rec in all_recetas if rec.nombre != receta_actual.nombre]
    recetas_arriba = sample(recetas_disponibles, 2)
    recetas_abajo = sample([rec for rec in recetas_disponibles if rec not in recetas_arriba], 3)
    return recetas_arriba, recetas_abajo

def ver_receta (request, receta_id):
    recetas = get_object_or_404(recets, pk=receta_id)
    all_recetas = recets.objects.all()

    #Muestra los productos del header
    try:
        carrito = Carrito.objects.get(usuario=request.user)
        pro_carrito = ProCarrito.objects.filter(carrito=carrito)
    except ObjectDoesNotExist:
        carrito = None
        pro_carrito = None

    
    #Puntos de ingredientes
    ingre_n = recetas.ingre.splitlines()
    #numeracion de procedimiento
    proce = recetas.proce.splitlines()
    proce_n = enumerate(proce, start=1)

    numeracion = {
        'proce_n' : proce_n, 
        'ingre_n' : ingre_n
    }

    primera, segunda = get_random_recipes(all_recetas, recetas)

    return render (request, 'Admin_v/ver_receta.html' , {'recetas' : recetas, 'numeracion' : numeracion,
                                                         'primera' : primera,
                                                         'segunda' : segunda, 'pro_carrito' : pro_carrito})

@login_required
def eliminar_receta(request, receta_id):
    recetas = get_object_or_404 (recets, pk=receta_id)
    recetas.delete()
    return redirect ('Admin_v/recetas')

@login_required
def bitacora (request):
    bd_bitacora = bitacors.objects.all().order_by('-fecha')
    bitacora_com = bitacors.objects.all()
    
    #Muestra los productos del header
    try:
        carrito = Carrito.objects.get(usuario=request.user)
        pro_carrito = ProCarrito.objects.filter(carrito=carrito)
    except ObjectDoesNotExist:
        carrito = None
        pro_carrito = None


    #Paginador de la tabla
    page = request.GET.get('page')
    paginator = Paginator(bd_bitacora, 7)

    try:
        bd_bitacora = paginator.page(page)
    except PageNotAnInteger:
        bd_bitacora = paginator.page(1)
    except EmptyPage:
        bd_bitacora = paginator.page(paginator.num_pages)

    #Paginador de los comentarios
    page1 = request.GET.get('page1')
    paginator1 = Paginator(bitacora_com, 10)

    try:
        bitacora_com = paginator.page(page1)
    except PageNotAnInteger:
        bitacora_com = paginator.page(1)
    except EmptyPage:
        bitacora_com = paginator.page(paginator1.num_pages)

    if request.method == 'POST':
        form = bitacora_D (request.POST)
        if form.is_valid():
            bitacoras = form.save(commit=False)
            bitacoras.nombre = form.cleaned_data['nombre']
            bitacoras.save()
            return redirect ('Admin_v/bitacora')
    else:
        form = bitacora_D()

    interacciones = Interaccion.objects.filter(bitacor__in=bitacora_com)

    for comentario in bitacora_com:
        like = Interaccion.objects.filter(bitacor_id=comentario.id, tipo='LIKE').count()
        dislike = Interaccion.objects.filter(bitacor_id=comentario.id, tipo='DISLIKE').count()

        comentario.like = like
        comentario.dislike = dislike
    
    
    comentarios_tot = bitacors.objects.exclude(comentario__isnull=True).exclude(comentario__exact='').count()
    comentarios_tot += Interaccion.objects.exclude(comentarios__isnull=True).exclude(comentarios__exact='').count()

    return render (request, 'Admin_v/bitacora.html', {'form' : form, 'bd_bitacora' : bd_bitacora,
                                                      'interacciones' : interacciones, 
                                                      'bitacora_com' : bitacora_com,
                                                      'comentarios_tot' : comentarios_tot,
                                                      'pro_carrito' : pro_carrito})

def interaccion(request):
    if request.method == 'POST':
        bitacora_id = request.POST.get('bitacora_id')
        tipo = request.POST.get('tipo')
        texto_comentario = request.POST.get('texto_comentario')

        if tipo == 'LIKE' or tipo == 'DISLIKE':
            # Verificar si el usuario ya ha interactuado con esta publicación
            exist_like = Interaccion.objects.filter(
                usuario=request.user,
                bitacor_id=bitacora_id,
                tipo='LIKE'
            ).exists()

            exist_dislike = Interaccion.objects.filter(
                usuario=request.user,
                bitacor_id=bitacora_id,
                tipo='DISLIKE'
            ).exists()

            # Eliminar la interacción existente si ya existe para el tipo actual
            if exist_like:
                like_delete = Interaccion.objects.filter(usuario=request.user, tipo='LIKE', bitacor_id=bitacora_id)
                like_delete.delete()
            elif exist_dislike:
                dislike_delete = Interaccion.objects.filter(usuario=request.user, tipo='DISLIKE', bitacor_id=bitacora_id)
                dislike_delete.delete()

            interaccion = Interaccion.objects.create(
                usuario=request.user,
                bitacor_id=bitacora_id,
                tipo=tipo
            )
            interaccion.save()

        elif tipo == 'COMENTARIO':
            interaccion = Interaccion.objects.create(
                usuario=request.user, 
                bitacor_id=bitacora_id,
                tipo=tipo,
                comentarios=texto_comentario
            )
            interaccion.save()

    return redirect('Admin_v/bitacora')

def eliminar_bitacora (request, bitacora_id):
    bd_bita = get_object_or_404 (bitacors, pk=bitacora_id)
    bd_bita.delete()
    return redirect ('Admin_v/bitacora')

@login_required
def tracking (request):
    carrito = Carrito.objects.get(usuario=request.user)
    pro_carrito = ProCarrito.objects.filter(carrito=carrito)

    if request.method == 'POST':
        form = traking_datos(request.POST)

        if form.is_valid():
            usuario_id = request.user.id
            carrito = Carrito.objects.filter(usuario_id=usuario_id).first()
            
            totales, created = Totales.objects.get_or_create(user_id=usuario_id)
            totales.total = carrito.total
            totales.save()

            guardado = request.POST.get ('guardar_n')
            opciones = request.POST.get ('opcion')

            if opciones == 'Si':
                guardar = form.save(commit=False)
                guardar.usuario_id = request.user.id
                guardar.latitud = request.POST.get ('latitud')
                guardar.longitud = request.POST.get ('longitud')
                guardar.email = request.POST.get ('email')
                tipo = request.POST.get ('pago')
                
                if tipo == 'tarjeta':
                    guardar.pago = tipo
                    guardar.tarjeta = request.POST.get ('nt')
                    guardar.mesaño = request.POST.get ('ma')
                    guardar.segu = request.POST.get ('cds')
                    guardar.titular = request.POST.get ('name')            

                elif tipo == 'efectivo':
                    guardar.pago = tipo

                if not datos_envio.objects.filter(guardado__iexact=guardado).exists():
                    guardar.guardado = guardado                    
                    guardar.save()

                    eliminar_carro = get_object_or_404 (Carrito, usuario_id=request.user.id)
                    eliminar_carro.delete()
                    return redirect(f'/Admin_v/final_pedido.html/{guardar.id}/')
                
                else:
                    Error = 'El nombre de guardado ya existe'
                    
                    return render (request, 'Admin_v/tracking.html', 
                                   {'form': traking_datos(), 'pro_carrito' : pro_carrito, 'Error' : Error})
                
            elif opciones == 'No':
                request.session['latitud'] = request.POST.get('latitud')
                request.session['longitud'] = request.POST.get ('longitud')

                return redirect('Admin_v/final_pedidoDont')
            else:
                ide = request.POST.get ('id')
                id_dato = datos_envio.objects.filter(id=ide).first()

                eliminar_carro = get_object_or_404 (Carrito, usuario_id=request.user.id)
                eliminar_carro.delete()

                return redirect(f'/Admin_v/final_pedido.html/{id_dato.id}/')
    else:
        form = traking_datos()

    return render (request, 'Admin_v/tracking.html', {'form': form, 'pro_carrito' : pro_carrito})

def obtener_envios (request):
    slecci = request.GET.get('slecci')

    if slecci:
        datos_lleno = datos_envio.objects.filter(guardado=slecci)
        lista_relleno = [] 

        for datass in datos_lleno:
            data_relle = {
                'cel': datass.cel,
                'ciudad': datass.ciudad,
                'prov': datass.provincia,
                'lati': datass.latitud,
                'longi': datass.longitud,
                'mesaño': datass.mesaño,
                'segu': datass.segu,
                'tarjeta': datass.tarjeta,
                'titular': datass.titular,
                'barrio': datass.barrio,
                'cedula': datass.cedula,
                'pago' : datass.pago,
                'id' : datass.id
            }
            lista_relleno.append(data_relle)

        return JsonResponse(lista_relleno, safe=False)
    
    else:
        datos = datos_envio.objects.filter(usuario_id=request.user.id)
        lista_envio = []

        for data in datos:
            data_envio = {
                'save': data.guardado
            }
            lista_envio.append(data_envio)

        return JsonResponse(lista_envio, safe=False)


@login_required
def final_pedido(request, id_envio):
    total = Totales.objects.filter(user_id=request.user.id)
    valor_envio = datos_envio.objects.filter(id=id_envio)

    return render (request, 'Admin_v/final_pedido.html', {'total' : total, 'valor_envio' : valor_envio})

@login_required
def final_pedido_dontsave (request):
    total = Totales.objects.filter(user_id=request.user.id)
    long = request.session.get ('longitud')
    lati = request.session.get ('latitud')

    eliminar = get_object_or_404 (Carrito, usuario_id=request.user.id)
    eliminar.delete()

    return render (request, 'Admin_v/final_pedido.html', {'total' : total, 'long' : long, 'lati':lati})

def delete_total (request):
    eliminar = get_object_or_404 (Totales, user_id=request.user.id)
    eliminar.delete()

    return JsonResponse ("Exito", safe=False)









#Vistas de Usuario Estandar
@login_required
def menu_u (request):
    ids_remo = [30,31]
    bd_productos = producto_pm.objects.exclude(id__in=ids_remo)
    bd_recetas = recets.objects.all()

    promo = producto_pm.objects.filter(id__in=ids_remo)

    img_promos = [
        'imagenes/menu_ae/promo1.png',
        'imagenes/menu_ae/promo2.png'
    ]
    
    try:
        carrito = Carrito.objects.get(usuario=request.user)
        pro_carrito = ProCarrito.objects.filter(carrito=carrito)
    except ObjectDoesNotExist:
        carrito = None
        pro_carrito = None
    
    
    if request.GET.get('search_P'):
        search_term = request.GET.get('search_P')
        bd_pro = bd_productos.filter(name__icontains=search_term)
        filtrado = list(bd_pro.values('name', 'id'))
        return JsonResponse({'filtrado': filtrado})
    
    return render(request, 'User_v/menu.html', {'bd_productos' : bd_productos,
                                                 'bd_recetas' : bd_recetas, 
                                                 'pro_carrito' : pro_carrito, 
                                                 'promo' : promo, 'img_promos' : img_promos})

def productos_u (request):
    bd_catego = categoria_pm.objects.values('name').distinct()
    
    ids_remo = [30,31]
    bd_pro = producto_pm.objects.exclude(id__in=ids_remo)
    bd_pro_s = producto_pm.objects.all()
    
    try:
        carrito = Carrito.objects.get(usuario=request.user)
        pro_carrito = ProCarrito.objects.filter(carrito=carrito)
    except ObjectDoesNotExist:
        carrito = None
        pro_carrito = None

    #Productos
    paginator = Paginator(bd_pro, 12)
    page = request.GET.get('page')

    try:
        bd_pro = paginator.page(page)
    except PageNotAnInteger:
        bd_pro = paginator.page(1)
    except EmptyPage:
        bd_pro = paginator.page(paginator.num_pages)

 
    if request.GET.get('search'):
        search_term = request.GET.get('search')
        bd_pro_s = bd_pro_s.filter(name__icontains=search_term)
        filtered_products = list(bd_pro_s.values('name', 'id'))
        return JsonResponse({'filtered_products': filtered_products})

    return render(request, 'User_v/productos.html', {'bd_catego': bd_catego,
                                                     'bd_pro': bd_pro,
                                                     'pro_carrito' : pro_carrito})

@login_required
def vertodos_productos_u (request, productos_id):
    pro = get_object_or_404(producto_pm, pk=productos_id)
    coments_p = coment_pro.objects.filter(productos=pro)

    try:
        carrito = Carrito.objects.get(usuario=request.user)
        pro_carrito = ProCarrito.objects.filter(carrito=carrito)
    except ObjectDoesNotExist:
        carrito = None
        pro_carrito = None

    
    if request.method == 'POST':
        comentario = request.POST.get ('comentario')
        user_id = request.POST.get ('user')

        userr = User.objects.get(pk=user_id)

        if comentario and userr:
            nuevo_comentario = coment_pro(
                productos = pro,
                user = userr,
                fecha = timezone.now(),
                comentario = comentario
            )
            nuevo_comentario.save()
    
    coment_pro_s = []
    for comment in coments_p:
        comments = coment_user.objects.filter(coment_proo_id = comment.id)
        coment_pro_s.append(comments)

    for like_dislike in coments_p:
        like = coment_user.objects.filter(coment_proo_id=like_dislike.id, tipo='LIKE').count()
        dislike = coment_user.objects.filter(coment_proo_id=like_dislike.id, tipo='DISLIKE').count()

        like_dislike.like = like
        like_dislike.dislike = dislike

    coment_totP = coment_pro.objects.exclude(comentario__isnull=True).exclude(comentario__exact='').filter(productos_id=productos_id).count()
    coment_totP += coment_user.objects.exclude(comentario__isnull=True).exclude(comentario__exact='').filter(coment_proo_id__in=coments_p.values_list('id', flat=True)).count()
    
    paginador = Paginator(coments_p, 8)
    page = request.GET.get('page')

    try:
        coments_p = paginador.page(page)
    except PageNotAnInteger:
        coments_p = paginador.page(1)
    except EmptyPage:
        coments_p = paginador.page(paginador.num_pages)


    return render (request, 'User_v/ver_productos.html', {'pro' : pro, 'coments_p' : coments_p,
                                                           'coment_pro_s' : coment_pro_s,
                                                           'coment_totP' : coment_totP, 
                                                           'pro_carrito' : pro_carrito})

@login_required
def carrito_u(request):
    try:
        carrito = Carrito.objects.get(usuario=request.user)
        pro_carrito = ProCarrito.objects.filter(carrito=carrito)
        
        if request.method == 'POST' and request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            cod_cupon = request.POST.get('cod_cupon')
            cupon_bd = get_object_or_404(cupones, Q(codigo__iexact=cod_cupon))
            
            descuento = cupon_bd.descuento
            limite = cupon_bd.limite
            usado = cupon_bd.usado
            fecha_f = cupon_bd.fecha_f

            return JsonResponse({'existe' : True, 'descuento' : descuento, 
                                'usado' : usado, 'limite' : limite, 'fecha_f' : fecha_f})
        
        return render(request, 'User_v/carrito.html', {'pro_carrito': pro_carrito})

    except ObjectDoesNotExist:

        return render(request, 'User_v/carrito.html')


@login_required
def recetas_u(request):
    bd_recetas = recets.objects.all()
    bd_recetasS = recets.objects.all()
    unico_catego = recets.objects.values('categoria').annotate(total=Count('categoria'))

    try:
        carrito = Carrito.objects.get(usuario=request.user)
        pro_carrito = ProCarrito.objects.filter(carrito=carrito)
    except ObjectDoesNotExist:
        carrito = None
        pro_carrito = None


    #paginador de las recetas
    page1 = request.GET.get('page1')
    paginator1 = Paginator(bd_recetasS, 6)

    try:
        bd_recetas2 = paginator1.page(page1)
    except PageNotAnInteger:
        bd_recetas2 = paginator1.page(1)
    except EmptyPage:
        bd_recetas2 = paginator1.page(paginator1.num_pages)
                

    if request.GET.get('search_R'):
        search_term = request.GET.get('search_R')
        bd_recetasS = bd_recetasS.filter(nombre__icontains=search_term)
        filtrado = list(bd_recetasS.values('nombre', 'id'))
        return JsonResponse({'filtrado': filtrado})
    
    return render(request, 'User_v/recetas.html', {'bd_recetas': bd_recetas, 
                                                   'bd_recetas2' : bd_recetas2,
                                                   'unico_catego' : unico_catego, 
                                                   'pro_carrito' : pro_carrito})

def ver_receta_u (request, receta_id):
    recetas = get_object_or_404(recets, pk=receta_id)
    all_recetas = recets.objects.all()

    try:
        carrito = Carrito.objects.get(usuario=request.user)
        pro_carrito = ProCarrito.objects.filter(carrito=carrito)
    except ObjectDoesNotExist:
        carrito = None
        pro_carrito = None

    
    #Puntos de ingredientes
    ingre_n = recetas.ingre.splitlines()
    #numeracion de procedimiento
    proce = recetas.proce.splitlines()
    proce_n = enumerate(proce, start=1)

    numeracion = {
        'proce_n' : proce_n, 
        'ingre_n' : ingre_n
    }

    primera, segunda = get_random_recipes(all_recetas, recetas)

    return render (request, 'User_v/ver_receta.html' , {'recetas' : recetas, 'numeracion' : numeracion,
                                                         'primera' : primera,
                                                         'segunda' : segunda, 'pro_carrito' : pro_carrito})

@login_required
def bitacora_u (request):
    bitacora_com = bitacors.objects.all().order_by('-fecha')
    
    try:
        carrito = Carrito.objects.get(usuario=request.user)
        pro_carrito = ProCarrito.objects.filter(carrito=carrito)
    except ObjectDoesNotExist:
        carrito = None
        pro_carrito = None


    page1 = request.GET.get('page1')
    paginator = Paginator(bitacora_com, 10)

    try:
        bitacora_com = paginator.page(page1)
    except PageNotAnInteger:
        bitacora_com = paginator.page(1)
    except EmptyPage:
        bitacora_com = paginator.page(paginator.num_pages)


    interacciones = Interaccion.objects.filter(bitacor__in=bitacora_com)

    for comentario in bitacora_com:
        like = Interaccion.objects.filter(bitacor_id=comentario.id, tipo='LIKE').count()
        dislike = Interaccion.objects.filter(bitacor_id=comentario.id, tipo='DISLIKE').count()

        comentario.like = like
        comentario.dislike = dislike
    
    
    comentarios_tot = bitacors.objects.exclude(comentario__isnull=True).exclude(comentario__exact='').count()

    return render (request, 'User_v/bitacora.html', {
                                                      'interacciones' : interacciones, 
                                                      'bitacora_com' : bitacora_com,
                                                      'comentarios_tot' : comentarios_tot,
                                                      'pro_carrito' : pro_carrito})

def interaccion_u(request):
    if request.method == 'POST':
        bitacora_id = request.POST.get('bitacora_id')
        tipo = request.POST.get('tipo')
        texto_comentario = request.POST.get('texto_comentario')

        if tipo == 'LIKE' or tipo == 'DISLIKE':
            # Verificar si el usuario ya ha interactuado con esta publicación
            exist_like = Interaccion.objects.filter(
                usuario=request.user,
                bitacor_id=bitacora_id,
                tipo='LIKE'
            ).exists()

            exist_dislike = Interaccion.objects.filter(
                usuario=request.user,
                bitacor_id=bitacora_id,
                tipo='DISLIKE'
            ).exists()

            # Eliminar la interacción existente si ya existe para el tipo actual
            if exist_like:
                like_delete = Interaccion.objects.filter(usuario=request.user, tipo='LIKE', bitacor_id=bitacora_id)
                like_delete.delete()
            elif exist_dislike:
                dislike_delete = Interaccion.objects.filter(usuario=request.user, tipo='DISLIKE', bitacor_id=bitacora_id)
                dislike_delete.delete()

            interaccion = Interaccion.objects.create(
                usuario=request.user,
                bitacor_id=bitacora_id,
                tipo=tipo
            )
            interaccion.save()

        elif tipo == 'COMENTARIO':
            interaccion = Interaccion.objects.create(
                usuario=request.user, 
                bitacor_id=bitacora_id,
                tipo=tipo,
                comentarios=texto_comentario
            )
            interaccion.save()

    return redirect('User_v/bitacora')

@login_required
def tracking_u (request):
    carrito = Carrito.objects.get(usuario=request.user)
    pro_carrito = ProCarrito.objects.filter(carrito=carrito)

    if request.method == 'POST':
        form = traking_datos(request.POST)

        if form.is_valid():
            usuario_id = request.user.id
            carrito = Carrito.objects.filter(usuario_id=usuario_id).first()
            
            totales, created = Totales.objects.get_or_create(user_id=usuario_id)
            totales.total = carrito.total
            totales.save()

            guardado = request.POST.get ('guardar_n')
            opciones = request.POST.get ('opcion')

            if opciones == 'Si':
                guardar = form.save(commit=False)
                guardar.usuario_id = request.user.id
                guardar.latitud = request.POST.get ('latitud')
                guardar.longitud = request.POST.get ('longitud')
                guardar.email = request.POST.get ('email')
                tipo = request.POST.get ('pago')
                
                if tipo == 'tarjeta':
                    guardar.pago = tipo
                    guardar.tarjeta = request.POST.get ('nt')
                    guardar.mesaño = request.POST.get ('ma')
                    guardar.segu = request.POST.get ('cds')
                    guardar.titular = request.POST.get ('name')            

                elif tipo == 'efectivo':
                    guardar.pago = tipo

                if not datos_envio.objects.filter(guardado__iexact=guardado).exists():
                    guardar.guardado = guardado                    
                    guardar.save()

                    eliminar_carro = get_object_or_404 (Carrito, usuario_id=request.user.id)
                    eliminar_carro.delete()
                    return redirect(f'/User_v/final_pedido.html/{guardar.id}/')
                
                else:
                    Error = 'El nombre de guardado ya existe'
                    
                    return render (request, 'User_v/tracking.html', 
                                   {'form': traking_datos(), 'pro_carrito' : pro_carrito, 'Error' : Error})
                
            elif opciones == 'No':
                request.session['latitud'] = request.POST.get('latitud')
                request.session['longitud'] = request.POST.get ('longitud')

                return redirect('User_v/final_pedidoDont')
            else:
                ide = request.POST.get ('id')
                id_dato = datos_envio.objects.filter(id=ide).first()

                eliminar_carro = get_object_or_404 (Carrito, usuario_id=request.user.id)
                eliminar_carro.delete()

                return redirect(f'/User_v/final_pedido.html/{id_dato.id}/')
    else:
        form = traking_datos()

    return render (request, 'User_v/tracking.html', {'form': form, 'pro_carrito' : pro_carrito})

def obtener_envios (request):
    slecci = request.GET.get('slecci')

    if slecci:
        datos_lleno = datos_envio.objects.filter(guardado=slecci)
        lista_relleno = [] 

        for datass in datos_lleno:
            data_relle = {
                'cel': datass.cel,
                'ciudad': datass.ciudad,
                'prov': datass.provincia,
                'lati': datass.latitud,
                'longi': datass.longitud,
                'mesaño': datass.mesaño,
                'segu': datass.segu,
                'tarjeta': datass.tarjeta,
                'titular': datass.titular,
                'barrio': datass.barrio,
                'cedula': datass.cedula,
                'pago' : datass.pago,
                'id' : datass.id
            }
            lista_relleno.append(data_relle)

        return JsonResponse(lista_relleno, safe=False)
    
    else:
        datos = datos_envio.objects.filter(usuario_id=request.user.id)
        lista_envio = []

        for data in datos:
            data_envio = {
                'save': data.guardado
            }
            lista_envio.append(data_envio)

        return JsonResponse(lista_envio, safe=False)


@login_required
def final_pedido_u(request, id_envio):
    total = Totales.objects.filter(user_id=request.user.id)
    valor_envio = datos_envio.objects.filter(id=id_envio)

    return render (request, 'User_v/final_pedido.html', {'total' : total, 'valor_envio' : valor_envio})

@login_required
def final_pedido_dontsave_u (request):
    total = Totales.objects.filter(user_id=request.user.id)
    long = request.session.get ('longitud')
    lati = request.session.get ('latitud')

    eliminar = get_object_or_404 (Carrito, usuario_id=request.user.id)
    eliminar.delete()

    return render (request, 'User_v/final_pedido.html', {'total' : total, 'long' : long, 'lati':lati})
