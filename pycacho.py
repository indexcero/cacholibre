import random

class Lanzada:
    """ Contiene métodos para lanzar los números 
    aleatorios en los dados. Y ver la 'dormida' """
    def __init__(self):
        self.jugada = [0, 0, 0, 0, 0]
    def lanzar(self):
        counter = 0
        for i in self.jugada:
            self.jugada[counter]=random.randint(1,6)
            counter += 1
        return(self.jugada)
    def ver_dormida(self):
        # Esta función está fallando
        self.dormida = False
        dados_repetidos = 0
        for i in self.jugada:
            dados_repetidos = self.jugada.count(i)
        if dados_repetidos > 4:
            self.dormida = True
        return(self.dormida)

class Analisis:
    def __init__(self, jugada):
        self.jugada = jugada
        self.numeros_repetidos = []
        self.puntajes = {}
        self.puntajes_ganadores = {}
        self.suma_numeros_repetidos = []
    def ver_numeros_repetidos(self):
        # La array de lanzamiento se llama self.jugada
        lanzada = self.jugada
        counter = 0
        self.senas= []
        self.quinas = []
        self.cuadras = []
        self.trenes = []
        self.tontos = []
        self.balas = []
        for i in lanzada:
            if counter < len(lanzada):
                if lanzada[counter] == 1:
                    self.balas.append(lanzada[counter])
                if lanzada[counter] == 2:
                    self.tontos.append(lanzada[counter])
                if lanzada[counter] == 3:
                    self.trenes.append(lanzada[counter])
                if lanzada[counter] == 4:
                    self.cuadras.append(lanzada[counter])
                if lanzada[counter] == 5:
                    self.quinas.append(lanzada[counter])
                if lanzada[counter] == 6:
                    self.senas.append(lanzada[counter])
                counter += 1
        return(self.senas, self.quinas, self.cuadras, self.trenes, self.tontos, self.balas)

    def sumar_numeros_repetidos(self):
        numeros_repetidos = self.ver_numeros_repetidos()
        for i in range(len(numeros_repetidos)):
            suma = 0
            for j in numeros_repetidos[i]:
                suma += j
            self.suma_numeros_repetidos.append(suma)
        return(self.suma_numeros_repetidos)

    def ver_opciones_numeros(self):
        #Aquí está tomando unos números muy extraños
        grupo_numeros_repetidos = self.sumar_numeros_repetidos()
        self.puntajes = {'Senas':grupo_numeros_repetidos[0], 'Quinas':grupo_numeros_repetidos[1],
                    'Cuadras':grupo_numeros_repetidos[2],'Trenes':grupo_numeros_repetidos[3],
                    'Tontos':grupo_numeros_repetidos[4],'Balas':grupo_numeros_repetidos[5]}
        return(self.puntajes)
        
    def ver_mejores_puntajes(self):
        self.puntajes_ganadores = {}
        for i in range(0,3):
            max_key = max(self.puntajes, key = self.puntajes.get)
            self.puntajes_ganadores[max_key] = self.puntajes.get(max_key)
            self.puntajes.pop(max_key)
        
        return(self.puntajes_ganadores)

    def ver_escalera(self):
        lanzada = self.jugada
        self.Escalera = False
        if 2 in lanzada and 3 in lanzada and 4 in lanzada and 5 in lanzada and 6 in lanzada:
            self.Escalera = True
        if 1 in lanzada and 2 in lanzada and 3 in lanzada and 4 in lanzada and 5 in lanzada:
            self.Escalera = True
        if 3 in lanzada and 4 in lanzada and 5 in lanzada and 6 in lanzada and 1 in lanzada:
            self.Escalera = True
        return(self.Escalera, lanzada)

    def ver_full(self):
        numeros_repetidos = self.ver_numeros_repetidos()
        self.Full = []
        self.es_Full = False
        self.Trica = False
        self.Doble = False
        def ver_tricas_y_dobles():
            counter = 0
            for i in numeros_repetidos:
                if len(i) == 3:
                    trica = numeros_repetidos[counter]
                    self.Trica = True
                    self.Full.append(trica)
                if len(i) == 2:
                    doble = numeros_repetidos[counter]
                    self.Doble = True 
                    self.Full.append(doble)
                counter += 1 
        ver_tricas_y_dobles()
        if self.Doble and self.Trica:
            self.es_Full = True
        return(self.es_Full,self.Full)

    def ver_poker(self):
        numeros_repetidos = self.ver_numeros_repetidos()
        self.Poker = False
        for element in numeros_repetidos:
            if len(element) > 3:
                self.Poker = True
        return(self.Poker, self.jugada)


    def ver_grande(self):
        numeros_repetidos = self.ver_numeros_repetidos()
        self.Grande = False
        for element in numeros_repetidos:
            if len(element) > 4:
                self.Grande = True
        return(self.Grande, self.jugada)


    def devolver_resultados(self):
        self.ver_opciones_numeros()
        #print(f'Todos los puntajes son: {self.puntajes}') !! Acordarse de esto
        self.todos_los_resultados = {
            'Puntajes_mejor' : self.ver_mejores_puntajes(),
            'Escalera' : self.ver_escalera(),
            'Poker': self.ver_poker(),
            'Full': self.ver_full(),
            'Grande' : self.ver_grande()
        }
        return(self.todos_los_resultados)



