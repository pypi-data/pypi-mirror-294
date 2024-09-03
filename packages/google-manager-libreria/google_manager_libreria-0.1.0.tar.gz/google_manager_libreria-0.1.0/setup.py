from setuptools import setup, find_packages

setup(
    name="google_manager_libreria",
    version="0.1.0",
    description="manejo del paquete google mails,hojas de calculodrive ",
    author="Jose parodi",
    author_email="developers@consultoraparodi.com.ar",
    packages=find_packages(),
    install_requires=["requests"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.12',
)
