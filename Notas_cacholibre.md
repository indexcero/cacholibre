## Tareas por hacer 

### El objeto de ver estado debe retornar también si el turno ha terminado
### Explicar que retornos guarda cada función

- No funciona bien la dormida
- Revisar que el sistema de suma de puntajes funcione bien
- Revisar dónde puede el jugador puede anotar su jugada
  - Revisar la obligatoriedad del turno, si o si se debe anotar
    - Quizás algo como

```python

self.turno_de_adrian = 1
self.turno_de_vale = 0 


while (Juego_completo != True):
    while (turno de adrian == 1):
        Adrian.jugar()
        Adrian.comprobar_estado()
        self.turno_de_adrian = Adrian.comprobar_estado()[0]
        if self.turno de adrian == 'Completo':
            print('Turno completo')
            turno_de_adrian = 0
    self.turno_de_adrian = 1

    if Turnos['Jugador_1'] == 1:
        Jugador_1.Jugar
        
    # Que la función de comprobar estado devuelva si el turno está completo

```

- Revisar mejor el sistema de turnos, que pase al oponente

- Hacer un diccionario de Nombres y objetos 



# Empezar a implementar el kivy
Screen1
Gridlayout
    Label
    Rectangle
    Button 
    Button
    Button
    Label

Screen2
Box Layout 
    Label
    Button 
    Button

Screen3
Box Layout 
    Label
    Button 
    Button
