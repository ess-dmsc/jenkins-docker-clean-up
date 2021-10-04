@Library('ecdc-pipeline')
import ecdcpipeline.ImageRemover

// Set periodic trigger at 4:56 every day.
properties([
  pipelineTriggers([cron('56 4 * * *')]),
])

docker_nodes = nodesByLabel('docker')
systest_nodes = nodesByLabel('system-test')
names = docker_nodes + systest_nodes

imageRemover = new ImageRemover(this)

def builders = [:]
for (x in names) {
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
          sh 'python stop_containers_running_for_too_long.py 24'
        }

        stage('Remove Docker Containers') {
          sh 'docker rm $(docker ps --all --quiet) || true'
        }

        stage('Remove Docker Images') {
          imageRemover.cleanImages()
        }
      } finally {
        cleanWs()
      }
    }
  }
}

itest_nodes = nodesByLabel('integration-test')
for (x in itest_nodes) {
  def name = x
  builders[name] = {
    node(itestnode) {
      try {
        stage('List Docker Containers') {
          sh 'docker ps --all'
        }

        stage('Remove Docker Containers') {
          sh 'docker rm $(docker ps --all --quiet) || true'
        }

        stage('Remove Docker Images') {
          imageRemover.cleanImages()
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
