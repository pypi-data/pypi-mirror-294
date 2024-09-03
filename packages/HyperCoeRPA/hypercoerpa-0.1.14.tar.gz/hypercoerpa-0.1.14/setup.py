from setuptools import setup

with open("README.md", "r") as arq:
    readme = arq.read()

setup(name='HyperCoeRPA',
    version='0.1.14',
    license='MIT License',
    author='Joao Buso',
    long_description=open('README.md', 'r', encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    author_email='joao.buso@gmail.com',
    keywords='rpa hypercoe log tria software',
    description=u'Repositorio para a utilização da API de Log do HyperCoe',
    packages=['HyperCoeRPA'],
    package_dir={"": "."},  # Indica que os pacotes estão na raiz
    include_package_data=True, 
    install_requires=['requests'])