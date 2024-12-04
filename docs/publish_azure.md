# With Github Education Program

This is how I did it and a personal documentation than the right way to do it.

1. Connect you Github Account with [Link](https://education.github.com/pack/redeem/microsoft-azure-student) from the Education page.
2. Install Azure CLI tool on your System.

## Login via Azure CLI

Run following command to authenticate against azure:

```bash
az login --allow-no-subscriptions
```

I've tried without `--allow-no-subscriptions` but it doesn't worked out.
For future logins I could drop the flag.

## Find Azure Location

With following command you are able to find your nearest azure instance:

```bash
az account list-locations
```

I have selected `germanywestcentral`.

## Create Resource Group

We first need a named resource group. I decided to name it `semVerCheck`.

```bash
az group create --name semVerCheck --location germanywestcentral
```

## Create Azure Container Registry

We need also a registry where we can upload our image to.
Dockerhub might also be possible, but I remained with azure.
The name of the registry needs to be unique, since the registry will be deployed as subdomain of azurecr.io.
I have used `semverreg` deploy it under the `semVerCheck` resource group.

```bash
az acr create --resource-group semVerCheck --name semverreg --sku basic
```

## Push the Container Image

Next we need to tag our docker image and push it to our fresh create registry.

```bash
docker tag semver-flask-app:latest semverreg.azurecr.io/semver-flask-app:latest
docker push semverreg.azurecr.io/semver-flask-app:latest
```

Here I am unsure about how I dumped my system with information and data that I tend to have only temporary.

## Create Docker Container

First we need to login to acr and gather the auth data.

```bash
az acr login --name semverreg
AZUSERNAME=$(az acr credential show --name semverreg --query username --output tsv)
AZPW=$(az acr credential show --name semverreg --query passwords[0].value --output tsv)
```

Now we are able to create the container

```bash
az container create \
    --resource-group semVerCheck \
    --name semver-flask-app \
    --image semverreg.azurecr.io/semver-flask-app:latest \
    --cpu 1 --memory 1.5 \
    --ports 8000 \
    --dns-name-label semver-check \
    --registry-login-server semverreg.azurecr.io \
    --registry-username $AZUSERNAME \
    --registry-password $AZPW
```

It will take sometime until the dns name is active.

## Test it

### Status of Container

```bash
az container show \
    --resource-group semVerCheck \
    --name semver-flask-app \
    --query instanceView.state \
    --out table
```

or

```bash
az container show \
    --resource-group semVerCheck \
    --name semver-flask-app \
    --query "{FQDN:ipAddress.fqdn,ProvisioningState:provisioningState}" \
    --out table
```

### All information

```bash
az container show \
    --resource-group semVerCheck \
    --name semver-flask-app \
    --out table
```
