from decouple import Config, RepositoryEnv


def useConfig(config):
    configurations = {
        'local': 'backend/.env.local',
        'test': 'backend/.env.test'
    }

    if config not in configurations:
        raise Exception(f"'{config}' is not a valid configuration.")

    config_path = configurations[config]
    return Config(RepositoryEnv(config_path))
