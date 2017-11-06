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
            cleanWs()

            stage('List Docker Images') {
                sh 'docker images'
            }

            stage('Remove Docker Images') {
                sh 'docker rmi $(docker images --quiet) || true'
            }
        }
    }
}

parallel builders
