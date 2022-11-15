#!/usr/bin/env python3.9

from kivy.core.window import Window
from kivy.lang.builder import Builder
from functools import partial
from kivy.properties import ObjectProperty, StringProperty, NumericProperty
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.uix.scatter import Scatter
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
import kivy
import random
import pycacho as pyc
kivy.require('1.0.7')

Builder.load_file('main.kv')

#from kivy.config import Config
# De momento estas funciones no causan algún efecto
#Config.set('graphics', 'resizable', '0')
#Config.set('graphics', 'width', '80')
#print(f'La pantalla mide {Window.size[0]}, {Window.size[1]}')


class Jugadores:
    def __init__(self):
        self.lista_jugadores = []
        self.jugadores_todos = {}
        self.jugada_actual = []
        self.index_jugador = 0
        self.ganador_total = ' '

    def nuevo_jugador(self, nuevo_jugador):
        self.lista_jugadores.append(nuevo_jugador)
    
    def limpiar_lista_jugadores(self):
        self.lista_jugadores = []

    def crear_jugadores(self):
        for jugador in self.lista_jugadores:
            self.jugadores_todos[str(jugador)] = pyc.Jugar(str(jugador))
        return (self.jugadores_todos)

    def cambiar_turno(self):
        if self.index_jugador < len(self.lista_jugadores) - 1:
            self.index_jugador += 1
        else:
            self.index_jugador = 0
        return (self.index_jugador)

    def devolver_nombre(self):
        self.nombre_jugador = self.lista_jugadores[self.index_jugador]
        return (self.nombre_jugador)

    def get_key(self):
        key_jugador = self.lista_jugadores[self.index_jugador]
        return (key_jugador)

    def lanzar(self):
        self.jugada = self.jugadores_todos[self.get_key()].lanzar()
        return (self.jugada[0])

    def ver_dormida(self):
        self.dormida = self.jugada[1]
        return(self.dormida)

    def ver_posibilidades(self):
        Posibilidades = self.jugadores_todos[self.get_key()].analizar()
        dict1 = Posibilidades[0]
        dict2 = Posibilidades[1]
        dict1.update(dict2)
        self.diccionarioRes = {k: v for k, v in sorted(
            dict1.items(), key=lambda item: item[1], reverse=True)}
        # cambiar este método a iteración de diccionario
        # El método debe debolver diccionarioRes
        self.lista_posibilidades = list(self.diccionarioRes.keys())[0:3]
        return (self.lista_posibilidades)

    def devolver_posibilidades(self):
        return (self.diccionarioRes)

    def anotar(self, string_eleccion):
        self.jugadores_todos[self.get_key()].anotar(string_eleccion)

    def actualizar_resultados(self):
        return (self.jugadores_todos[self.get_key()].actualizar_resultados())

    def borrar_posibilidad(self, key_casilla):
        self.jugadores_todos[self.get_key()].borrar(key_casilla)

    def check_estado_juego(self):
        return (self.jugadores_todos[self.get_key()].check_estado_juego())

    def cambiar_dados(self, lista_dados_cambiar):
        # Cambiar esta string por los dados adecuados
        self.jugadores_todos[self.get_key()].cambiar(lista_dados_cambiar)

    def volcar_dados(self, lista_dados_volcar):
        self.jugadores_todos[self.get_key()].volcar(lista_dados_volcar)

    def get_mano(self):
        return (self.jugadores_todos[self.get_key()].de_mano)

    def check_ganador(self):
        self.puntajes_todos_jugadores = {}
        self.juegos_completos = {}
        self.jugadores_ganadores = {}
        # Aplicar este método.
        self.juego_terminado = False
        self.nombre_jugador_ganador = ' '

        # Ver como checkear si todos los jugadores han ganado
        for jugador in self.jugadores_todos:
            self.juegos_completos[jugador] = self.jugadores_todos[jugador].check_estado_juego()[
                0]
            self.jugadores_ganadores[jugador] = self.jugadores_todos[jugador].check_estado_juego()[
                1]
            self.puntajes_todos_jugadores[jugador] = self.jugadores_todos[jugador].check_estado_juego()[
                2]
        for jugador in self.puntajes_todos_jugadores:
            # Puede que aquí esté el problema
            if all(x == True for x in self.juegos_completos.values()):
                # Revisar esta función
                self.juego_terminado = True
        self.puntajes_ordenados = {k: v for k, v in sorted(
            self.puntajes_todos_jugadores.items(), key=lambda item: item[1], reverse=True)}

        # Ahora sólo comprobamos el método del puntaje, no vemos las otras maneras de ganar
        for jugador in self.jugadores_ganadores:
            if self.jugadores_ganadores[jugador] == True:
                self.ganador_total = jugador
            else:
                self.ganador_total = next(iter(self.puntajes_ordenados))
        if all(x == True for x in self.juegos_completos.values()):
            self.juego_terminado = True
            print(f'El\n\n\n Ganador \n\n es: {self.ganador_total} \n\n')
        return (self.juego_terminado, self.ganador_total)


