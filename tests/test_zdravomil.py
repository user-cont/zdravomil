import pytest
import os
import json
import requests
from pathlib import Path
from flexmock import flexmock

import zdravomil.core as zdravomil


def fake_post_to_gihub(url, json, headers):
    assert url == 'https://api.dummy.com/repos/container-images/rsyslog/pulls/2/reviews'
    assert headers == {'Authorization': f"token None"}
    assert json == {
        "commit_id": '123456',
        "body": f"Dockerfile linter passed, see some_pastebin_url for more info.",
        "event": 'APPROVE'
    }
    resp = requests.Response()
    resp.status_code = 200
    return resp


class TestZdravomil:
    """Test Zdravomil class"""

    def setup_method(self):
        self.zdravo = zdravomil.Zdravomil()

    @pytest.fixture
    def umb_message_container(self):
        content = (Path(__file__).parent / 'data/fedmsg_message.json').read_text()
        return json.loads(content)

    def fake_distgit_repo_func(self, file):
        self.zdravo.dockerfile_path = Path(__file__).parent / 'data' / file

    def test_valid_dockerfile(self, umb_message_container):
        flexmock(self.zdravo, push_to_pastebin=True)
        flexmock(self.zdravo, get_source_info=True)
        (flexmock(self.zdravo)
         .should_receive("fetch_dockerfile")
         .replace_with(self.fake_distgit_repo_func('Dockerfile_valid')))
        flexmock(requests). \
            should_receive("post"). \
            replace_with(fake_post_to_gihub).once()


        self.zdravo.message = umb_message_container
        self.zdravo.artifact_info = {
            'repo': umb_message_container['msg']['repository']['full_name'],
            'pr_id': umb_message_container['msg']['issue']['number'],
            'rev': '123456'
        }
        self.zdravo.pastebin_url = 'some_pastebin_url'

        self.zdravo.process()
        assert self.zdravo.colin_result_status == 'passed'