class Cambio:
    def __init__(self, jugada, de_mano):
        self.jugada = jugada
        self.de_mano = de_mano
    def volcar_dados(self):
        # Revisar funcionamiento, tiene bastantes bugs
        self.de_mano = False
        self.dado_intercambiable = int(input(f'Qué dado quisieras volcar?: '))        
        if self.jugada[self.dado_intercambiable] == 1:
            self.jugada[self.dado_intercambiable] = 6
        if self.jugada[self.dado_intercambiable] == 2:
            self.jugada[self.dado_intercambiable] = 5
        if self.jugada[self.dado_intercambiable] == 3:
            self.jugada[self.dado_intercambiable] = 4
        if self.jugada[self.dado_intercambiable] == 4:
            self.jugada[self.dado_intercambiable] = 3
        if self.jugada[self.dado_intercambiable] == 5:
            self.jugada[self.dado_intercambiable] = 2
        if self.jugada[self.dado_intercambiable] == 6:
            self.jugada[self.dado_intercambiable] = 1
        return(self.jugada, self.de_mano)

    def volver_a_lanzar(self):
        dados_lanzables = input('¿Qué dados quieres volver a lanzar? ').split()
        self.de_mano = False
        for element in dados_lanzables:
            self.jugada[int(element)] = random.randint(1,6)
        return(self.jugada, self.de_mano)

class Poderes:
    def __init__(self,de_mano,escalera,full,poker,grande):
        self.de_mano = de_mano
        self.escalera = escalera
        self.full = full
        self.poker = poker
        self.grande = grande
        self.sum_escalera = 0
        self.sum_full = 0
        self.sum_poker = 0
        self.sum_grande = 0

    def anotar_escalera(self):
        if self.escalera[0] == True:
            if self.de_mano == False:
                self.sum_escalera = 20
                return(self.sum_escalera)
            if self.de_mano == True:
                self.sum_escalera = 25
                return(self.sum_escalera)
        else:
            pass
    
    def anotar_full(self):

        if self.full[0] == True:
            if self.de_mano == False:
                self.sum_full= 30
                return(self.sum_full)
            if self.de_mano == True:
                self.sum_full= 35
                return(self.sum_full)
        else:
            pass
    
    def anotar_poker(self):
        if self.poker[0] == True:
            if self.de_mano == False:
                self.sum_poker = 40
                return(self.sum_poker)
            if self.de_mano == True:
                self.sum_poker = 45
                return(self.sum_poker)
        else:
            pass

    def anotar_grande(self):
        if self.grande[0] == True:
                self.sum_grande = 50
        else:
            pass

    def devolver_puntajes(self):
        self.anotar_escalera()
        self.anotar_full()
        self.anotar_grande()
        self.anotar_poker()
        self.puntajes_poder = {'Escalera':self.sum_escalera,
                                'Full':self.sum_full,
                                'Poker': self.sum_poker,
                                'Grande':self.sum_grande}
        return(self.puntajes_poder)