Jugadores_objeto = Jugadores()

## Variable globales

font_general = int(Window.size[0]/20)
font_small = int(Window.size[0]/30)
dado_size = int(Window.size[0]/6)

# Versión computadora
#alto = int(Window.size[0])
#ancho = int(Window.size[1])
#limite_abajo_dados = int(Window.size[0] - (Window.size[0]/4))
#limite_arriba_dados = int(Window.size[0]/4)

#Versión smartphone
alto = int(Window.size[1])
ancho = int(Window.size[0])
limite_abajo_dados = int(alto - (alto/3))
limite_arriba_dados = int(alto/3)


print(f'Screen size es de {Window.size[0]} por {Window.size[1]}')
print(f'Elimite de abajo es {limite_abajo_dados} y el límite de arriba {limite_arriba_dados}')


class MenuPrincipal(Screen):
    pass

class MyTextInput(TextInput):
    def on_parent(self, widget, parent):
        self.focus = True

class JugadoresScreen(Screen):
    def __init__(self, **kwargs):
        super(JugadoresScreen, self).__init__(**kwargs)
        listaJugadores = ObjectProperty(None)
        self.index_jugadores = 0
        self.counter_espacio = 0

    def on_pre_enter(self):
        Clock.schedule_once(self.añadir_jugador, 0)
        Window.softinput_mode = "below_target"

    def añadir_jugador(self, _):
        self.nuevo_jugador = MyTextInput(
            hint_text='Jugador@',
            font_size=font_general,
            #font_name= 'fonts/Titillium_Web/TitilliumWeb-SemiBold.ttf',
            size_hint_y=None,
            multiline=False,
            on_text_validate=self.enter_jugador
        )
        self.listaJugadores.add_widget(self.nuevo_jugador)
        self.focus = True
        self.scrollJugadores.scroll_to(self.nuevo_jugador)

    def enter_jugador(self, _):
        self.añadir_jugador(_)
    def save_data(self):
        for child in reversed(self.listaJugadores.children):
            if isinstance(child, TextInput):
                Jugadores_objeto.nuevo_jugador(child.text)

    def on_pre_leave(self):

        self.save_data()
        Jugadores_objeto.crear_jugadores()
        self.listaJugadores.clear_widgets()


class TurnoScreen(Screen):
    def __init__(self, **kwargs):
        super(TurnoScreen, self).__init__(**kwargs)
        turnoDe = ObjectProperty(None)

    def on_enter(self):
        self.nombre_jugador = Jugadores_objeto.devolver_nombre()
        self.turnoDe.text = f'Turno de {self.nombre_jugador}'


class GanadorScreen(Screen):
    def __init__(self, **kwargs):
        super(GanadorScreen, self).__init__(**kwargs)
        ganador = ObjectProperty(None)

    def on_pre_enter(self):
        self.nombre_jugador = Jugadores_objeto.check_ganador()[1]
        self.ganador.text = f'¡Felicidades, {self.nombre_jugador}!'
        for k,v in Jugadores_objeto.puntajes_ordenados.items():
            puntaje = Label(text=f" {k} : {v}", font_size=font_general)
            self.puntajes.add_widget(puntaje)
    def on_leave(self):
        Jugadores_objeto.limpiar_lista_jugadores()

