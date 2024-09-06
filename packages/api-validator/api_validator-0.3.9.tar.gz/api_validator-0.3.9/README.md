# API Validator

CLI Tool that validates an OpenAPI specification against a live application using [Newman](https://github.com/postmanlabs/newman). Optionally generates the OpenAPI spec from code using [NightVision](https://www.nightvision.net/).

## Installation

```bash
# pipx is recommended for installing CLI tools
pip install pipx
pipx install api-validator

# Or install it with pip
pip3 install api-validator --user
```

You'll also have to install some prerequisites that `api-validator` wraps around. Namely:
- [NightVision CLI](https://docs.nightvision.net/docs/installing-the-cli)
- [Newman](https://github.com/postmanlabs/newman)
- [postman-to-openapi](https://www.npmjs.com/package/postman-to-openapi)
- [oasdiff](https://github.com/Tufin/oasdiff)
- [GitHub CLI](https://cli.github.com/manual/)
- [Semgrep](https://github.com/semgrep/semgrep) (currently required for API discovery on Java only; migrating soon)

* You can do that quickly by running this command:

```bash
# Install some prerequisites 
api-validator install
```

If that doesn't work, you can run these:

```bash
brew install tufin/tufin/oasdiff
brew install gh
brew install nvsecurity/taps/nightvision
brew install newman  # or npm install -g newman
brew install semgrep

npm install postman-to-openapi -g
```

* We manage the config for this tool in a config file. We've bundled it into the distribution. You can create the config file like this:

```bash
api-validator create-config-file -o config.yml
```

* Now you can list the various jobs that are available:

```bash
# Note: api-validator will look for the config file in the current directory. You can specify a different location with the -c flag.
# Example: api-validator list-jobs -c custom-config.yml

# List all jobs
api-validator list-jobs -c config.yml
# Only list Python jobs
api-validator list-jobs --language python
```


It will print out the available jobs in the config file, like this:

<details open>
<summary>Jobs listing</summary>
<br>

```
Language: dotnet, Job Name: altinn-studio, Repo: https://github.com/Altinn/altinn-studio
Language: dotnet, Job Name: bitwarder-server, Repo: https://github.com/bitwarden/server
Language: dotnet, Job Name: dotnet-kavita, Repo: https://github.com/Kareadita/Kavita
Language: dotnet, Job Name: dvcsharp-api, Repo: https://github.com/appsecco/dvcsharp-api
Language: dotnet, Job Name: edwinvw-pitstop-customers, Repo: https://github.com/EdwinVW/pitstop
Language: dotnet, Job Name: edwinvw-pitstop-vehicles, Repo: https://github.com/EdwinVW/pitstop
Language: dotnet, Job Name: edwinvw-pitstop-workshop, Repo: https://github.com/EdwinVW/pitstop
Language: dotnet, Job Name: eshop-catalog-api, Repo: https://github.com/api-extraction-examples/eShop
Language: dotnet, Job Name: eshop-ordering-api, Repo: https://github.com/api-extraction-examples/eShop
Language: dotnet, Job Name: eshop-webhooks-api, Repo: https://github.com/api-extraction-examples/eShop
Language: dotnet, Job Name: featbit, Repo: https://github.com/featbit/featbit
Language: dotnet, Job Name: jellyfin, Repo: https://github.com/NightVisionExamples/jellyfin
Language: dotnet, Job Name: universalis, Repo: https://github.com/Universalis-FFXIV/Universalis
Language: dotnet, Job Name: wallet-wasabi, Repo: https://github.com/zkSNACKs/WalletWasabi
Language: go, Job Name: crAPI-go, Repo: https://github.com/vulnerable-apps/crAPI
Language: js, Job Name: blockchain-explorer, Repo: https://github.com/api-extraction-examples/blockchain-explorer
Language: js, Job Name: cve-services, Repo: https://github.com/api-extraction-examples/cve-services
Language: js, Job Name: dvws-node, Repo: https://github.com/vulnerable-apps/dvws-node
Language: js, Job Name: express-anything-llm, Repo: https://github.com/api-extraction-examples/anything-llm
Language: js, Job Name: express-rest-boilerplate, Repo: https://github.com/dnighvn/express-rest-boilerplate
Language: js, Job Name: hypertube, Repo: https://github.com/api-extraction-examples/Hypertube
Language: js, Job Name: infisicial, Repo: https://github.com/api-extraction-examples/infisical
Language: js, Job Name: juice-shop, Repo: https://github.com/vulnerable-apps/juice-shop
Language: js, Job Name: kubero, Repo: https://github.com/api-extraction-examples/kubero
Language: js, Job Name: nodejs-api-showcase, Repo: https://github.com/api-extraction-examples/nodejs-api-showcase
Language: js, Job Name: nodejs-goof, Repo: https://github.com/vulnerable-apps/nodejs-goof
Language: js, Job Name: valetudo, Repo: https://github.com/api-extraction-examples/Valetudo
Language: python, Job Name: Inventree-django, Repo: https://github.com/api-extraction-examples/InvenTree
Language: python, Job Name: a-flaskrestful-api, Repo: https://github.com/api-extraction-examples/a-flaskrestful-api
Language: python, Job Name: argus-eye-django, Repo: https://github.com/api-extraction-examples/Eye
Language: python, Job Name: cert-viewer-flask, Repo: https://github.com/blockchain-certificates/cert-viewer
Language: python, Job Name: cpa-network-django, Repo: https://github.com/api-extraction-examples/cpa-network
Language: python, Job Name: crAPI-python, Repo: https://github.com/vulnerable-apps/crAPI
Language: python, Job Name: defect-dojo-django, Repo: https://github.com/api-extraction-examples/django-DefectDojo
Language: python, Job Name: django-crm, Repo: https://github.com/api-extraction-examples/Django-CRM
Language: python, Job Name: greater-wms-django, Repo: https://github.com/api-extraction-examples/GreaterWMS
Language: python, Job Name: help-desk-service-django, Repo: https://github.com/api-extraction-examples/help-desk-service
Language: python, Job Name: intelowl-django, Repo: https://github.com/api-extraction-examples/IntelOwl
Language: python, Job Name: karrio-django, Repo: https://github.com/api-extraction-examples/karrio
Language: python, Job Name: librephotos-django, Repo: https://github.com/api-extraction-examples/librephotos
Language: python, Job Name: libretime-django, Repo: https://github.com/api-extraction-examples/libretime
Language: python, Job Name: mathesar-django, Repo: https://github.com/api-extraction-examples/mathesar
Language: python, Job Name: medileaf-backend, Repo: https://github.com/api-extraction-examples/MediLeaf_backend
Language: python, Job Name: netbox-django, Repo: https://github.com/api-extraction-examples/netbox
Language: python, Job Name: nimbler-django, Repo: https://github.com/NimblerSecurity/nimbler-django
Language: python, Job Name: posthog-django, Repo: https://github.com/api-extraction-examples/posthog
Language: python, Job Name: wger-django, Repo: https://github.com/api-extraction-examples/wger
Language: spring, Job Name: Alibaba-Nacos, Repo: https://github.com/api-extraction-examples/nacos
Language: spring, Job Name: Angular-SpringBoot-REST-JWT, Repo: https://github.com/mrin9/Angular-SpringBoot-REST-JWT
Language: spring, Job Name: Netflix-Conductor, Repo: https://github.com/api-extraction-examples/conductor
Language: spring, Job Name: Newbee-Mall, Repo: https://github.com/api-extraction-examples/newbee-mall
Language: spring, Job Name: Spring-boot-Banking, Repo: https://github.com/api-extraction-examples/Spring-boot-Banking
Language: spring, Job Name: ZHENFENG13-My-Blog, Repo: https://github.com/api-extraction-examples/ZHENFENG13-My-Blog
Language: spring, Job Name: apereo-cas, Repo: https://github.com/api-extraction-examples/cas
Language: spring, Job Name: crAPI-spring, Repo: https://github.com/vulnerable-apps/crAPI
Language: spring, Job Name: javaspringvulny, Repo: https://github.com/vulnerable-apps/javaspringvulny
Language: spring, Job Name: thingsboard, Repo: https://github.com/api-extraction-examples/thingsboard
```

</details>


### Mode 1: Comparing API Discovery to existing OpenAPI Specs

You can compare NightVision's API Discovery results to existing OpenAPI specs, based on the content of the config file. This is useful for grading the effectiveness of the API Discovery tool.

You can run these comparisons at different scopes:
1. Select job by job name
2. Bulk select jobs, filtered by language
3. Bulk select all jobs

* Run a comparison for a single job:

```bash
api-validator compare \
    --config-file config.yml \
    --job juice-shop \
    --output-file comparison-juice-shop.md
```

* Run a comparison for a single job:

```bash
api-validator compare \
    --config-file config.yml \
    --job juice-shop \
    --output-file comparison-juice-shop.md
```

The output will look like this:

<details open>
<summary>Juice Shop output</summary>

```
Thread 0 will process cloning for jobs: juice-shop
	juice-shop/juice-shop: Cloning...
	juice-shop/juice-shop: Local repo already exists. Skipping clone.
juice-shop/juice-shop: Thread 0 progress: Repository cloned for: juice-shop
Thread 0 will process extraction for jobs: juice-shop
	juice-shop/juice-shop: Working on Job: juice-shop
	juice-shop/juice-shop: Repo: https://github.com/juice-shop/juice-shop, Swagger File: https://raw.githubusercontent.com/api-extraction-examples/juice-shop/master/swagger.yml, Language: js
	juice-shop/juice-shop: Downloading base Swagger file...
	juice-shop/juice-shop: Data downloaded from https://raw.githubusercontent.com/api-extraction-examples/juice-shop/master/swagger.yml and saved as /Users/kinnaird/github.com/nvsecurity/api-validator/analysis/base/juice-shop.yml
	juice-shop/juice-shop: Running extraction...
		juice-shop/juice-shop: Running command: api-excavator --log-level info --output /Users/kinnaird/github.com/nvsecurity/api-validator/analysis/revision/juice-shop.yml -l js /Users/kinnaird/github.com/nvsecurity/api-validator/analysis/repos/juice-shop
		juice-shop/juice-shop: INFO Initializing language provider
		juice-shop/juice-shop: INFO Finished initializing language provider
		juice-shop/juice-shop: INFO Starting language provider execution
		juice-shop/juice-shop: INFO Finished language provider execution
		juice-shop/juice-shop: INFO Starting generating OpenAPI document
		juice-shop/juice-shop: INFO OpenAPI document generated in 653.800208ms
		juice-shop/juice-shop: Number of discovered paths: 87
		juice-shop/juice-shop: Number of discovered classes: 0
		juice-shop/juice-shop: INFO Generated the OpenAPI document.
		juice-shop/juice-shop: INFO Successfully validated the output.
	juice-shop/juice-shop: Performing OASDiff operation...
	Running oasdiff command:
		oasdiff diff /Users/kinnaird/github.com/nvsecurity/api-validator/analysis/base/juice-shop.yml /Users/kinnaird/github.com/nvsecurity/api-validator/analysis/revision/juice-shop.yml --exclude-elements description,examples,title,summary
	juice-shop/juice-shop: Completed work on Job: juice-shop

juice-shop/juice-shop: Thread 0 progress: Completed: juice-shop
Thread 0 final status: Completed: juice-shop
All threads completed.
Saved comparison-juice-shop.md
```

<br>

</details>

* Run a comparison for Python apps:

```bash
api-validator compare \
    --config-file config.yml \
    --language python \
    --output-file comparison-python.md
```

* Run a comparison for all jobs:

```bash
api-validator compare \
    --config-file config.yml \
    --all \
    --output-file comparison-all.md
```

## Mode 2: Validating OpenAPI specs based on traffic

We took another route to validating our OpenAPI specs - testing the OpenAPI spec against live applications.

We use [Newman](https://github.com/postmanlabs/newman) to confirm that each of the URL paths and HTTP methods are valid. It's not a perfect evaluation system, but it's a solid data point of the effectiveness.

Assumptions:
* **Valid endpoints**: For instance, if the endpoint responds with HTTP 200, we assume it is valid. Also, if it responds with `401 Unauthorized` or `403 Forbidden`, we assume it is valid because it is a valid endpoint, but we do not have access to it. With `400 Bad Request`, we assume it is valid because the request body was not formatted correctly. We do not attempt to format the request body to match the API spec.
* **Invalid endpoints**: If the endpoint responds with HTTP `404 Not Found`, we assume it is invalid. If it responds with `405 Method Not Allowed`, we treated as invalid because the generated API spec was incorrect about that method. For `500 Internal Server Error`, this might be a valid endpoint but there is not a way to tell for sure without testing it manually.

In the case of Juice Shop, you can see that out of the **97** endpoints were discovered, of which **79** were valid and **18** were invalid/hallucinated. This gives us a success rate of **74.53%**.

Here's an example of how to run the traffic validation:

* Now run an example app with Docker:

```bash
docker run --restart always -d -p 3000:3000 --name juice-shop bkimminich/juice-shop
```

* Now run the validator to test the API and generate a markdown-formatted report:

```bash
api-validator yolo-traffic \
    --config-file config.yml \
    --swagger-file juice-shop.yml \
    --server http://localhost:3000 \
    --app-name juice-shop
```

It will generate a file called `./summary.md`. 

## Config File

The config file is a YAML file that contains details about the applications you are scanning. For example, you might want to skip certain endpoints that are destructive or that you don't want to test. You should also specify the  repository URL and language of the application; that information is used in the generated Markdown report, but it's not the end of the world if you don't include it.

Here is an example:

```yaml
apps:
  nodejs-goof:
    repo: 'https://github.com/vulnerable-apps/nodejs-goof'
    language: js
    github_stars: 485
    provided_swagger_file: ""
    skip_endpoints:
    - path: '/destroy/:id'
      method: GET
      description: Destroy an endpoint
  juice-shop:
    repo: 'https://github.com/vulnerable-apps/juice-shop'
    language: js
    provided_swagger_file: "https://raw.githubusercontent.com/api-extraction-examples/juice-shop/master/swagger.yml"
    github_stars: 8900
    skip_endpoints:
      - path: '/file-upload'
        method: POST
        description: Upload a file
      - path: '/profile/image/file'
        method: POST
        description: Upload a file
```

We've provided the default config file in the distribution, which you can generate with `api-validator create-config-file -o config.yml`. 
