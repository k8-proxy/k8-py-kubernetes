FROM public.ecr.aws/lambda/python:3.8

COPY --from=build-image /usr/local/c-icap/bin/c-icap-client /usr/local/c-icap/bin/c-icap-client

RUN yum install -y git automake make gcc libtool

RUN git clone https://github.com/filetrust/c-icap.git /src
WORKDIR /src/c-icap
RUN autoreconf -ivf \
    && ./configure --prefix=/usr/local/c-icap \
    && make; make install

RUN pip install python-dotenv

RUN git clone https://github.com/owasp-sbot/OSBot-Utils.git
RUN cp -R ./OSBot-Utils/osbot_utils ${LAMBDA_TASK_ROOT}/osbot_utils

# Copy function code
COPY app.py ${LAMBDA_TASK_ROOT}

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "app.run" ]