class DormidaScreen(Screen):
    def __init__(self, **kwargs):
        super(DormidaScreen, self).__init__(**kwargs)
        ganador_dormida = ObjectProperty(None)

    def on_pre_enter(self):
        self.nombre_jugador = Jugadores_objeto.devolver_nombre()
        self.ganador_dormida.text = f'¡Felicidades, {self.nombre_jugador}!'
        Clock.schedule_once(self.mostrar_dados, 0)


    def mostrar_dados(self, _):
        self.Lanzada = Jugadores_objeto.jugada_actual
        for i in self.Lanzada:
            imagenesdados = ImagenDado(source=f'sprites/dado_{i}.png')
            self.campo_dados.add_widget(imagenesdados)

    def on_leave(self):
        #Implementar código para nueva partida aquí y en ganador screen para borrar todos los garbage data
        # En el archivo .kv poner root.nueva_partida en "on press"
        Jugadores_objeto.limpiar_lista_jugadores()


class LanzarWidget(Screen):
    def __init__(self, **kwargs):
        super(LanzarWidget, self).__init__(**kwargs)
    def lanzar(self):
        Jugadores_objeto.jugada_actual = Jugadores_objeto.lanzar()
    def on_leave(self, *args):
        dormida = Jugadores_objeto.ver_dormida()
        if dormida:
            self.manager.current = 'Dormida'



class CachoWidget(BoxLayout):
    # Esto en realidad tendría que ser un widget y no un boxlayout
    pass


class ImagenDado(Scatter):
    source = StringProperty(None)


class LanzadaScreen(Screen):

    def __init__(self, **kwargs):
        super(LanzadaScreen, self).__init__(**kwargs)
        campo = ObjectProperty(None)
        botones = ObjectProperty(None)

    def on_pre_enter(self):
        Clock.schedule_once(self.mostrar_dados, 0)

    def mostrar_dados(self, _):
        self.Lanzada = Jugadores_objeto.jugada_actual
        self.espacio_dados = FloatLayout()

        # Podríamos hacer que los dados no aparezcan encima de otros al guardar
        # su valor de posicionamiento

        for i in self.Lanzada:
            # Cambiar esto para la versión de computadora
            pos_x = int(random.randint(300, ancho-300))
            pos_y = int(random.randint(limite_arriba_dados, limite_abajo_dados))
            imagenesdados = ImagenDado(
                source=f'sprites/dado_{i}.png', pos=(pos_x, pos_y))
            self.espacio_dados.add_widget(imagenesdados)

        self.campo.add_widget(self.espacio_dados)

    def on_pre_leave(self):
        Jugadores_objeto.ver_posibilidades()

    def on_leave(self):
        Clock.schedule_once(self.borrar_dados, 0)

    def borrar_dados(self, _):
        self.espacio_dados.clear_widgets()


