FROM public.ecr.aws/lambda/python:3.9

RUN pip install numpy==1.19.4 matplotlib==3.3.3

# Copy function code
COPY app.py ${LAMBDA_TASK_ROOT}

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "app.handler" ]