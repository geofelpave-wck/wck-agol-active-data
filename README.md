# functions-framework-example

Example functions framework template with multiple routes supported.

* I can make this into a CLI template with cookiecutter, if we all agree to finalize this.

---;

Running:

```bash
# Run locally within functions-framework
functions-framework --target=run --port=8080 

# Test healthcheck endpoint 
curl -v --get http://localhost:8080/healthcheck

# Test the echo endpoint
curl --header "Content-Type: application/json" \
  --request POST \
  --data '{"username":"alex","password":"banamania"}' \
  http://localhost:8080/echo

# Running from deployed cloud function: 
curl -X POST <url-to-cloud-function>/echo -H "Content-Type: application/json" -d '{"foo": "bar"}
```

Deployment:

```bash
make deploy
```

Required env vars (`_local/.env`):

```bash
# Deployment 
GCP_PROJECT_ID=""
GCP_REGION=""
```

## How to use

```bash

## Setup local repo
git clone <url/to/repo>.git <name of your new function repo>
cd <name of your new function repo>
rm -rf .git 
git init 
git add .
git commit -m 'initial commit'

## Setup local python env, e.g. uv -- not necessary, but great 
uv sync 

## Run debug server 
functions-framework --target=run --port=8080 --debug 

## Modify the @app.route functions in main as needed 
vim main.py 

# ...

## Test as desired 

# ...

# When done, commit changes and push 
git add . 
git commit -m 'foo'
git push origin main 

# Re-deploy (CI/CD pending)
# If you're not authenticated, first: 
    # gcloud auth login
make deploy  

# You're done!
```