class CambiarScreen(Screen):

    def __init__(self, **kwargs):
        super(CambiarScreen, self).__init__(**kwargs)
        campo = ObjectProperty(None)
        botones = ObjectProperty(None)
        dados_seleccionados = ObjectProperty(None)
        self.numeros_dados_seleccionados = []
        self.key_dado_select = 0
        self.dado_resucitado = 0

    def on_pre_enter(self):
        Clock.schedule_once(self.mostrar_dados, 0)

    def mostrar_dados(self, _):
        self.Lanzada = Jugadores_objeto.jugada_actual
        self.espacio_dados = FloatLayout()
        self.botones_dict = {}
        self.ids_y_valores = {}
        self.counter = 0
        self.lista_seleccionados = []

        for i in self.Lanzada:

            key = 'dado_' + str(self.counter)
            pos_x = int(random.randint(300, ancho-300))
            pos_y = int(random.randint(limite_arriba_dados, limite_abajo_dados))

            dado = ImagenDado(
                source=f'sprites/dado_{i}_des.png', pos=(pos_x, pos_y))

            self.ids_y_valores[key] = i
            self.botones_dict[key] = dado
            self.botones_dict[key].bind(
                on_touch_down=lambda *args: self.my_function(i, *args))
            self.ids[key] = self.botones_dict[key]
            self.espacio_dados.add_widget(self.botones_dict[key])
            self.counter += 1

        self.campo.add_widget(self.espacio_dados)

    def my_function(self, numero_dado, instance, touch):
        self.selected_id = self.get_id(instance)
        self.numero_seleccionado = self.ids_y_valores[self.selected_id]

        self.mover_dado()

    def get_id(self,  instance):
        for id, widget in self.ids.items():
            if widget.__self__ == instance:
                return id

    def mover_dado(self):
        numero_dado = self.numero_seleccionado
        dado_select = Button(background_normal=f'sprites/dado_{numero_dado}.png',
                             size=(dado_size, dado_size),
                             size_hint=(None, None),
                             on_press=self.devolver_dado,
                             text=str(numero_dado),
                             color=(0, 0, 0, 0)
                             )
        self.nuevo_id_dado = f'dado_select_{self.key_dado_select}'
        self.ids[self.nuevo_id_dado] = dado_select
        self.key_dado_select += 1
        self.espacio_dados.remove_widget(self.ids[self.selected_id])

        self.dados_seleccionados.add_widget(dado_select)

    def devolver_dado(self, instance):
        id_seleccionado = self.get_id(instance)
        self.dados_seleccionados.remove_widget(self.ids[id_seleccionado])
        try:
            self.numeros_dados_seleccionados.remove(int(instance.text))
        except:
            print(f'No se pudo eliminar el dado: {instance.text}')
        valor_dado = instance.text
        self.dado_resucitado += 1


        key = 'dado_' + str(self.counter)




        pos_x = int(random.randint(300, ancho-300))
        pos_y = int(random.randint(limite_arriba_dados, limite_abajo_dados))
        dado = ImagenDado(source=f'sprites/dado_{valor_dado}_des.png', pos=(pos_x, pos_y))

        self.ids_y_valores[key] = valor_dado
        self.botones_dict[key] = dado
        # este valor se aprieta cada vez que se devuelve el dado
        self.botones_dict[key].bind(
            on_touch_down=lambda *args: self.my_function(valor_dado, *args))
        self.ids[key] = self.botones_dict[key]
        self.espacio_dados.add_widget(self.botones_dict[key])
        self.counter += 1

    def save_data(self):
        for child in reversed(self.dados_seleccionados.children):
            if isinstance(child, Button):
                self.numeros_dados_seleccionados.append(child.text)

    def relanzar(self):
        self.save_data()
        lista_index_cambiar = []
        lanzada = self.Lanzada
        for numero in self.numeros_dados_seleccionados:
            int_numero = int(numero)
            try:
                lista_index_cambiar.append(lanzada.index(int_numero))
            except:
                print('Algo falla en el index al añadir números')
        if lista_index_cambiar:
            Jugadores_objeto.cambiar_dados(lista_index_cambiar)
        self.manager.current = 'Anotar'

    def volcar(self):
        self.save_data()
        print(
            f'La lista de seleccionados es {self.numeros_dados_seleccionados}')
        lanzada = self.Lanzada
        lista_numeros_volcar = []
        for numero in self.numeros_dados_seleccionados:
            lista_numeros_volcar.append(int(numero))
        if lista_numeros_volcar:
            try:
                Jugadores_objeto.volcar_dados(lista_numeros_volcar)
            except:
                print(f'Hay un error en la lista: {lista_numeros_volcar}')
        self.manager.current = 'Anotar'

    def on_pre_leave(self):
        Jugadores_objeto.ver_posibilidades()

    def on_leave(self):
        Clock.schedule_once(self.borrar_dados, 0)

    def borrar_dados(self, _):
        for numero in self.numeros_dados_seleccionados:
            self.numeros_dados_seleccionados.remove(numero)
        self.espacio_dados.clear_widgets()
        self.dados_seleccionados.clear_widgets()