class Jugar:
    def __init__(self, nombre_jugador):
        self.nombre_jugador = nombre_jugador
        self.de_mano = True
        self.balas_guardar = '_'
        self.tontos_guardar = '_'
        self.trenes_guardar = '_'
        self.cuadras_guardar = '_'
        self.quinas_guardar = '_'
        self.senas_guardar = '_'
        self.escalera_guardar = '_'
        self.poker_guardar = '_'
        self.full_guardar = '_'
        self.grande_1_guardar = '_'
        self.grande_2_guardar = '_'


    def preguntar(self):
        self.imprimir_estado()
        self.jugada_lanzada = False
        self.cambios_realizados = False
        self.jugada_anotada = False
        Accion = input(f'''¿Qué desea hacer?
                        - Lanzar (h)
                        - Volver a lanzar dados(k)
                        - Anotar mi jugada(l)
                        - Ver mi jugada(v)
                        - Ver la tabla de puntajes(t)
                        - Borrar una casilla (r) 
                        - Ver el estado de los puntajes en el juego (w)
                        - Salir (x)\n''')

        if Accion == 'h':
            self.lanzar()
            print(f'\n Tu jugada es:\n {self.jugada} \n')
            # Aquí preguntar qué quisieras hacer.
            # Después que pase al siguiente turno 
            self.jugada_lanzada = True
            return(self.jugada_lanzada)
        if Accion == 'k':
            self.cambiar()
            print('\n Cambios realizados en la jugada \n')
            self.cambios_realizados = True
            return(self.cambios_realizados)
        if Accion == 'l':
            self.anotar()
            self.jugada_anotada = True
            print('\n Jugada anotada. \n ')
        if Accion == 'v':
            print(f'Tu jugada hasta el momento es: \n {self.jugada} \n ')
        if Accion == 't':
            self.imprimir_estado()
        if Accion == 'r':
            #preguntar sólo una vez que ya haya realizado su pregunta. 
            self.borrar()
        if Accion == 'w':
            self.estado_juego()
        if Accion == 'x':
            quit()


    def lanzar(self):
        self.jugada = Lanzada().lanzar()
        self.dormida = Lanzada().ver_dormida()
        print(f'Es dormida? {self.dormida}')
        return(self.jugada)
    def analizar(self):
        Analisis_objeto = Analisis(self.jugada)
        print(f'\n Tu jugada es: {Analisis_objeto.jugada} \n ')

        #Diccionario de resultados: 
        Resultados = Analisis_objeto.devolver_resultados()
        self.opciones_numeros = Analisis_objeto.ver_opciones_numeros()
        print(f'Todas las posibilidades numéricas son {self.opciones_numeros}')
        print(f'{Resultados} \n')

        Poderes_objeto = Poderes(self.de_mano, Resultados['Escalera'],
                        Resultados['Full'],
                        Resultados['Poker'], Resultados['Grande'])

        self.Puntajes_poderes = Poderes_objeto.devolver_puntajes()

        print(f'Los diccionarios de puntaje están así \n\n: {self.Puntajes_poderes} \n \n')
        return(self.Puntajes_poderes,self.opciones_numeros)

    def cambiar(self):
        Cambio_objeto = Cambio(self.jugada, self.de_mano)
        nueva_jugada = Cambio_objeto.volver_a_lanzar()
        self.jugada = nueva_jugada[0]
        self.de_mano = nueva_jugada[1]
        return(self.jugada, self.de_mano)

    def anotar(self):
        #Solución provisional, pensar cómo cambiar esto
        self.analizar()
        print(f'¿La jugada es de mano? {self.de_mano}')
        print(f'Tus posibilidades numéricas son {self.Puntajes_poderes}')
        print(f'Tus posibilidades numéricas son {self.opciones_numeros}')
        elec = input('Que quisieras anotar?  ')

        if self.Puntajes_poderes['Escalera'] != 0 and elec =='Escalera':
            print('Anotaré escalera')
            if self.escalera_guardar == '_':
                self.escalera_guardar = self.Puntajes_poderes['Escalera']
                #Tal vez matar la función con return de self.escalera_guardar
            else:
                print('No puedo guardar ahí, espacio lleno')
        if self.Puntajes_poderes['Grande'] != 0 and elec =='Grande':
            print('Anotaré grande')
            if self.grande_1_guardar == '_':
                self.grande_1_guardar = self.Puntajes_poderes['Grande']
            else:
                if self.grande_2_guardar == '_':
                    self.grande_2_guardar = self.Puntajes_poderes['Grande']
                else:
                    print('No puedo guardar ahí, espacio lleno')
        if self.Puntajes_poderes['Poker'] != 0 and elec =='Poker':
            print('Anotaré poker')
            if self.poker_guardar == '_':
                self.poker_guardar = self.Puntajes_poderes['Poker']
            else:
                print('No puedo guardar ahí, espacio lleno')
        if self.Puntajes_poderes['Full'] != 0 and elec =='Full':
            print('Anotaré full')
            if self.full_guardar == '_':
                self.full_guardar = self.Puntajes_poderes['Full']
            else:
                print('No puedo guardar ahí, espacio lleno')
        
        if self.balas_guardar == '_' and elec=='Balas':
            if self.opciones_numeros['Balas'] != 0:
                self.balas_guardar = self.opciones_numeros['Balas']
        else:
            print('No puedo guardar ahí, espacio lleno')
        if self.tontos_guardar == '_' and elec=='Tontos':
            if self.opciones_numeros['Tontos'] != 0:
                self.tontos_guardar = self.opciones_numeros['Tontos']
        else:
            print('No puedo guardar ahí, espacio lleno')
        if self.trenes_guardar == '_' and elec=='Trenes':
            if self.opciones_numeros['Trenes'] != 0:
                self.trenes_guardar = self.opciones_numeros['Trenes']
        else:
            print('No puedo guardar ahí, espacio lleno')
        if self.cuadras_guardar == '_' and elec=='Cuadras':
            if self.opciones_numeros['Cuadras'] != 0:
                self.cuadras_guardar = self.opciones_numeros['Cuadras']
        else:
            print('No puedo guardar ahí, espacio lleno')
        if self.quinas_guardar == '_' and elec=='Quinas':
            if self.opciones_numeros['Quinas'] != 0:
                self.quinas_guardar = self.opciones_numeros['Quinas']
        else:
            print('No puedo guardar ahí, espacio lleno')
        if self.senas_guardar == '_' and elec=='Senas':
            if self.opciones_numeros['Senas'] != 0:
                self.senas_guardar = self.opciones_numeros['Senas']
        else:
            print('No puedo guardar ahí, espacio lleno')

    
    def borrar(self):
        borrar_input = input('¿Qué casilla quisieras borrar?')
        # Borrar esta variable por una mejor implementación
        Borrar_logro = True
        if borrar_input == 'Senas':
            if self.senas_guardar == '_':
                self.senas_guardar = 0
            else:
                print('No puedo borrar esa casilla, casilla llena')
                Borrar_logro = False
        if borrar_input == 'Quinas':
            if self.quinas_guardar == '_':
                self.quinas_guardar = 0
            else:
                print('No puedo borrar esa casilla, casilla llena')
                Borrar_logro = False
        if borrar_input == 'Cuadras':
            if self.cuadras_guardar == '_':
                self.cuadras_guardar = 0
            else:
                print('No puedo borrar esa casilla, casilla llena')
                Borrar_logro = False
        if borrar_input == 'Trenes':
            if self.trenes_guardar == '_':
                self.trenes_guardar = 0
            else:
                print('No puedo borrar esa casilla, casilla llena')
                Borrar_logro = False
        if borrar_input == 'Tontos':
            if self.tontos_guardar == '_':
                self.tontos_guardar = 0
            else:
                print('No puedo borrar esa casilla, casilla llena')
                Borrar_logro = False
        if borrar_input == 'Balas':
            if self.balas_guardar == '_':
                self.balas_guardar = 0
            else:
                print('No puedo borrar esa casilla, casilla llena')
                Borrar_logro = False
        if borrar_input == 'Escalera':
            if self.escalera_guardar == '_':
                self.escalera_guardar = 0
            else:
                print('No puedo borrar esa casilla, casilla llena')
                Borrar_logro = False
        if borrar_input == 'Full':
            if self.full_guardar == '_':
                self.full_guardar = 0
            else:
                print('No puedo borrar esa casilla, casilla llena')
                Borrar_logro = False
        if borrar_input == 'Poker':
            if self.poker_guardar == '_':
                self.poker_guardar = 0
            else:
                print('No puedo borrar esa casilla, casilla llena')
                Borrar_logro = False
        if borrar_input == 'Grande':
            if self.grande_1_guardar != 0:
                self.grande_1_guardar = 0
            if self.grande_2_guardar != 0:
                self.grande_2_guardar = 0
            else:
                print(' No puedo borrar, casillas ya borradas')
                Borrar_logro = False
        pass

    def actualizar_resultados(self):
        self.diccionario_resultados = {'Nombre' : self.nombre_jugador,
                                    'Escalera_g' : self.escalera_guardar,
                                    'Poker_g': self.poker_guardar,
                                    'Full_g': self.full_guardar,
                                    'Grande1_g': self.grande_1_guardar,
                                    'Grande2_g': self.grande_2_guardar,
                                    'Balas_g' : self.balas_guardar,
                                    'Tontos_g' : self.tontos_guardar,
                                    'Trenes_g' : self.trenes_guardar,
                                    'Cuadras_g' : self.cuadras_guardar,
                                    'Quinas_g': self.quinas_guardar,
                                    'Senas_g': self.senas_guardar
                                    }
        return(self.diccionario_resultados)

    def check_panza_de_oro(self):
        #Revisar si es neceserio actualizar los resultados en cada llamada 
        self.actualizar_resultados()
        self.panza_de_oro = False
        tiene_full = self.diccionario_resultados['Full_g'] != '_' and self.diccionario_resultados['Full_g'] > 40
        tiene_poker = self.diccionario_resultados['Poker_g'] != '_' and self.diccionario_resultados['Poker_g'] > 40
        tiene_escalera = self.diccionario_resultados['Escalera_g'] != '_' and self.diccionario_resultados['Escalera_g'] > 20
        tiene_grande_1 = self.diccionario_resultados['Grande1_g'] != '_' and self.diccionario_resultados['Grande1_g'] == 50
        tiene_grande_2 = self.diccionario_resultados['Grande2_g'] != '_' and self.diccionario_resultados['Grande2_g'] == 50
        if tiene_full and tiene_poker and tiene_escalera and tiene_grande_1 and tiene_grande_2:
            self.panza_de_oro = True
        return(self.panza_de_oro)

    def check_puntajes(self):
        #Revisar si es neceserio actualizar los resultados en cada llamada 
        self.actualizar_resultados()
        self.puntajes_completos = False
        puntajes = list(self.diccionario_resultados.values())
        puntajes_limpio = puntajes[1:]
        self.valores_completos = 0
        counter = 0
        for i in puntajes_limpio:
            if puntajes_limpio[counter] != '_':
                counter +=1
                self.valores_completos += 1
            else:
                counter +=1
        if self.valores_completos >= len(puntajes_limpio):
            self.puntajes_completos = True
            print('Juego completo')
            return(self.puntajes_completos)
        
    
    def check_poker(self):
        #Revisar si es neceserio actualizar los resultados en cada llamada. 
        # Tal vez solo en la primera vez.
        self.actualizar_resultados()
        self.poker_completo = False
        poker_balas = False
        poker_tontos = False
        poker_trenes= False
        poker_cuadras = False
        poker_quinas = False
        poker_senas = False
        grande1 = False
        grande2 = False
        if self.diccionario_resultados['Balas_g'] != '_':
            poker_balas = self.diccionario_resultados['Balas_g'] >= 4
        if self.diccionario_resultados['Tontos_g'] != '_':
            poker_tontos = self.diccionario_resultados['Tontos_g'] >= 8
        if self.diccionario_resultados['Trenes_g'] != '_':
         poker_trenes = self.diccionario_resultados['Trenes_g'] >= 12
        if self.diccionario_resultados['Cuadras_g'] != '_':
            poker_cuadras= self.diccionario_resultados['Cuadras_g'] >= 8
        if self.diccionario_resultados['Quinas_g'] != '_':
            poker_quinas = self.diccionario_resultados['Quinas_g'] >= 20
        if self.diccionario_resultados['Senas_g'] != '_':
            poker_senas = self.diccionario_resultados['Senas_g'] >= 24
        if self.diccionario_resultados['Grande1_g'] != '_':
            grande_1 = self.diccionario_resultados['Grande1_g'] == 50
        if self.diccionario_resultados['Grande2_g'] != '_':
            grande_2 = self.diccionario_resultados['Grande2_g'] == 50

        primera_fila= poker_balas and poker_tontos and poker_trenes and grande_1
        segunda_fila= poker_cuadras and poker_quinas and poker_senas and grande_2
        self.poker_completo = primera_fila and segunda_fila
        if self.poker_completo:
            return(self.poker_completo)

    def estado_juego(self):
        self.actualizar_resultados()
        self.juego_completo = False
        self.jugador_ganador = False
        if self.dormida:
            self.juego_completo = True
            self.jugador_ganador = True
        if self.check_panza_de_oro():
            self.juego_completo = True
            self.jugador_ganador = True
        if self.check_poker():
            self.juego_completo == True
            self.jugador_ganador = True
        if self.check_puntajes():
            self.juego_completo = True
        #Tal vez mejorar esta manera de tomar los puntajes
        puntajes_limpio = list(self.diccionario_resultados.values())[1:]
        print(puntajes_limpio)
        self.puntaje_final = 0
        for i in range(len(puntajes_limpio)):
            if puntajes_limpio[i] != '_':
                self.puntaje_final += puntajes_limpio[i]
        print(f'''
                El jugador se ha dormido? {self.dormida}
                Existe la panza de oro? {self.check_panza_de_oro()}
                Existen todos los pokers? {self.check_poker()}
                Están todos los puntajes llenos? {self.check_puntajes()}
                La cantidad de puntajes completos es {self.valores_completos}''')
        print(f'El juego ha terminado? {self.juego_completo} El puntaje es: {self.puntaje_final}')
        print(f'El jugador ha ganado? {self.jugador_ganador}')
        return(self.juego_completo, self.jugador_ganador, self.puntaje_final)

    def imprimir_estado(self):
        self.Grafico = (f''' 
         {self.nombre_jugador}
        {self.balas_guardar} | {self.escalera_guardar} | {self.cuadras_guardar} 
        {self.tontos_guardar} | {self.full_guardar} | {self.quinas_guardar} 
        {self.trenes_guardar} | {self.poker_guardar} | {self.senas_guardar} 
        
            {self.grande_1_guardar}/{self.grande_2_guardar}

        ''')
        print(self.Grafico)

Adrian = Jugar('Adrián')

while True: 
    Adrian.preguntar()


class sistema_de_turnos():
    def __init__(self):
        pass
    def turno(self):
        #Si ya realizó la jugada, entonces preguntar si desea cambiar, pensar cómo implementar esto.
        pass
        
