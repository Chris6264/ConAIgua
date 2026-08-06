## Ejecución de la interfaz web

Para ejecutar la interfaz web del proyecto, primero se debe clonar el repositorio correspondiente:

```bash
git clone https://github.com/Chris6264/conaigua-chat-ui.git
cd conaigua-chat-ui
```

La interfaz web utiliza **Docker** para levantar el entorno de desarrollo de manera controlada y reproducible. La aplicación está construida con **React** y **Next.js**, y utiliza **pnpm** para la instalación de dependencias.

### 1. Instalar dependencias

Primero, se deben instalar las dependencias del frontend mediante el siguiente comando:

```bash
docker compose run --rm frontend sh -c "corepack enable && pnpm install"
```

### 2. Levantar la interfaz web

Después de instalar las dependencias, se puede levantar la interfaz web con:

```bash
docker compose up
```

Una vez ejecutado el comando anterior, Docker inicia los servicios necesarios para montar la interfaz web. Desde esta interfaz, el usuario podrá interactuar con el sistema, realizar consultas en lenguaje natural y visualizar las respuestas generadas por el agente.
