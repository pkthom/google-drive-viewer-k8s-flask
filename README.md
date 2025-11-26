# google-drive-viewer-k8s-flask

## Requirement

- DockerHub account
- k8s cluster with an ingress nginx controller
- A machie with docker & kubectl & helm installed
- A domain to deploy this
- Google spreadsheet to desplay

## 1. Replace some variables

Replace these with yours

- test/values.yaml
```
image:
  repository: yourusername/yourimage
  # This sets the pull policy for images.
  pullPolicy: IfNotPresent
  # Overrides the image tag whose default is the chart appVersion.
  tag: "yourtag"
```
```
ingress:
  enabled: true
  className: "nginx"
  annotations: {}
    # kubernetes.io/ingress.class: nginx
    # kubernetes.io/tls-acme: "true"
  hosts:
    - host: yourdomain
```
- test/templates/deployment.yaml
```
          env:
            - name: EXCEL_URL
              value: "https://docs.google.com/spreadsheets/d/id/export?format=xlsx"
```

## 2. Build an image and push 

```
docker login
docker build -t yourusername/yourimage:yourtag .
docker push yourusername/yourimage:yourtag 
```

## 3. Deploy Helm chart

```
kubectl create namespace test
helm install test ./test -n test
```

## 4. Test 

```
kubectl get pods -n test
```
You should see smt like this:
```
NAME                    READY   STATUS    RESTARTS   AGE
test-569665985b-g2922   1/1     Running   0          13s
```

Access https://yourdomain 
