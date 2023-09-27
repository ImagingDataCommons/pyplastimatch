# Ubuntu 22.04LTS Plastimatch Docker Container

This Docker container for Plastimatch was intended as a test of PyPlastimatch's installation utility functions, but since it could be useful to someone I'm sharing it here.

## Build the Docker Container

To build the Docker container, run the following commands from the root of the PyPlastimatch repository:

```
cd tests/dockerfiles/

docker build --tag pypla_22.04 .
```

## Run the Docker Container

Assuming the data you want to convert/manipulate with Plastimatch is stored at `/home/dennis/Desktop/sample_data/`, the Docker command to run will look like the following

```
docker run --rm -it --entrypoint bash -v /home/dennis/Desktop/sample_data/:/app/data pypla_22.04
```

This will mount the data directory to the container's `/app/data` directory, and you can then run Plastimatch commands from within the container. For example, if `/home/dennis/Desktop/sample_data/` is structured as follows:

```
(base) dennis@W2-S1:~$ tree /home/dennis/Desktop/sample_data/ -L 1
/home/dennis/Desktop/sample_data/
└── dicom
```

Then, once inside the container, you can run the following command to convert the DICOM files to a volume saved in the NRRD format:

```
cd /app/data

plastimatch convert --input input_dcm/ --output-img test.nrrd
```

