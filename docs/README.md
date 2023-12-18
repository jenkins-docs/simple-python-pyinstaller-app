# Explicación

### Terraform para configurar Docker in Docker con Jenkins

El archivo `main.tf` contiene la configuración de Terraform para desplegar un entorno Docker in Docker con Jenkins. Aquí se describen las principales secciones del archivo:

#### Configuración de Terraform

```hcl
terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0.1"
    }
  }
}

provider "docker" {}
```

- **Configuración del Proveedor**: Se establece la versión del proveedor de Docker que se utilizará.

#### Recursos Docker

```hcl
resource "docker_network" "jenkins" {
  name = "jenkins"
}

resource "docker_volume" "jenkins-docker-certs" {
  name = "jenkins-docker-certs"
}

resource "docker_volume" "jenkins-data" {
  name = "jenkins-data"
}

resource "docker_volume" "homeDir" {
  name = "homeDir"
}
```

- **Red y Volúmenes de Docker**: Se definen la red y volúmenes necesarios para el entorno de Jenkins.

```hcl
resource "docker_image" "docker_dind" {
  name         = "docker:dind"
  keep_locally = false
}
```

- **Imagen de Docker in Docker**: Se especifica la imagen de Docker in Docker que se utilizará.

### Terraform (main.tf)

#### Recurso `docker_container` para Jenkins-Docker (Docker in Docker)

```hcl
resource "docker_container" "jenkins-docker" {
  image = docker_image.docker_dind.image_id
  name  = "jenkins-docker"
  privileged = true

  network_mode = docker_network.jenkins.name

  env = [
    "DOCKER_TLS_CERTDIR=/certs",
  ]

  volumes {
    volume_name = docker_volume.jenkins-docker-certs.name
    container_path = "/certs/client"
  }

  volumes {
    volume_name    = docker_volume.jenkins-data.name
    container_path = "/var/jenkins_home"
  }

  ports {
    internal = 2376
    external = 2376
  }

  ports {
    internal = 3000
    external = 3000
  }

  ports {
    internal = 5000
    external = 5000
  }
}
```

- **`jenkins-docker` Container**:
  - Utiliza la imagen de Docker in Docker (`docker:dind`).
  - Se ejecuta en modo privilegiado para permitir la ejecución de Docker dentro del contenedor.
  - Se conecta a la red Docker definida por `docker_network.jenkins`.
  - Configuración de variables de entorno para Docker.
  - Configura volúmenes para certificados y datos de Jenkins.
  - Expone puertos 2376, 3000 y 5000.

#### Recurso `docker_container` para Jenkins-BlueOcean

```hcl
resource "docker_container" "jenkins-blueocean" {
  name  = "jenkins-blueocean"
  image = docker_image.jenkins-blueocean.image_id

  network_mode = docker_network.jenkins.name

  env = [
    "DOCKER_HOST=tcp://docker:2376",
    "DOCKER_CERT_PATH=/certs/client",
    "DOCKER_TLS_VERIFY=1",
    "JAVA_OPTS=-Dhudson.plugins.git.GitSCM.ALLOW_LOCAL_CHECKOUT=true",
  ]

  volumes {
    volume_name = docker_volume.jenkins-docker-certs.name
    container_path = "/certs/client"
    read_only = true
  }

  volumes {
    volume_name    = docker_volume.jenkins-data.name
    container_path = "/var/jenkins_home"
  }
  
  volumes {
    volume_name    = docker_volume.homeDir.name
    host_path = "/home/gcrows/"
    container_path = "/home"
  }

  ports {
    internal = 8080
    external = 8080
  }

  ports {
    internal = 50000
    external = 50000
  }

  restart = "on-failure"
}
```

- **`jenkins-blueocean` Container**:
  - Utiliza la imagen personalizada de Jenkins con Blue Ocean (`myjenkins-blueocean:2.426.2-1`).
  - Se conecta a la misma red Docker (`docker_network.jenkins`).
  - Configuración de variables de entorno para la comunicación con el contenedor Docker (`jenkins-docker`).
  - Configura volúmenes para certificados, datos de Jenkins y un directorio de inicio personalizado.
  - Expone puertos 8080 y 50000.
  - Se reinicia automáticamente en caso de fallo.

### Dockerfile

```Dockerfile
FROM jenkins/jenkins:2.426.2-jdk17

USER root
RUN apt-get update && apt-get install -y lsb-release
RUN curl -fsSLo /usr/share/keyrings/docker-archive-keyring.asc \
  https://download.docker.com/linux/debian/gpg
RUN echo "deb [arch=$(dpkg --print-architecture) \
  signed-by=/usr/share/keyrings/docker-archive-keyring.asc] \
  https://download.docker.com/linux/debian \
  $(lsb_release -cs) stable" > /etc/apt/sources.list.d/docker.list
RUN apt-get update && apt-get install -y docker-ce-cli
USER jenkins
RUN jenkins-plugin-cli --plugins "blueocean:1.27.9 docker-workflow:572.v950f58993843"
# Crear network
# docker network create jenkins

# Construir la imagen de Jenkins
# docker build -t myjenkins-blueocean:2.426.2-1  .

# Ejecutar el contenedor de Jenkins
# docker run \
#   --name jenkins-blueocean \
#   --detach \
#   --network jenkins \
#   --env DOCKER_HOST=tcp://docker:2376 \
#   --env DOCKER_CERT_PATH=/certs/client \
#   --env DOCKER_TLS_VERIFY=1 \
#   --publish 8080:8080 \
#   --publish 50000:50000 \
#   --volume jenkins-data:/var/jenkins_home \
#   --volume jenkins-docker-certs:/certs/client:ro \
#   --volume "$HOME":/home \
#   --restart=on-failure \
#   --env JAVA_OPTS="-Dhudson.plugins.git.GitSCM.ALLOW_LOCAL_CHECKOUT=true" \
#   myjenkins-blueocean:2.426.2-1


# Ejecutar docker in a docker
# docker run \                                                                                                                                ✔  9s  
#   --name jenkins-docker \
#   --rm \
#   --detach \
#   --privileged \
#   --network jenkins \
#   --network-alias docker \
#   --env DOCKER_TLS_CERTDIR=/certs \
#   --volume jenkins-docker-certs:/certs/client \
#   --volume jenkins-data:/var/jenkins_home \
#   --publish 2376:2376 \
#   --publish 3000:3000 --publish 5000:5000 \
#   docker:dind \
#   --storage-driver overlay2
```

- **Dockerfile**:
  - La imagen se basa en `jenkins/jenkins:2.426.2-jdk17`.
  - Se cambia al usuario root para instalar dependencias necesarias y configurar Docker.
  - Se vuelve al usuario jenkins para instalar los plugins Blue Ocean y Docker Workflow.

### Comandos Docker (comentarios en el código)

Se proporcionan comentarios con los comandos de Docker para ejecutar el entorno:

- **Crear red y construir la imagen de Jenkins**.
- **Ejecutar el contenedor de Docker in Docker**.
- **Ejecutar el contenedor de Jenkins con Blue Ocean**.
