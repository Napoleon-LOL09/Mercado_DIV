from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

main_app = 'main'

urlpatterns = [
    path ('', views.register_login, name='base'),
    path('reset_password/', views.reset_password, name='reset_password'),
    path ('logout/', LogoutView.as_view(template_name='logout.html'), name='logout'), 
    path('new_password/<uidb64>/<token>/', views.new_password, name='new_password'),
    path('password_reset_complete/', views.password_reset_complete, name='password_reset_complete'),
    
    #Urls de Administrador:
    path ('Admin_v/menu.html', views.menu_a, name='Admin_v/menu'),
    path ('Admin_v/usuarios.html/', views.usuarios, name='Admin_v/usuarios'),
    path ('eliminar_registro/<int:registro_id>/', views.eliminar_usuario, name='eliminar_registro'),
    path ('Admin_v/categorias.html/', views.categoria, name='Admin_v/categorias'),
    path ('actualizar_categorias/', views.actualizar_categorias, name='actualizar_categorias'),
    path ('eliminar_categoria/<int:categoria_id>/', views.eliminar_categoria, name='eliminar_categoria'),
    path ('Admin_v/productos.html/', views.productos, name='Admin_v/productos'),
    path ('Admin_v/ver_productos.html/<int:productos_id>/', views.vertodos_productos, name='Admin_v/ver_productos'),
    path ('comnetPro_S/', views.comnetPro_S, name='comnetPro_S'),
    path ('eliminar_comentP/<int:coments_id>/<int:pro_id>/', views.eliminar_comentP, name='eliminar_comentP'),
    path ('Admin_v/editar_producto.html/<int:producto_id>/', views.editar_producto, name='Admin_v/editar_producto'),
    path ('eliminar_producto/<int:producto_id>/', views.eliminar_producto, name='eliminar_producto'),
    path ('agregar_al_carrito/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path ('Admin_v/carrito.html/', views.carrito, name='Admin_v/carrito' ),
    path ('updatelimit_cupon/', views.updatelimit_cupon, name='updatelimit_cupon'),
    path ('car_sindes_val/', views.car_sindes_val, name='car_sindes_val'),
    path ('actualizar_cantidad/<int:producto_id>/', views.actualizar_cantidad, name='actualizar_cantidad'),
    path ('eliminar_del_carrito/<int:producto_id>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
    path ('Admin_v/cupon.html/', views.cupon, name='Admin_v/cupon'),
    path ('actualizar_cupones/', views.actualizar_cupones, name='actualizar_cupones'),
    path ('eliminar_cupon/<int:cupon_id>', views.eliminar_cupon, name='eliminar_cupon'),
    path ('Admin_v/recetas.html/', views.recetas, name='Admin_v/recetas'),
    path ('filtrar_recetas/', views.filtrar_recetas, name='filtrar_recetas'),
    path ('Admin_v/ver_receta.html/<int:receta_id>/', views.ver_receta, name='Admin_v/ver_receta'),
    path ('Admin_v/editar_recetas.html/<int:receta_id>', views.editar_recetas, name='Admin_v/editar_recetas'),
    path ('eliminar_receta/<int:receta_id>/', views.eliminar_receta, name='eliminar_receta'),
    path ('Admin_v/bitacora.html/', views.bitacora, name='Admin_v/bitacora'),
    path ('interaccion/', views.interaccion, name='interaccion'),
    path ('eliminar_bitacora/<int:bitacora_id>/', views.eliminar_bitacora, name='eliminar_bitacora'),
    path ('Admin_v/tracking.html/', views.tracking, name='Admin_v/tracking'),
    path ('obtener_envios/', views.obtener_envios, name='obtener_envios'),
    path ('Admin_v/final_pedido.html/<int:id_envio>/', views.final_pedido, name='Admin_v/final_pedido'),
    path ('Admin_v/final_pedido.html/', views.final_pedido_dontsave, name='Admin_v/final_pedidoDont'),
    path ('delete_total/', views.delete_total, name='delete_total'),
    
    #Urls de Usuario Estandar:
    path ('User_v/menu.html/', views.menu_u, name='User_v/menu'),
    path ('User_v/productos.html/', views.productos_u, name='User_v/productos'),
    path ('User_v/ver_productos.html/<int:productos_id>/', views.vertodos_productos_u, name='User_v/ver_productos'),
    path ('User_v/carrito.html/', views.carrito_u, name='User_v/carrito'),
    path ('User_v/recetas.html/', views.recetas_u, name='User_v/recetas'),
    path ('User_v/ver_receta.html/<int:receta_id>/', views.ver_receta_u, name='User_v/ver_receta'),
    path ('User_v/bitacora.html/', views.bitacora_u, name='User_v/bitacora'),
    path ('interaccion_u/', views.interaccion_u, name='interaccion_u'),
    path ('User_v/tracking.html/', views.tracking_u, name='User_v/tracking'),
    path ('User_v/final_pedido.html/<int:id_envio>/', views.final_pedido_u, name='User_v/final_pedido'),
    path ('User_v/final_pedido.html/', views.final_pedido_dontsave_u, name='User_v/final_pedidoDont')

	]