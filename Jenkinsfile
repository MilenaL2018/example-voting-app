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
                  sleep 10
                  cd ./ut
                  npx codeceptjs run --steps --reporter mocha-multi
                '''
            }
            
            post {
                success {
                    junit '**/output/*.xml'
                }
            }
        }
        
    stage('Static code analisis') {
            steps {
                sh 'mvn sonar:sonar -Dsonar.projectKey=AgusVelez5_spring-boot-app -Dsonar.organization=agusvelez5 -Dsonar.host.url=https://sonarcloud.io -Dsonar.login=b378dbfb4258b2712dd3dc78052400611207bd8a  -Dmaven.test.failure.ignore=true -Dsonar.scanner.force-deprecated-java-version=truenode'
            }
    }
        
    stage('Push image') {
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


