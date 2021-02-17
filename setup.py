import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open('requirements.txt') as f:
    required = f.read().splitlines()

    
setuptools.setup(
    name="medrical", 
    version="0.1.1",
    author="Dimitris Prasakis",
    author_email="dimitris@prasakis.com",
    description="Medrical is a real-time medical biometric monitoring system, powered by Apache Kafka and postgreSQL.",
    include_package_data = True,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DimitrisPr/medrical",
    packages=setuptools.find_packages(),
    install_requires=required,
    entry_points={
        'console_scripts': [
            'medrical = medrical.cli.cli:medrical',
            'medrical-configure = medrical.config.config:configure'
        ],
    }
)


