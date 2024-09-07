from setuptools import setup, find_packages

setup(
    name='jlm_echo_plugin',
    version='0.1',
    packages=find_packages(),
    entry_points={
        'llm.models': [
            'jecho = jecho_model:JEchoModel',
        ],
    },
    install_requires=['llm', 'tlid'],
)