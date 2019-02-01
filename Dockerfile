# Start off generating our GRPC + proto library.
FROM znly/protoc:latest as build-proto
ARG proto_dir=protos/
RUN mkdir /code
WORKDIR /code

RUN apk add --no-cache build-base curl automake autoconf libtool git zlib-dev
RUN git clone https://github.com/Ryanb58/boiler-protorepo.git
WORKDIR /code/boiler-protorepo

RUN rm -rf ${proto_dir}
RUN mkdir ${proto_dir}

RUN /usr/bin/protoc --python_out=${proto_dir} -I . *.proto

RUN /usr/bin/protoc --plugin=protoc-gen-grpc=/usr/bin/grpc_python_plugin \
    --proto_path=. \
    --python_out=${proto_dir} \
	--grpc_out=${proto_dir} \
	-I ${proto_dir} *.proto

# Next we build the actual contents of the docker container that'll run.
FROM python:3.7

ADD . /code
WORKDIR /code
COPY --from=0 /code/boiler-protorepo/protos ./protos
RUN pip install -r requirements.txt

EXPOSE 80
CMD ["python","app.py"]