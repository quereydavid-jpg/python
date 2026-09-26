from direct.showbase.ShowBase import ShowBase
from panda3d.core import AmbientLight, DirectionalLight, LColor, Vec3, TextNode
from direct.gui.OnscreenText import OnscreenText
from direct.task import Task
import random

class ShooterPanda3D(ShowBase):
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
        self.jugador.setScale(0.8, 0.8, 1.8)  # Forma humanoide básica
        self.jugador.setPos(0, 0, 0.9)
        self.jugador.setColor(0.1, 0.6, 0.9, 1)  # Azul

        # Pistola en la mano (un pequeño bloque acoplado al frente del jugador)
        self.pistola = self.loader.loadModel("models/box")
        self.pistola.reparentTo(self.jugador)
        self.pistola.setScale(0.3, 0.6, 0.3)
        self.pistola.setPos(0.6, 0.5, 0)
        self.pistola.setColor(0.2, 0.2, 0.2, 1)  # Gris oscuro

        # Posición de la cámara en tercera persona detrás del jugador
        self.camera.setPos(0, -15, 6)
        self.camera.lookAt(self.jugador)

        # 3. Listas y Variables del Juego
        self.zombies = []
        self.balas = []
        self.tiempo_ultimo_zombie = 0
        self.intervalo_zombie = 15.0  # Aparece un zombie cada 15 segundos

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
        
        # Disparar con la barra espaciadora
        self.accept("space", self.disparar)

        # 4. Interfaz en pantalla (HUD)
        self.texto_municion = OnscreenText(
            text="Munición: ∞ (INFINITA)",
            pos=(-1.3, 0.9), scale=0.07, fg=(1, 1, 1, 1), align=TextNode.ALeft
        )
        self.texto_zombies = OnscreenText(
            text="Zombies en escena: 0",
            pos=(-1.3, 0.8), scale=0.07, fg=(1, 0.2, 0.2, 1), align=TextNode.ALeft
        )
        self.texto_tiempo = OnscreenText(
            text="Próximo Zombie en: 15.0s",
            pos=(-1.3, 0.7), scale=0.07, fg=(1, 1, 0, 1), align=TextNode.ALeft
        )

        # Registrar el bucle principal de juego
        self.taskMgr.add(self.bucle_juego_task, "BucleJuegoTask")

    def actualizar_tecla(self, tecla, estado):
        self.teclas[tecla] = estado

    def disparar(self):
        # Crear una bala (pequeña esfera o cubo amarillo)
        bala = self.loader.loadModel("models/box")
        bala.reparentTo(self.render)
        bala.setScale(0.2)
        # Posición inicial de la bala en la pistola
        bala.setPos(self.jugador.getPos() + Vec3(0.6, 0.5, 0))
        bala.setColor(1, 1, 0, 1) # Amarillo
        
        # Guardamos la bala junto con su dirección de avance
        self.balas.append({"nodo": bala, "direccion": Vec3(0, 1, 0)})

    def spawnear_zombie(self):
        # Crear un zombie (bloque de color rojo oscuro)
        zombie = self.loader.loadModel("models/box")
        zombie.reparentTo(self.render)
        zombie.setScale(0.8, 0.8, 1.8)
        
        # Aparecer en una posición aleatoria alrededor del mapa
        x_aleatorio = random.randint(-15, 15)
        y_aleatorio = random.randint(15, 25)
        zombie.setPos(x_aleatorio, y_aleatorio, 0.9)
        zombie.setColor(0.6, 0.1, 0.1, 1) # Rojo zombie
        
        self.zombies.append(zombie)

    def bucle_juego_task(self, task):
        dt = globalClock.getDt()
        velocidad_jugador = 8.0 * dt
        velocidad_zombie = 3.0 * dt
        velocidad_bala = 30.0 * dt

        # Movimiento del Jugador con WASD
        pos = self.jugador.getPos()
        if self.teclas["w"]: pos.y += velocidad_jugador
        if self.teclas["s"]: pos.y -= velocidad_jugador
        if self.teclas["a"]: pos.x -= velocidad_jugador
        if self.teclas["d"]: pos.x += velocidad_jugador
        self.jugador.setPos(pos)

        # Hacer que la cámara siga suavemente al jugador
        self.camera.setX(pos.x)
        self.camera.setY(pos.y - 12)

        # Generar enemigos cada 15 segundos
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
            
            # Calcular dirección hacia el jugador
            direccion = (jugador_pos - z_pos)
            direccion.normalize()
            z.setPos(z_pos + direccion * velocidad_zombie)

            # Detectar si el zombie toca al jugador (Game Over básico)
            if (z_pos - jugador_pos).length() < 1.0:
                self.texto_municion.setText("¡HAS SIDO ATRAPADO POR UN ZOMBIE!")
                return Task.done

        # Mover Balas y detectar impactos en zombies
        for b in self.balas[:]:
            nodo_bala = b["nodo"]
            nodo_bala.setY(nodo_bala.getY() + velocidad_bala)

            # Eliminar bala si sale demasiado lejos de la pantalla
            if nodo_bala.getY() > 50:
                nodo_bala.removeNode()
                self.balas.remove(b)
                continue

            # Comprobar colisión de la bala con los zombies
            impacto = False
            for z in self.zombies[:]:
                if (nodo_bala.getPos() - z.getPos()).length() < 1.2:
                    # Destruir zombie y bala
                    z.removeNode()
                    self.zombies.remove(z)
                    impacto = True
                    break
            
            if impacto:
                nodo_bala.removeNode()
                self.balas.remove(b)

        # Actualizar textos del HUD
        self.texto_zombies.setText(f"Zombies en escena: {len(self.zombies)}")

        return Task.cont

if __name__ == "__main__":
    app = ShooterPanda3D()
    app.run()