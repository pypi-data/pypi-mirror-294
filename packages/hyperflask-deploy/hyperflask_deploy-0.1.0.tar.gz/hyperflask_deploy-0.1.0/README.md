# Hyperflask-Deploy

**⚠️ This is a work in progress project which is not functionnal yet**

The infrastructure needed to independently host your Hyperflask projects.

This repository contains resources and scripts to create and manage servers to run containerized Hyperflask apps. The infrastructure is kept as simple and straighforward as possible with minimal operations needed.

This setup is meant to deploy apps on a single server. This stack can be run on cheap machines or VMs from any server/cloud providers.

 - Fully Open-Source stack that is 100% self-hostable if desired
 - Configure them using [Ansible](https://www.ansible.com/)
 - Use [Kamal](https://kamal-deploy.org/) to deploy using [Docker](https://www.docker.com/)
 - Hardened host machines
 - Full monitoring & observability using [OpenTelemetry Collector](https://opentelemetry.io/docs/collector/)
 - [Valkey](https://valkey.io/) for in-memory storage and queues
 - Privacy minded (GDPR compliant)

Note: Hyperflask-Deploy is pre-installed when using the [Hyperflask-Start template](https://github.com/hyperflask/hyperflask-start).

## Usage

Add to your hyperflask projects:

    pip install hyperflask-deploy

This will add the `deploy` command:

    hyperflask deploy