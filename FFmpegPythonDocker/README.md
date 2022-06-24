

```bash
CONTAINER_NAME=py3-ffmpeg
CONTAINER_REGISTRY_NAME=<replace with container name>

# Build and run image
docker build -t "lamrax:$CONTAINER_NAME" .
docker run -it lamrax:$CONTAINER_NAME

# Deploy to Container
$ az acr login --name $CONTAINER_REGISTRY_NAME
docker tag lamrax/$CONTAINER_NAME $CONTAINER_REGISTRY_NAME.azurecr.io/$CONTAINER_NAME
docker push $CONTAINER_REGISTRY_NAME.azurecr.io/$CONTAINER_NAME

# Check 
az acr repository list --name $CONTAINER_REGISTRY_NAME.azurecr.io/$CONTAINER_NAME --output table
```