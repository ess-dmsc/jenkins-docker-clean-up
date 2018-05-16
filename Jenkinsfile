// Set periodic trigger at 4:56 every Sunday.
properties([
  pipelineTriggers([cron('56 4 * * 7')]),
])

def names = [
  'dmbuild01.dm.esss.dk',
  'dmbuild02.dm.esss.dk',
  'dmbuild03.dm.esss.dk'
]

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

      stage('List Docker Images') {
        sh 'docker images'
      }

      stage('Remove Docker Images') {
        sh 'docker rmi $(docker images --quiet) || true'
      }

      cleanWs()
    }
  }
}

parallel builders
