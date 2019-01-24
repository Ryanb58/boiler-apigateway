build:
	docker build --tag=apigateway .

tag:
	docker tag apigateway:latest ryanb58/boiler-apigateway:latest

push:
	docker push ryanb58/boiler-apigateway:latest

run:
	docker run -it -p 80:80 apigateway

run-local:
	docker run -it -p 80:80 ryanb58/apigateway:latest