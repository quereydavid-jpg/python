from direct.showbase.ShowBase import ShowBase
from panda3d.core import AmbientLight, DirectionalLight, LColor, Vec3, TextNode
from panda3d.core import CollisionTraverser, CollisionNode, CollisionSphere, CollisionHandlerQueue
from direct.gui.OnscreenText import OnscreenText
from direct.task import Task
import random

class LaberintoZombiesPanda(ShowBase):
    def __init__(self):
        super().__init__()
        self.disableMouse()

        # Configuración general de iluminación
        luz_ambiental = AmbientLight("luz_ambiental")
        luz_ambiental.setColor(LColor(0.6, 0.6, 0.6, 1))
        self.render.setLight(self.render.attachNewNode(luz_ambiental))

        luz_dir = DirectionalLight("luz_dir")
        luz_dir.setColor(LColor(0.8, 0.8, 0.8, 1))
        luz_node = self.render.attachNewNode(luz_dir)
        luz_node.setHpr(45, -45, 0)
        self.render.setLight(luz_node)

        # Variables de Estado del Juego
        self.nivel_actual = 1
        self.vidas = 3
        self.municion = 15
        self.puntuacion = 0
        
        # Listas de entidades del nivel
        self.paredes = []
        self.zombies = []
        self.balas = []
        self.cajas_municion = []
        self.meta_nodo = None

        # Controles de teclado
        self.teclas = {"w": False, "s": False, "a": False, "d": False}
        self.accept("w", self.actualizar_tecla, ["w", True])
        self.accept("w-up", self.actualizar_tecla, ["w", False])
        self.accept("s", self.actualizar_tecla, ["s", True])
        self.accept("s-up", self.actualizar_tecla, ["s", False])
        self.accept("a", self.actualizar_tecla, ["a", True])
        self.accept("a-up", self.actualizar_tecla, ["a", False])
        self.accept("d", self.actualizar_tecla, ["d", True])
        self.accept("d-up", self.actualizar_tecla, ["d", False])
        self.accept("space", self.disparar)

        # Interfaz de Usuario (HUD)
        self.texto_hud = OnscreenText(
            text="", pos=(-1.3, 0.9), scale=0.05, fg=(1, 1, 1, 1), align=TextNode.ALeft
        )
        self.texto_alerta = OnscreenText(
            text="", pos=(0, 0.7), scale=0.06, fg=(1, 0.3, 0.3, 1), align=TextNode.ACenter
        )

        # Iniciar Nivel 1
        self.cargar_nivel(self.nivel_actual)

        # Bucle principal
        self.taskMgr.add(self.bucle_juego_task, "BucleJuegoTask")

    def actualizar_tecla(self, tecla, estado):
        self.teclas[tecla] = estado

    def limpiar_nivel(self):
        for p in self.paredes: p.removeNode()
        for z in self.zombies: z["nodo"].removeNode()
        for b in self.balas: b["nodo"].removeNode()
        for c in self.cajas_municion: c.removeNode()
        if self.meta_nodo: self.meta_nodo.removeNode()
        if hasattr(self, "jugador") and self.jugador: self.jugador.removeNode()
        
        self.paredes.clear()
        self.zombies.clear()
        self.balas.clear()
        self.cajas_municion.clear()

    def cargar_nivel(self, nivel):
        self.limpiar_nivel()

        # 1. Crear al Personaje Principal
        self.jugador = self.loader.loadModel("models/box")
        self.jugador.reparentTo(self.render)
        self.jugador.setScale(0.6, 0.6, 1.8)
        self.jugador.setPos(0, -10, 0.9)
        self.jugador.setColor(0.1, 0.5, 0.9, 1)

        # 2. Diseñar Laberinto según el Nivel
        if nivel == 1:
            coordenadas_paredes = [
                (-5, 0, 10, 1), (5, 0, 10, 1), (0, 8, 1, 12), (-8, 12, 6, 1)
            ]
        elif nivel == 2:
            coordenadas_paredes = [
                (-4, 2, 8, 1), (4, 6, 1, 8), (-6, 10, 8, 1), (2, 14, 10, 1)
            ]
        else:
            coordenadas_paredes = [
                (-3, 3, 6, 1), (3, 7, 1, 8), (-5, 11, 8, 1), (4, 13, 6, 1), (-2, 16, 8, 1)
            ]

        for px, py, sx, sy in coordenadas_paredes:
            pared = self.loader.loadModel("models/box")
            pared.reparentTo(self.render)
            pared.setScale(sx, sy, 2.0)
            pared.setPos(px, py, 1.0)
            pared.setColor(0.3, 0.3, 0.3, 1)
            self.paredes.append(pared)

        # 3. Meta / Final del laberinto
        self.meta_nodo = self.loader.loadModel("models/box")
        self.meta_nodo.reparentTo(self.render)
        self.meta_nodo.setScale(1.5, 1.5, 0.1)
        self.meta_nodo.setPos(0, 22, 0.1)
        self.meta_nodo.setColor(0, 1, 0, 1)

        # 4. Cajas de Munición
        pos_municion = [(-6, 5), (6, 12), (0, 18)]
        for mx, my in pos_municion:
            caja = self.loader.loadModel("models/box")
            caja.reparentTo(self.render)
            caja.setScale(0.5, 0.5, 0.5)
            caja.setPos(mx, my, 0.3)
            caja.setColor(1, 0.8, 0, 1)
            self.cajas_municion.append(caja)

        # 5. Generar Zombies con estado "inactivo" por defecto
        cantidad_zombies = 2 + nivel
        for i in range(cantidad_zombies):
            z_nodo = self.loader.loadModel("models/box")
            z_nodo.reparentTo(self.render)
            z_nodo.setScale(0.6, 0.6, 1.8)
            z_nodo.setPos(random.randint(-8, 8), random.randint(5, 20), 0.9)
            z_nodo.setColor(0.2, 0.6, 0.2, 1) # Color zombie inactivo (verde normal)
            
            # Guardamos su vida (2 disparos) y su estado de alerta ("inactivo")
            self.zombies.append({"nodo": z_nodo, "vida": 2, "activo": False})

        self.texto_alerta.setText(f"¡BIENVENIDO AL NIVEL {nivel}! Explora con cuidado.")

    def disparar(self):
        if self.municion > 0:
            self.municion -= 1
            bala = self.loader.loadModel("models/box")
            bala.reparentTo(self.render)
            bala.setScale(0.2)
            bala.setPos(self.jugador.getPos() + Vec3(0, 0.5, 0))
            bala.setColor(1, 1, 0, 1)
            self.balas.append({"nodo": bala, "direccion": Vec3(0, 1, 0)})
        else:
            self.texto_alerta.setText("¡SIN MUNICIÓN! Busca cajas amarillas.")

    py_zombie_velocidades = {1: 2.5, 2: 4.0, 3: 5.5}

    def bucle_juego_task(self, task):
        dt = globalClock.getDt()
        velocidad_jugador = 7.0 * dt
        velocidad_zombie = self.py_zombie_velocidades[self.nivel_actual] * dt
        velocidad_bala = 35.0 * dt

        # Movimiento del Jugador
        pos = self.jugador.getPos()
        nueva_pos = Vec3(pos)
        if self.teclas["w"]: nueva_pos.y += velocidad_jugador
        if self.teclas["s"]: nueva_pos.y -= velocidad_jugador
        if self.teclas["a"]: nueva_pos.x -= velocidad_jugador
        if self.teclas["d"]: nueva_pos.x += velocidad_jugador

        colision_pared = False
        for pared in self.paredes:
            if (nueva_pos - pared.getPos()).length() < 1.2:
                colision_pared = True
                break
        
        if not colision_pared:
            self.jugador.setPos(nueva_pos)

        # Cámara siguiendo al jugador
        self.camera.setX(self.jugador.getX())
        self.camera.setY(self.jugador.getY() - 12)
        self.camera.setZ(self.jugador.getZ() + 6)
        self.camera.lookAt(self.jugador)

        # Comprobar recolección de munición
        for caja in self.cajas_municion[:]:
            if (self.jugador.getPos() - caja.getPos()).length() < 1.2:
                self.municion += 15
                caja.removeNode()
                self.cajas_municion.remove(caja)
                self.texto_alerta.setText("¡+15 Munición recargada!")

        # Comprobar si llegó a la meta
        if (self.jugador.getPos() - self.meta_nodo.getPos()).length() < 1.5:
            if self.nivel_actual < 3:
                self.nivel_actual += 1
                self.cargar_nivel(self.nivel_actual)
                return Task.cont
            else:
                self.texto_hud.setText("¡HAS GANADO EL JUEGO COMPLETANDO TODOS LOS NIVELES!")
                return Task.done

        # Lógica de los Zombies (Activación por proximidad)
        rango_deteccion = 8.0  # Distancia a la que el zombie detecta al jugador y cobra vida

        for z in self.zombies[:]:
            z_nodo = z["nodo"]
            z_pos = z_nodo.getPos()
            jugador_pos = self.jugador.getPos()
            distancia_al_jugador = (jugador_pos - z_pos).length()

            # Si el zombie está inactivo, comprobamos si el jugador se acercó lo suficiente
            if not z["activo"]:
                if distancia_al_jugador < rango_deteccion:
                    z["activo"] = True
                    z_nodo.setColor(0.8, 0.1, 0.1, 1) # Se pone de color rojo al activarse
            
            # Si ya está activo, se mueve persiguiendo al jugador
            if z["activo"]:
                direccion = (jugador_pos - z_pos)
                direccion.normalize()
                z_nodo.setPos(z_pos + direccion * velocidad_zombie)

                # Daño al tocar al jugador
                if distancia_al_jugador < 1.0:
                    self.vidas -= 1
                    self.jugador.setPos(0, -10, 0.9)
                    if self.vidas <= 0:
                        self.texto_hud.setText("¡GAME OVER! Los zombies te han atrapado.")
                        return Task.done

        # Mover Balas y Detección de Impactos
        for b in self.balas[:]:
            nodo_bala = b["nodo"]
            nodo_bala.setY(nodo_bala.getY() + velocidad_bala)

            if nodo_bala.getY() > 30:
                nodo_bala.removeNode()
                self.balas.remove(b)
                continue

            impacto_registrado = False
            for z in self.zombies[:]:
                if (nodo_bala.getPos() - z["nodo"].getPos()).length() < 1.2:
                    z["vida"] -= 1
                    impacto_registrado = True
                    # Si un zombie recibe un disparo, se activa inmediatamente aunque estuviera lejos
                    z["activo"] = True
                    z["nodo"].setColor(0.8, 0.1, 0.1, 1)
                    
                    if z["vida"] <= 0:
                        z["nodo"].removeNode()
                        self.zombies.remove(z)
                        self.puntuacion += 100
                    break
            
            if impacto_registrado:
                nodo_bala.removeNode()
                self.balas.remove(b)

        # Actualizar HUD
        self.texto_hud.setText(
            f"Nivel: {self.nivel_actual}/3  |  Vidas: {'❤ ' * self.vidas}  |  Munición: {self.municion}  |  Zombies Vivos: {len(self.zombies)}"
        )

        return Task.cont

if __name__ == "__main__":
    app = LaberintoZombiesPanda()
    app.run()