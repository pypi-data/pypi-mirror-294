from setuptools import setup, find_packages

setup(
    name="en-mi-club-api",
    version="0.5.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=[
        'boto3',
        'email_validator',
        'fastapi',
        'fastapi-cli',
        'passlib',
        'psycopg2',
        'PyJWT',
        'pydantic==2.7.4',
        'pydantic_core==2.18.4',
        'pydantic-settings==2.3.3',
        'python-dateutil',
        'python-dotenv',
        'python-multipart',
        'rut_chile',
        'sqlalchemy',
        'uvicorn',
    ],
    author="Ingeniasoft",
    description="API entities for En Mi Club",
)
