pipeline {
    environment { 
        registryCredential = 'docker-hub-credentials'
    }
  agent any
  
   tools {
        nodejs "node"
    }
    
  stages {
  
    stage('Build') {
      steps {
        sh  'docker build -t milelucero98/result:latest ./result'
        sh 'docker build -t milelucero98/vote:latest ./vote'
        sh 'docker build -t milelucero98/worker:latest ./worker'
      }
    }
    
    stage('Prepare') {
            steps{
                sh script:'''
                  #!/bin/bash
                  cd ./it
                  npm install
                '''
            }
        }
    
    stage('Test') {
            steps {
                sh script:'''
                  #!/bin/bash
                  docker-compose -d up
                  sleep 7
                  cd ./it
                  npx codeceptjs run --steps --reporter mocha-multi
                '''
            }
            
            post {
                success {
                    junit '**/output/*.xml'
                }
            }
        }
        
        stage('Deploy') {
            steps {
                withCredentials([usernamePassword( credentialsId: 'docker-hub-credentials', usernameVariable: 'USERNAME', passwordVariable: 'PASSWORD')]) {
                    script {
                        docker.withRegistry('', 'docker-hub-credentials') {
                            sh "docker login -u ${USERNAME} -p ${PASSWORD}"
                            sh "docker push $registry:$BUILD_ID"
                        }   
                    }
                }   
            }
        }
  }
}


