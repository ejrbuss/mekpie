from functools import wraps

config_layer = 0

def cli_config(name):
    def cli_config_decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            global config_layer
            tell(f'Configuring {name}...')
            config_layer += 1
            result = fn(*args, **kwargs)
            config_layer -= 1
            tell(f'{name} configured!')
            return result
        return wrapper
    return cli_config_decorator

def tell(message):
    header  = '>' * config_layer
    message = message.strip().replace('\n', f'\n{header} ')
    print(f'{header} {message}')

def ask(prompt, default=None, options=None, validator=None):
    message, error = prompt
    while True:
        header = '>' * config_layer
        footer = ': ' if default is None else f' (default `{default}`): '
        value = input(f'{header} {message}{footer}')
        if value == '' and default:
            value = default
        if ((options and value in options)
            or (validator and validator(value))
            or (not validator and not options)
        ):
            tell(f'Selected `{value}`.')
            return value
        tell(error.format(value))