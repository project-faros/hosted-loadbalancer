.PHONY : build _dockerfile publish clean clean_container clean_image run join start stop devel _devel_run

APPLICATION=hosted-loadbalancer
APP_VERS=$(shell date +%y.1%W.%u%H%M)
IMAGE=hosted-loadbalancer-operator
VERS=$(shell cat version.txt)
DEVDIR=$(shell pwd)
UPSTREAM=$(shell cat ../upstream.txt)
TOKEN=basic cm1rcmF1czpiITdDbTUmQ1kyQ0A2UGQ=

build:
	operator-sdk build --image-builder podman $(UPSTREAM)/$(IMAGE):$(VERS)

bundle:
	operator-sdk bundle create $(UPSTREAM)/$(APPLICATION):latest \
		--directory ./deploy/olm-catalog/$(VERS) \
		--package $(IMAGE) \
		--channels beta \
		--default-channel beta \
		--image-builder podman

publish:
	podman image tag $(UPSTREAM)/$(IMAGE):$(VERS) $(UPSTREAM)/$(IMAGE):latest
	podman push $(UPSTREAM)/$(IMAGE):$(VERS)
	podman push $(UPSTREAM)/$(IMAGE):latest

publish_bundle:
	operator-courier push ./deploy/olm-catalog/ faros $(APPLICATION) $(APP_VERS) "$(TOKEN)"

devel:
	operator-sdk run --local

test:
	operator-courier verify --ui_validate_io deploy/olm-catalog
