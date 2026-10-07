# MOMENTUM · Python y DRL

Curso práctico de **1 hora** para repasar los fundamentos de Python. Trabajarás con notebooks de Jupyter que combinan explicaciones breves, ejemplos que puedes ejecutar y ejercicios.

**Requisitos previos:** ninguno. **Nivel:** inicial.

## Elige cómo trabajar

| Opción | Qué necesitas | Recomendada si… |
|---|---|---|
| [**A · Docker**](#opción-a--docker-recomendada) | Docker instalado | Quieres el entorno listo, idéntico al del aula |
| [**B · GitHub Codespaces**](#opción-b--github-codespaces) | Una cuenta de GitHub | No puedes o no quieres instalar nada |
| [**C · Tu propio Python**](#opción-c--tu-propio-python) | Python 3.10 o superior | Ya tienes Python y prefieres tu editor |

Las tres opciones usan exactamente los mismos notebooks.

## Opción A · Docker (recomendada)

Instala [Docker Desktop](https://docs.docker.com/get-docker/) (Windows, macOS) o Docker Engine (Linux) y comprueba que está en marcha. Después, en una terminal:

```bash
docker run -d --name momentum-drl -p 8080:8080 -v momentum-drl:/home/coder/workspace ghcr.io/ugr-sail/momentum-drl:latest
```

La primera vez descarga la imagen (unos minutos). Cuando termine:

1. Abre <http://localhost:8080> en el navegador.
2. Introduce la contraseña `curso2026`.
3. Abre `00_bienvenida.ipynb`. Si te pide un kernel, elige **Python (curso)**.

Verás VS Code en el navegador con Python, Jupyter y todas las librerías ya instaladas. Tu trabajo se guarda en el volumen `momentum-drl` y se conserva aunque apagues el ordenador.

| Quiero… | Comando |
|---|---|
| Detener el curso | `docker stop momentum-drl` |
| Volver a arrancarlo | `docker start momentum-drl` |
| Empezar de cero con el material original | `docker rm -f momentum-drl && docker volume rm momentum-drl` y repetir el `docker run` |
| Actualizar a la última versión | `docker pull ghcr.io/ugr-sail/momentum-drl:latest` y empezar de cero (⚠️ borra tu trabajo: descarga antes los notebooks que quieras conservar con clic derecho → *Download*) |

<details>
<summary>Alternativa con Docker Compose y los notebooks en tu carpeta</summary>

Si prefieres que los notebooks estén en una carpeta de tu equipo (por ejemplo, para hacer copias), descarga este repositorio (botón **Code → Download ZIP**, o `git clone`) y, dentro de la carpeta:

```bash
docker compose up -d
```

Abre <http://localhost:8080> (contraseña `curso2026`). Lo que hagas queda en la carpeta `workspace/`. Para detenerlo: `docker compose down`.

</details>

<details>
<summary>Problemas frecuentes</summary>

- **`port is already allocated`:** otro programa usa el puerto 8080. Cambia `-p 8080:8080` por `-p 8888:8080` y abre <http://localhost:8888>.
- **`The container name "/momentum-drl" is already in use`:** ya lo creaste antes. Usa `docker start momentum-drl`.
- **`Cannot connect to the Docker daemon`:** Docker no está en marcha. Abre Docker Desktop y espera a que arranque.

</details>

## Opción B · GitHub Codespaces

[![Abrir en GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/ugr-sail/momentum-drl)

Pulsa el botón (o *Code → Codespaces → Create codespace* en esta página). Se abre VS Code en el navegador con todo instalado; la primera vez tarda unos minutos. Las cuentas personales de GitHub incluyen horas gratuitas al mes.

Para recuperar un notebook original, ejecuta `git restore workspace/` en la terminal.

## Opción C · Tu propio Python

Descarga este repositorio (**Code → Download ZIP**, o `git clone https://github.com/ugr-sail/momentum-drl`) y, dentro de la carpeta:

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m ipykernel install --user --name curso-python --display-name "Python (curso)"
jupyter lab workspace
```

También puedes abrir la carpeta con VS Code (extensiones *Python* y *Jupyter*) o, si tienes Docker y la extensión *Dev Containers*, elegir *Reopen in Container*.

## Contenido

| Notebook | Contenido | Tiempo |
|---|---|---|
| [`00_bienvenida`](workspace/00_bienvenida.ipynb) | Presentación y uso de notebooks | — |
| [`01_variables_y_tipos`](workspace/01_variables_y_tipos.ipynb) | Variables, tipos, operadores, cadenas y f-strings | 15 min |
| [`02_colecciones`](workspace/02_colecciones.ipynb) | Listas, tuplas, diccionarios y conjuntos | 15 min |
| [`03_control_de_flujo`](workspace/03_control_de_flujo.ipynb) | `if`, bucles `for` y `while`, comprensiones | 15 min |
| [`04_funciones`](workspace/04_funciones.ipynb) | Funciones, errores y módulos | 15 min |

Cada notebook termina con ejercicios. Intenta resolverlos antes de mirar las soluciones en [`workspace/soluciones/`](workspace/soluciones/).
Para practicar por tu cuenta tienes un notebook vacío: [`workspace/plantilla.ipynb`](workspace/plantilla.ipynb).

## Cómo trabajar con los notebooks

- Ejecuta una celda con **Mayús + Intro**. Ejecuta las celdas **en orden**, de arriba abajo.
- Si aparece un `NameError`, probablemente te saltaste una celda anterior: usa *Run All* (ejecutar todo) o reinicia el kernel y vuelve a empezar desde arriba.
- Puedes modificar los ejemplos y experimentar sin miedo.

## Licencia y autoría

Contenido didáctico bajo [CC BY 4.0](LICENSE-CONTENT.md); código y configuración bajo [MIT](LICENSE).

Miguel Molina-Solana · [SAIL-UGR research group](https://github.com/ugr-sail) · Universidad de Granada
