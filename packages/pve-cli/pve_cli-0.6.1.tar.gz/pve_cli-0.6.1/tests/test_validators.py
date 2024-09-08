import pytest
from typer import BadParameter

from pve_cli.util.exceptions import InvalidConfigError
from pve_cli.util.validators import cluster_validate, config_validate


class TestValidateConfig:
    def test_valid_config(self, valid_config: dict):
        try:
            config_validate(valid_config)
        except Exception as exc:
            pytest.fail(f'validate_config raised exception {exc}')

    def test_invalid_default_cluster(self):
        config = {
            'defaults': {'cluster': 'invalid'},
            'clusters': {
                'examplecluster': {
                    'host': 'examplehost',
                    'user': 'root',
                    'realm': 'foo',
                    'token_name': 'test',
                    'token_secret': 'PSSST!',
                }
            },
        }
        with pytest.raises(InvalidConfigError):
            config_validate(config)

    def test_missing_cluster_key(self):
        config = {
            'defaults': {'cluster': 'examplecluster'},
            'clusters': {
                'examplecluster': {'host': 'examplehost', 'user': 'root', 'token_name': 'test', 'token_secret': 'PSSST!'},
                'second_cluster': {'host': 'host2', 'token_name': 'test', 'token_secret': 'PSSST!'},
            },
        }

        with pytest.raises(InvalidConfigError) as exc:
            config_validate(config)

        assert 'examplecluster: realm' in str(exc.value)
        assert 'second_cluster: user, realm' in str(exc.value)


class TestValidateCluster:
    def test_valid_cluster(self, valid_config: dict):
        try:
            cluster_validate(valid_config, 'examplecluster')
        except Exception as exc:
            pytest.fail(f'validate_cluster raised exception {exc}')

    def test_invalid_cluster(self, valid_config: dict):
        with pytest.raises(BadParameter):
            cluster_validate(valid_config, 'invalidcluster')
