@Library('ecdc-pipeline')
import ecdcpipeline.ImageRemover

// Set periodic trigger at 4:56 every day.
properties([
  pipelineTriggers([cron('56 4 * * *')]),
])

docker_nodes = nodesByLabel('docker')

imageRemover = new ImageRemover(this)

def builders = [:]
for (x in docker_nodes) {
  def name = x
  builders[name] = {
    node(name) {
      try {
        stage('Checkout') {
          checkout scm
        }

        stage('List Docker Containers') {
          sh 'docker ps --all'
        }

        stage('Stop containers running for more than 24 hours') {
          sh 'LC_ALL=en_US.utf-8 python3 stop_containers_running_for_too_long.py 24'
        }

        stage('Remove Docker Containers') {
          sh 'docker rm $(docker ps --all --quiet) || true'
        }

        stage('Remove Docker Images') {
          try {
            imageRemover.cleanImages()
          } catch(e) {
            echo 'Ignoring error'
          }
        }
      } finally {
        cleanWs()
      }
    }
  }
}

timeout(time: 1, unit: 'HOURS') {
  node('master') {
    parallel builders
  }
}