class AnotarScreen(Screen):
    def __init__(self, **kwargs):
        super(AnotarScreen, self).__init__(**kwargs)
        papel = ObjectProperty(None)
        campo_dados = ObjectProperty(None)
        botones_opciones = ObjectProperty(None)

    def on_pre_enter(self):
        Clock.schedule_once(self.mostrar_dados, 0)
        Clock.schedule_once(self.mostrar_opciones, 0)
        Clock.schedule_once(self.mostrar_anotados, 0)

    def mostrar_dados(self, _):
        self.Lanzada = Jugadores_objeto.jugada_actual
        for i in self.Lanzada:
            image = Image(source=f'sprites/dado_{i}.png', size=(dado_size,dado_size))
            self.dado = Scatter(
                size_hint=(None, None),
            )  
            self.dado.add_widget(image)
            self.campo_dados.add_widget(self.dado)

    def mostrar_anotados(self, _):
        self.puntajes = Jugadores_objeto.actualizar_resultados()
        # UI
        self.container = BoxLayout(orientation='vertical',
                                   spacing=10,
                                   pos_hint={'center_x': 0.4,
                                             'center_y': 0.50},
                                   )
        self.separador = Label(size_hint=(0.1, 0.1))
        self.nombre_jugador = Button(text=self.puntajes['Nombre'],
                                     size_hint=(0.05, 0.05),
                                     pos_hint={'center_x': 0.5,
                                               'center_y': 0.5},
                                     color=(0, 0, 0, 1),
                                     font_size=font_general,
                                     background_normal='sprites/numero_anotado.png',
                                     background_down='sprites/numero_down.png',
                                     )

        self.numeros = GridLayout(cols=3,
                                  spacing=1.5,
                                  size_hint=(1, 4))
        self.grandes = BoxLayout(orientation='horizontal',
                                 padding=10,
                                 size_hint=(0.6, 0.6),
                                 pos_hint={'center_x': 0.5, 'center_y': 0.2})
        for k, v in self.puntajes.items():
            if k != 'Nombre' and k != 'Grande1_g' and k != 'Grande2_g':
                numero = Button(text=str(v),
                                font_size=font_general,
                                size_hint=(0.8, 0.8),
                                color=(0, 0, 0, 1),
                                background_normal='sprites/numero_anotado.png',
                                background_down='sprites/numero_down.png')
                self.numeros.add_widget(numero)

        for k, v in self.puntajes.items():
            if k == 'Grande1_g' or k == 'Grande2_g':
                numero = Button(text=f"{v}",
                                font_size=font_general,
                                color=(0, 0, 0, 1),
                                background_normal='sprites/numero_anotado.png',
                                background_down='sprites/numero_down.png'
                                )
                self.grandes.add_widget(numero)
        self.container.add_widget(self.separador)
        self.container.add_widget(self.nombre_jugador)
        self.container.add_widget(self.numeros)
        self.container.add_widget(self.grandes)
        self.papel.add_widget(self.container)

    def mostrar_opciones(self, _):
        opciones = Jugadores_objeto.lista_posibilidades
        self.cantidad_opciones = 0
        Grande = Button(text=f'Grande',
                        font_size=font_general,
                        size_hint=(1, .8),
                        background_normal='sprites/button_verde_1.png',
                        background_down='sprites/button_verde_1_down.png',
                        on_press=self.opcion_elegida
                        )
        for opcion in opciones:
            if opcion == 'Grande':
                self.botones_opciones.add_widget(Grande)
                self.cantidad_opciones += 1

        for i in opciones:
            Boton = Button(text=f'{i}',
                           font_size=font_general,
                           size_hint=(1, .8),
                           background_normal='sprites/button_verde_1.png',
                           background_down='sprites/button_verde_1_down.png',
                           on_press=self.opcion_elegida
                           )
            if i != 'Grande':
                if Jugadores_objeto.actualizar_resultados()[i + '_g'] == '_':
                    self.botones_opciones.add_widget(Boton)
                    self.cantidad_opciones += 1

        espacio_vacio = Label(size_hint=(1,.7))
        if self.cantidad_opciones <= 1:
            self.botones_opciones.add_widget(espacio_vacio)
        Boton_otro = Button(text=f'Otras opciones',
                            font_size=font_general,
                            size_hint=(1, .8),
                            background_normal='sprites/button_naranja.png',
                            background_down='sprites/button_naranja_down.png',
                            on_press=self.otras_opciones
                            )
        self.botones_opciones.add_widget(Boton_otro)

    def otras_opciones(self, instance):
        self.manager.current = 'mas_opciones'

    def opcion_elegida(self, instance):
        eleccion = str(instance.text)
        Jugadores_objeto.anotar(eleccion)
        Jugadores_objeto.actualizar_resultados()
        Juego_finalizado = Jugadores_objeto.check_ganador()[0]
        if Juego_finalizado:
            self.manager.current = 'Ganador'
        else:
            Jugadores_objeto.cambiar_turno()
            self.manager.current = 'Turno'
        self.mostrar_anotado()

    def mostrar_anotado(self):
        # Esta función si tiene una utilidad
        pass

    def on_leave(self):
        Clock.schedule_once(self.borrar_todo, 0)

    def borrar_todo(self, _):
        self.papel.clear_widgets()
        self.campo_dados.clear_widgets()
        self.botones_opciones.clear_widgets()


