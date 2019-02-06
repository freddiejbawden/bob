INFO=/bin/echo -e "\x1b[32;01m[BOB]\x1b[0m" 
WARN=/bin/echo -e "\x1b[33;01m[BOB]\x1b[0m"
ERR=/bin/echo -e "\x1b[31;01m[BOB]\x1b[0m"
MAKE:=$(MAKE) --no-print-directory 
ifndef ENV
	ENV=dev
endif

run: start-mongo
ifeq ($(ENV),prod)
	@$(MAKE) start-server
else
	@$(MAKE) start-dev-server
endif


start-dev-server:
	@$(INFO) "Starting dev server"
	@cd server; npm dev

start-server:
	@$(INFO) "Starting server"
	@cd server; npm start

start-mongo:
	@$(INFO) "Starting mongodb"
	sudo service mongod start
	
install:
ifneq ($(shell id -u),0)
	$(error Make needs to be executed as root)
endif
	@$(MAKE) real-install
	@source /etc/environment || true
	@source ~/.bashrc || true
	@source ~/.bash_profile || true

real-install: install-node

install-mongo:
ifneq ($(service --status-all | grep -Fq 'mongod'), 0)
	@$(INFO) "Mongodb not found. Installing..."
	@# @apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 9DA31620334BD75D9DCB49F368818C72E52529D4
	@# @echo "deb [ arch=amd64 ] https://repo.mongodb.org/apt/ubuntu bionic/mongodb-org/4.0 multiverse" | tee /etc/apt/sources.list.d/mongodb-org-4.0.list
	@apt-get update
	@apt-get install -y mongodb
else
	@$(INFO) "Mongodb is already installed."
endif
	@$(MAKE) start-mongo

install-node:
ifeq (,$(shell which node))
	@$(INFO) "Node.js not found. Installing..."
	@curl -sL https://deb.nodesource.com/setup_11.x | bash -
	@apt-get install -y nodejs
else
	@$(INFO) "Node.js is already installed."
endif