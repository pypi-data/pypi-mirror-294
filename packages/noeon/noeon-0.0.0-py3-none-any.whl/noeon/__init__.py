from pkgutil import extend_path

# https://peps.python.org/pep-0420/#namespace-packages-today
__path__ = extend_path(__path__, __name__)
