MODULES = hostserver meta web backend cli

default: build

download:
	$(foreach module, $(MODULES), $(MAKE) -C $(module) download;)

build:
	$(foreach module, $(MODULES), $(MAKE) -C $(module) build;)

clean:
	$(foreach module, $(MODULES), $(MAKE) -C $(module) clean;)
