@Library('ecdc-pipeline')
import ecdcpipeline.ImageRemover

// Set periodic trigger at 4:56 every day.
properties([
  pipelineTriggers([cron('56 4 * * *')]),
])

def names = [
  'dmbuild01.dm.esss.dk',
  'dmbuild02.dm.esss.dk',
  'dmbuild05.dm.esss.dk',
  'dmbuild06.dm.esss.dk',
  'dmbuild07.dm.esss.dk',
  'dmbuild08.dm.esss.dk',
  'dmbuild09.dm.esss.dk',
  'dmbuild10.dm.esss.dk',
  'dmbuild11.dm.esss.dk',
  // 'dmbuild20.dm.esss.dk',
  'dmbuild21.dm.esss.dk',
  'dmbuild22.dm.esss.dk',
  'dmbuild23.dm.esss.dk',
  'dmbuild24.dm.esss.dk',
  'dmbuild25.dm.esss.dk',
  'dmbuild26.dm.esss.dk',
  'systest01.dm.esss.dk',
  'systest02.dm.esss.dk'
]

imageRemover = new ImageRemover(this)

def builders = [:]
for (x in names) {
  def name = x
  builders[name] = {
    node(name) {
      checkout scm

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

      cleanWs()
    }
  }
}

itestnode = 'itestjenkins01.dm.esss.dk'
builders[itestnode] = {
  node(itestnode) {
    stage('List Docker Containers') {
      sh 'docker ps --all'
    }

    stage('Remove Docker Containers') {
      sh 'docker rm $(docker ps --all --quiet) || true'
    }

    stage('Remove Docker Images') {
      imageRemover.cleanImages()
    }

    cleanWs()
  }
}

timeout(time: 1, unit: 'HOURS') {
  parallel builders
}
