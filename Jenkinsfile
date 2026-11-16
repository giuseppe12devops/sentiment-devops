pipeline {
    agent any

    // Jenkins controlla periodicamente se ci sono nuovi commit
    triggers {
        pollSCM('H/2 * * * *')
    }

    parameters {
        string(name: 'EMAIL_NOTIFICHE', defaultValue: '', description: 'Email per gli avvisi della pipeline')
    }

    stages {
        stage('Build') {
            steps {
                // Creo l'immagine Docker del servizio
                sh 'docker build -t sentiment-api:latest .'
            }
        }

        stage('Test') {
            steps {
                // Eseguo i test dentro al container
                sh 'docker run --rm sentiment-api:latest python -m pytest -q'
            }
        }

        stage('Deploy') {
            steps {
                // Aggiorno il servizio solo se i test sono passati
                sh 'docker compose up -d --no-deps --no-build --force-recreate app'
            }
        }
    }

    post {
        success {
            echo 'Build, test e deploy completati'
            script {
                def email = params.EMAIL_NOTIFICHE?.trim() ?: env.EMAIL_DESTINATARIO?.trim()
                if (email) {
                    mail to: email,   
                         subject: "OK - ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                         body: "La pipeline è terminata correttamente. ${env.BUILD_URL}"
                }
            }
        }
        failure {
            echo 'Pipeline fallita. Controlla i log di Jenkins.'
            script {
                def email = params.EMAIL_NOTIFICHE?.trim() ?: env.EMAIL_DESTINATARIO?.trim()
                if (email) {
                    mail to: email, 
                         subject: "ERRORE - ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                         body: "La pipeline è fallita. ${env.BUILD_URL}"
                }
            }
        }
    }
}