class OpcionesScreen(Screen):
    def __init__(self, **kwargs):
        super(OpcionesScreen, self).__init__(**kwargs)
        papel_op = ObjectProperty(None)
        botones_opciones_op = ObjectProperty(None)

    def on_pre_enter(self):
        Clock.schedule_once(self.mostrar_opciones, 0)
        Clock.schedule_once(self.mostrar_anotados, 0)

    def mostrar_anotados(self, _):
        self.puntajes = Jugadores_objeto.actualizar_resultados()
        # UI
        self.container = BoxLayout(orientation='vertical',
                                   spacing=2,
                                   )
        self.nombre_jugador = Button(text=self.puntajes['Nombre'],
                                     size_hint=(0.2, 0.2),
                                     pos_hint={'center_x': 0.5,
                                               'center_y': 0.5},
                                     color=(0, 0, 0, 1),
                                     background_normal='sprites/numero_anotado.png',
                                     background_down='sprites/numero_anotado.png')
        self.numeros = GridLayout(cols=3)
        self.grandes = BoxLayout(orientation='horizontal',
                                 padding=10,
                                 size_hint=(0.6, 0.6),
                                 pos_hint={'center_x': 0.5})
        for k, v in self.puntajes.items():
            if k != 'Nombre' and k != 'Grande1_g' and k != 'Grande2_g':
                numero = Button(text=str(v),
                                font_size=font_general,
                                size_hint=(1, .8),
                                color=(0, 0, 0, 1),
                                background_normal='sprites/numero_anotado.png',
                                background_down='sprites/numero_down.png')
                self.numeros.add_widget(numero)

        for k, v in self.puntajes.items():
            if k == 'Grande1_g' or k == 'Grande2_g':
                numero = Button(text=f"{v}",
                                color=(0, 0, 0, 1),
                                font_size=font_general,
                                background_normal='sprites/numero_anotado.png',
                                background_down='sprites/numero_down.png'
                                )
                self.grandes.add_widget(numero)
        self.container.add_widget(self.nombre_jugador)
        self.container.add_widget(self.numeros)
        self.container.add_widget(self.grandes)
        self.papel_op.add_widget(self.container)

    def mostrar_opciones(self, _):
        opciones = Jugadores_objeto.devolver_posibilidades()
        self.fin_opciones = False
        cantidad_opciones = 0
        for k, v in opciones.items():
            Boton = Button(text=f'{k}',
                           font_size=font_general,
                           size_hint=(1, .3),
                           background_normal='sprites/button_verde_1.png',
                           background_down='sprites/button_verde_1_down.png',
                           on_press=self.opcion_elegida
                           )
            if v != 0 and Jugadores_objeto.actualizar_resultados()[k + '_g'] == '_':
                self.botones_opciones_op.add_widget(Boton)
                cantidad_opciones += 1
            if cantidad_opciones == 0:
                self.fin_opciones = True

        Boton_relanzar = Button(text=f'Volver a lanzar',
                                font_size=font_general,
                                size_hint=(1, .3),
                                background_normal='sprites/button_celeste.png',
                                background_down='sprites/button_celeste_down.png',
                                on_press=self.cambiar_dados
                                )
        Espacio_vacio = Label(size_hint=(1,.7))
        Boton_borrar = Button(text=f'Borrar',
                              font_size=font_general,
                              size_hint=(1, .3),
                              background_normal='sprites/button_naranja.png',
                              background_down='sprites/button_naranja_down.png',
                              on_press=self.borrar_casilla
                              )
        if self.fin_opciones:
            self.botones_opciones_op.add_widget(Espacio_vacio)
        if Jugadores_objeto.get_mano():
            self.botones_opciones_op.add_widget(Boton_relanzar)
        self.botones_opciones_op.add_widget(Boton_borrar)

    def cambiar_dados(self, instance):
        self.manager.current = 'Cambiar'

    def borrar_casilla(self, instance):
        self.manager.current = 'Borrar'

    def opcion_elegida(self, instance):
        eleccion = str(instance.text)
        Jugadores_objeto.anotar(eleccion)
        Jugadores_objeto.actualizar_resultados()
        Jugadores_objeto.cambiar_turno()
        self.mostrar_anotado()
        self.cambiar_jugador()

    def mostrar_anotado(self):
        pass

    def cambiar_jugador(self):
        self.manager.current = 'Turno'

    def on_leave(self):
        Clock.schedule_once(self.borrar_todo, 0)

    def borrar_todo(self, _):
        self.papel_op.clear_widgets()
        self.botones_opciones_op.clear_widgets()


