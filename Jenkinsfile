// Set periodic trigger at 4:56 every Sunday.
properties([
    pipelineTriggers([cron('56 4 * * 7')]),
])

def nodes = [
    'dmbuild01.dm.esss.dk',
    'dmbuild02.dm.esss.dk',
    'dmbuild03.dm.esss.dk'
]

def builders = [:]
for (x in nodes) {
    def node = x
    builders[node] = {
        node(node) {
            cleanWs()

            stage('Remove Docker Images') {
                sh 'docker rmi $(docker images --quiet) || true'
            }
        }
    }
}

parallel builders
