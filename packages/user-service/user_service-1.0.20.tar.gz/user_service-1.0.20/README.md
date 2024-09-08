step 1:- clone the project.

step 2:- Make sure Docker, minikube, kubectl are in place.

step3:- run docker build -t <service-name> <service-dir>. It will build the image 

step 4:- You can see using docker images.

step 5:- Once image is created, tag it and push it to Docker Hub.
docker tag movie-service-image divyajyotidas15/movie-service-image:1.0.0.0
docker push divyajyotidas15/movie-service-image:1.0.0.0

step 6:- Deploy it on local minikube. This will start minikube k8s cluster locally for Devlopment.
minikube start
minikube tunnel

step 7:- create k8s deployments object for each service.
 kubectl apply -f movie-service/k8s/

step 8:- Expose deployment object
 kubectl expose deployment movie --type=LoadBalancer --port=8775

