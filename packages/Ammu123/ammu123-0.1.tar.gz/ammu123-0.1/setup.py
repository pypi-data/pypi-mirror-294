from setuptools import setup, find_packages

setup(
    name="Ammu123",
    version="0.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "streamlit",
    ],
    entry_points={
        'console_scripts': [
            'run-streamlit-app=streamlit_app.a:main',
        ],
    },
)
