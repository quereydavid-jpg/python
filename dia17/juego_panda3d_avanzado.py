from direct.showbase.ShowBase import ShowBase
from panda3d.core import AmbientLight, DirectionalLight, LColor, Vec3, TextNode
from panda3d.core import CollisionTraverser, CollisionNode, CollisionSphere, CollisionHandlerQueue
from direct.gui.OnscreenText import OnscreenText
from direct.task import Task
import random

class ShooterAvanzadoPanda3D(ShowBase):
    def __init__(self):
        super().__init__()

        # Configurar la ventana y desactivar el mouse por defecto
        self.disableMouse()

        # 1. Configurar Entorno e Iluminación
        self.entorno = self.loader.loadModel("models/environment")
        self.entorno.reparentTo(self.render)
        self.entorno.setScale(0.25, 0.25, 0.25)
        self.entorno.setPos(-8, 42, 0)

        luz_ambiental = AmbientLight("luz_ambiental")
        luz_ambiental.setColor(LColor(0.5, 0.5, 0.5, 1))
        self.render.setLight(self.render.attachNewNode(luz_ambiental))

        luz_dir = DirectionalLight("luz_dir")
        luz_dir.setColor(LColor(0.8, 0.8, 0.8, 1))
        luz_node = self.render.attachNewNode(luz_dir)
        luz_node.setHpr(45, -45, 0)
        self.render.setLight(luz_node)

        # 2. Crear al Personaje (Jugador)
        self.jugador = self.loader.loadModel("models/box")
        self.jugador.reparentTo(self.render)
        self.jugador.setScale(0.8, 0.8, 1.8)
        self.jugador.setPos(0, 0, 0.9)
        self.jugador.setColor(0.1, 0.6, 0.9, 1)  # Azul

        # Pistola en la mano
        self.pistola = self.loader.loadModel("models/box")
        self.pistola.reparentTo(self.jugador)
        self.pistola.setScale(0.3, 0.6, 0.3)
        self.pistola.setPos(0.6, 0.5, 0)
        self.pistola.setColor(0.2, 0.2, 0.2, 1)

        # 2.1 SEGUNDO MODELO: Cargar models/panda-model en otra posición con distinto comportamiento
        self.panda_npc = self.loader.loadModel("models/panda-model")
        self.panda_npc.reparentTo(self.render)
        self.panda_npc.setScale(0.5, 0.5, 0.5)
        self.panda_npc.setPos(8, 10, 0)  # Ubicado a la derecha del escenario

        # 3. Configuración de Cámara y Zoom
        self.distancia_zoom = 12.0  # Distancia inicial detrás del jugador
        self.camera.setPos(0, -self.distancia_zoom, 6)
        self.camera.lookAt(self.jugador)

        # 4. Listas y Variables del Juego
        self.zombies = []
        self.balas = []
        self.tiempo_ultimo_zombie = 0
        self.intervalo_zombie = 15.0

        # Controles de movimiento
        self.teclas = {"w": False, "s": False, "a": False, "d": False}
        self.accept("w", self.actualizar_tecla, ["w", True])
        self.accept("w-up", self.actualizar_tecla, ["w", False])
        self.accept("s", self.actualizar_tecla, ["s", True])
        self.accept("s-up", self.actualizar_tecla, ["s", False])
        self.accept("a", self.actualizar_tecla, ["a", True])
        self.accept("a-up", self.actualizar_tecla, ["a", False])
        self.accept("d", self.actualizar_tecla, ["d", True])
        self.accept("d-up", self.actualizar_tecla, ["d", False])
        
        # Disparar con barra espaciadora
        self.accept("space", self.disparar)

        # Controles de Zoom (+ y - / o corchetes como alternativa cómoda)
        self.accept("add", self.ajustar_zoom, [-1.5])    # Tecla + del teclado numérico
        self.accept("hyphen", self.ajustar_zoom, [1.5])   # Tecla - del teclado numérico
        self.accept("=", self.ajustar_zoom, [-1.5])       # Tecla + general
        self.accept("-", self.ajustar_zoom, [1.5])       # Tecla - general
        self.accept("[", self.ajustar_zoom, [1.5])       # Alternativa alejar
        self.accept("]", self.ajustar_zoom, [-1.5])      # Alternativa acercar

        # 5. Sistema de Colisiones Básicas (CollisionTraverser)
        self.cTrav = CollisionTraverser()
        self.col_handler = CollisionHandlerQueue()

        # Esfera de colisión en el Jugador
        col_node_jugador = CollisionNode("col_jugador")
        col_node_jugador.addSolid(CollisionSphere(0, 0, 0, 1.5))
        self.c_jugador_path = self.jugador.attachNewNode(col_node_jugador)

        # Esfera de colisión en la Cámara
        col_node_camara = CollisionNode("col_camara")
        col_node_camara.addSolid(CollisionSphere(0, 0, 0, 0.5))
        self.c_camara_path = self.camera.attachNewNode(col_node_camara)
        
        # Registrar colisión de la cámara contra el jugador
        self.cTrav.addCollider(self.c_camara_path, self.col_handler)

        # 6. Interfaz de Usuario (HUD / Textos)
        self.texto_municion = OnscreenText(
            text="Munición: ∞ (INFINITA)", pos=(-1.3, 0.9), scale=0.06, fg=(1, 1, 1, 1), align=TextNode.ALeft
        )
        self.texto_zombies = OnscreenText(
            text="Zombies en escena: 0", pos=(-1.3, 0.83), scale=0.06, fg=(1, 0.2, 0.2, 1), align=TextNode.ALeft
        )
        self.texto_tiempo = OnscreenText(
            text="Próximo Zombie en: 15.0s", pos=(-1.3, 0.76), scale=0.06, fg=(1, 1, 0, 1), align=TextNode.ALeft
        )
        
        # Etiqueta de texto para la posición exacta de la cámara (actualizada en cada cuadro)
        self.texto_pos_cam = OnscreenText(
            text="Cámara Pos: (0, 0, 0)", pos=(1.3, 0.9), scale=0.05, fg=(0.2, 1, 0.2, 1), align=TextNode.ARight
        )

        # Etiqueta de aviso de colisión de cámara
        self.texto_alerta_cam = OnscreenText(
            text="", pos=(0, 0.6), scale=0.06, fg=(1, 0.3, 0.3, 1), align=TextNode.ACenter
        )

        # Registrar bucle principal
        self.taskMgr.add(self.bucle_juego_task, "BucleJuegoTask")

    def actualizar_tecla(self, tecla, estado):
        self.teclas[tecla] = estado

    def ajustar_zoom(self, cantidad):
        # Modifica la distancia de la cámara limitándola entre un rango seguro
        self.distancia_zoom = max(4.0, min(30.0, self.distancia_zoom + cantidad))

    def disparar(self):
        bala = self.loader.loadModel("models/box")
        bala.reparentTo(self.render)
        bala.setScale(0.2)
        bala.setPos(self.jugador.getPos() + Vec3(0.6, 0.5, 0))
        bala.setColor(1, 1, 0, 1)
        self.balas.append({"nodo": bala, "direccion": Vec3(0, 1, 0)})

    def spawnear_zombie(self):
        zombie = self.loader.loadModel("models/box")
        zombie.reparentTo(self.render)
        zombie.setScale(0.8, 0.8, 1.8)
        
        x_aleatorio = random.randint(-15, 15)
        y_aleatorio = random.randint(15, 25)
        zombie.setPos(x_aleatorio, y_aleatorio, 0.9)
        zombie.setColor(0.6, 0.1, 0.1, 1)
        self.zombies.append(zombie)

    def bucle_juego_task(self, task):
        dt = globalClock.getDt()
        velocidad_jugador = 8.0 * dt
        velocidad_zombie = 3.0 * dt
        velocidad_bala = 30.0 * dt

        # 1. Movimiento del Jugador con WASD
        pos = self.jugador.getPos()
        if self.teclas["w"]: pos.y += velocidad_jugador
        if self.teclas["s"]: pos.y -= velocidad_jugador
        if self.teclas["a"]: pos.x -= velocidad_jugador
        if self.teclas["d"]: pos.x += velocidad_jugador
        self.jugador.setPos(pos)

        # 2. Comportamiento diferente para el segundo modelo (Panda NPC): Rota y se desplaza en círculo
        angulo_panda = task.time * 40
        self.panda_npc.setH(angulo_panda)
        x_panda = 8 + 3 * random.choice([-1, 1]) * (task.time % 2) # Ligero movimiento orgánico
        self.panda_npc.setX(x_panda)

        # 3. Posicionar la cámara detrás del jugador aplicando el zoom dinámico
        self.camera.setX(pos.x)
        self.camera.setY(pos.y - self.distancia_zoom)
        self.camera.setZ(pos.z + 5)
        self.camera.lookAt(self.jugador)

        # 4. Actualizar la etiqueta de texto con la posición actual de la cámara
        cam_pos = self.camera.getPos()
        self.texto_pos_cam.setText(f"Cámara Pos: ({cam_pos.x:.1f}, {cam_pos.y:.1f}, {cam_pos.z:.1f})")

        # 5. Ejecutar chequeo de colisiones (CollisionTraverser)
        self.cTrav.traverse(self.render)
        
        # Comprobar si la cámara está demasiado cerca del personaje
        colision_detectada = False
        for entrada in self.col_handler.getEntries():
            if entrada.getIntoNodePath() == self.c_jugador_path:
                colision_detectada = True
                break

        if colision_detectada:
            self.texto_alerta_cam.setText("⚠️ ¡CÁMARA DEMASIADO CERCA DEL PERSONAJE! ⚠️")
        else:
            self.texto_alerta_cam.setText("")

        # 6. Generación de zombies cada 15 segundos
        self.tiempo_ultimo_zombie += dt
        tiempo_restante = max(0.0, self.intervalo_zombie - self.tiempo_ultimo_zombie)
        self.texto_tiempo.setText(f"Próximo Zombie en: {tiempo_restante:.1f}s")

        if self.tiempo_ultimo_zombie >= self.intervalo_zombie:
            self.spawnear_zombie()
            self.tiempo_ultimo_zombie = 0.0

        # Mover Zombies hacia el jugador
        for z in self.zombies[:]:
            z_pos = z.getPos()
            jugador_pos = self.jugador.getPos()
            
            direccion = (jugador_pos - z_pos)
            direccion.normalize()
            z.setPos(z_pos + direccion * velocidad_zombie)

            if (z_pos - jugador_pos).length() < 1.0:
                self.texto_municion.setText("¡HAS SIDO ATRAPADO POR UN ZOMBIE!")
                return Task.done

        # Mover Balas e impactos
        for b in self.balas[:]:
            nodo_bala = b["nodo"]
            nodo_bala.setY(nodo_bala.getY() + velocidad_bala)

            if nodo_bala.getY() > 50:
                nodo_bala.removeNode()
                self.balas.remove(b)
                continue

            impacto = False
            for z in self.zombies[:]:
                if (nodo_bala.getPos() - z.getPos()).length() < 1.2:
                    z.removeNode()
                    self.zombies.remove(z)
                    impacto = True
                    break
            
            if impacto:
                nodo_bala.removeNode()
                self.balas.remove(b)

        self.texto_zombies.setText(f"Zombies en escena: {len(self.zombies)}")

        return Task.cont

if __name__ == "__main__":
    app = ShooterAvanzadoPanda3D()
    app.run()