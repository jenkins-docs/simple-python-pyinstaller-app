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
# docker run \
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