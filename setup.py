import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    version                       = "0.3.1"               , # change this on every release
    name                          = "k8_kubernetes"  ,
    author                        = "Dinis Cruz",
    author_email                  = "dcruz@glasswallsolutions.com",
    description                   = "Glasswall - K8 Kubernetes helper methods",
    long_description              = long_description,
    long_description_content_type = "text/markdown",
    url                           = "https://github.com/k8-proxy/k8-kubectl.git",
    packages                      = setuptools.find_packages(),
    classifiers                   = [ "Programming Language :: Python :: 3"   ,
                                      "License :: OSI Approved :: MIT License",
                                      "Operating System :: OS Independent"   ])
