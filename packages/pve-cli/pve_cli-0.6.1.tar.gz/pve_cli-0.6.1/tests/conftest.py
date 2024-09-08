from pathlib import Path

import pytest
import toml
from typer.testing import CliRunner


@pytest.fixture
def runner() -> CliRunner:
    return CliRunner()


@pytest.fixture
def valid_config() -> dict:
    return {
        'defaults': {'cluster': 'examplecluster'},
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


@pytest.fixture
def valid_config_no_default_cluster(tmp_path: Path) -> Path:
    config_file_path = tmp_path / 'config.toml'
    config = {
        'clusters': {
            'examplecluster': {
                'host': 'examplehost',
                'user': 'root',
                'realm': 'foo',
                'token_name': 'test',
                'token_secret': 'PSSST!',
            }
        }
    }
    config_file_path.write_text(toml.dumps(config))
    return config_file_path