class BorrarScreen(Screen):
    def __init__(self, **kwargs):
        super(BorrarScreen, self).__init__(**kwargs)
        mensaje = ObjectProperty(None)
        papel_bo = ObjectProperty(None)
        confirmar = ObjectProperty(None)
        self.key = ' '

    def on_pre_enter(self):
        Clock.schedule_once(self.mostrar_anotados, 0)

    def mostrar_anotados(self, _):
        self.puntajes = Jugadores_objeto.actualizar_resultados()
        # UI
        self.container = BoxLayout(orientation='vertical',
                                   )
        self.nombre_jugador = Button(text=self.puntajes['Nombre'],
                                     size_hint=(0.3, 0.3),
                                     pos_hint={'center_x': 0.5, 'center_y': 0},
                                     color=(0, 0, 0, 1),
                                     font_size=font_general-5,
                                     background_normal='sprites/numero_anotado.png',
                                     background_down='sprites/numero_down.png',
                                     )

        self.numeros = GridLayout(cols=3,
                                  spacing=5,
                                  size_hint=(1, 4))
        self.grandes = BoxLayout(orientation='horizontal',
                                 padding=8,
                                 size_hint=(1, 1),
                                 pos_hint={'center_x': 0.5})
        for k, v in self.puntajes.items():
            if k != 'Nombre' and k != 'Grande1_g' and k != 'Grande2_g':
                numero = Button(text=str(k),
                                font_size=font_general,
                                size_hint=(1, 1),
                                color=(0, 0, 0, 0),
                                background_normal='sprites/numero_anotado.png',
                                background_down='sprites/numero_down.png',
                                on_press=self.get_key_selected)

                numero_lleno = Button(text=str(v),
                                      font_size=font_general,
                                      size_hint=(1, 1),
                                      color=(0, 0, 0, 1),
                                      background_normal='sprites/numero_anotado.png',
                                      )
                if v == '_':
                    self.numeros.add_widget(numero)
                else:
                    self.numeros.add_widget(numero_lleno)
                self.ids[k] = numero

        for k, v in self.puntajes.items():
            if k == 'Grande1_g' or k == 'Grande2_g':
                espacio_grande = Button(text=str(k),
                                        font_size=font_general,
                                        size_hint=(1, 1),
                                        color=(0, 0, 0, 0),
                                        background_normal='sprites/numero_anotado.png',
                                        background_down='sprites/numero_down.png',
                                        on_press=self.get_grande_selected)

                espacio_grande_lleno = Button(text=str(v),
                                              font_size=font_general,
                                              size_hint=(1, 1),
                                              color=(0, 0, 0, 1),
                                              background_normal='sprites/numero_anotado.png',
                                              )
                # self.grandes.add_widget(numero)
                if v == '_':
                    self.grandes.add_widget(espacio_grande)
                else:
                    self.grandes.add_widget(espacio_grande_lleno)
                self.ids[str(k)] = numero
        self.container.add_widget(self.nombre_jugador)
        self.container.add_widget(self.numeros)
        self.container.add_widget(self.grandes)
        self.papel_bo.add_widget(self.container)

    def get_grande_selected(self, instance):
        self.mensaje.clear_widgets()
        self.confirmar.clear_widgets()
        self.key = instance.text[:-3]
        self.mostrar_mensaje(self.key)
        self.mostrar_boton()

    def get_key_selected(self, instance):
        self.mensaje.clear_widgets()
        self.confirmar.clear_widgets()
        self.key = instance.text[:-2]
        self.mostrar_mensaje(self.key)
        self.mostrar_boton()

    def mostrar_mensaje(self, mensaje):
        texto_confirmacion = Label(text=f"¿Segur@ que desea borrar {mensaje}?",
                                   color=(1, 1, 1, 1),
                                   font_size=font_general,
                                   #font_name= 'fonts/Titillium_Web/TitilliumWeb-SemiBold.ttf'
                                   )
        self.mensaje.add_widget(texto_confirmacion)

    def mostrar_boton(self):
        boton_confirmar = Button(text="Borrar",
                                 size_hint=(1, .8),
                                 font_size=font_general,
                                 background_normal='sprites/button_naranja.png',
                                 background_down='sprites/button_naranja_down.png',
                                 on_press=self.borrar_posibilidad)
        self.confirmar.add_widget(boton_confirmar)

    def borrar_posibilidad(self, instance):
        key_borrar = str(self.key)
        Jugadores_objeto.borrar_posibilidad(key_borrar)
        Clock.schedule_once(self.cambiar_turno, 0)

    def cambiar_turno(self, _):
        self.mensaje.clear_widgets()
        self.confirmar.clear_widgets()
        self.papel_bo.clear_widgets()
        Juego_finalizado = Jugadores_objeto.check_ganador()[0]
        if Juego_finalizado:
            self.manager.current = 'Ganador'
        else:
            Jugadores_objeto.cambiar_turno()
            self.manager.current = 'Turno'


class JuegoApp(App):
    
    font_general_a = NumericProperty(font_general)
    font_small_a = NumericProperty(font_small)
    dado_size_a = NumericProperty(dado_size)

    def build(self):
        sm = ScreenManager(transition=FadeTransition())
        sm.add_widget(MenuPrincipal())
        sm.add_widget(JugadoresScreen())
        sm.add_widget(TurnoScreen())
        sm.add_widget(LanzarWidget())
        sm.add_widget(LanzadaScreen())
        sm.add_widget(DormidaScreen())
        sm.add_widget(AnotarScreen())
        sm.add_widget(GanadorScreen())
        sm.add_widget(OpcionesScreen())
        sm.add_widget(CambiarScreen())
        sm.add_widget(BorrarScreen())
        return (sm)



if __name__ == '__main__':
    JuegoApp().run()
