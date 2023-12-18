terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0.1"
    }
  }
}

provider "docker" {}

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



resource "docker_image" "docker_dind" {
  name         = "docker:dind"
  keep_locally = false
}

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


resource "docker_image" "jenkins-blueocean" {
  name = "myjenkins-blueocean:2.426.2-1"
  build {
    context = "./"
    dockerfile = "Dockerfile"
  }
}


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