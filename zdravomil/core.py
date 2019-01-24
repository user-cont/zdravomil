import colin
import os
import requests
import subprocess
import logging
from tempfile import mkstemp


from zdravomil.utils import *
logger = logging.getLogger(__name__)


class Zdravomil:

    def __init__(self):
        self.colin_result = None
        self.colin_logs = ''
        self.pastebin_url = ''
        self.github_api_header = {'Authorization': f"token {os.getenv('GITHUB_API_KEY')}"}

    def fetch_dockerfile(self):
        url = f"https://raw.githubusercontent.com/{self.artifact_info['source_repo']}/{self.artifact_info['rev']}/Dockerfile"
        logger.info(f"Pulling Dockerfile from: {url}")
        r = requests.get(url)

        if r.status_code == 200:
            self.dockerfile_path = os.path.join(
                HOME, f"Dockerfile-{os.path.basename(self.artifact_info['repo'])}"
                f"-{self.artifact_info['rev'][:6]}")

            with open(self.dockerfile_path, "w+") as dockerfile:
                dockerfile.write(r.text)

        elif r.status_code == 404:
            raise ZdravoIgnoredCommit('Dockerfile not found... SKIPPING linters.')
        else:
            r.raise_for_status()

    def run_linter(self):
        """
        Run colin linter and set results
        """
        logger.debug('Run colin linting')
        self.colin_result = colin.run(target=self.dockerfile_path,
                                      ruleset_name="fedora", target_type='dockerfile')
        self.colin_logs = self.colin_result.get_pretty_string(stat=False, verbose=False)
        self._set_result_status()

        if not self.colin_logs:
            raise Exception('Output of linter empty')

        logger.debug(self.colin_result.get_pretty_string(stat=False, verbose=True))
        logger.debug('Linters ended with status: %s', self.colin_result_status)

    def _set_result_status(self):
        if self.colin_result.statistics.get('FAIL', 0) > 0:
            self.colin_result_status = 'failed'
        elif self.colin_result.statistics.get('ERROR', 0) > 0:
            self.colin_result_status = 'needs_inspection'
        else:
            self.colin_result_status = 'passed'

    def push_to_pastebin(self):
        """
        Push logs to pastebin and provide url
        :return: string
        """
        self.pastebin_url = subprocess.check_output(['pastebinit', '-i', self.log_file,
                                                     '-b', 'http://paste.ubuntu.com/']).decode("utf-8").rstrip()

    def process(self):
        self.log_file = mkstemp()[1]
        log_handler = logging.FileHandler(self.log_file)
        log_handler.setLevel(logging.DEBUG)
        logger.addHandler(log_handler)
        logger.setLevel(logging.DEBUG)

        logger.info('Detected Pull request #%s in %s.', str(self.artifact_info['pr_id']),  str(self.artifact_info['repo']))
        try:
            self.get_source_info()
            self.fetch_dockerfile()
            self.run_linter()
            self.push_to_pastebin()
            self.report_to_github()

        except (ZdravoIgnoredCommit, AuthorMailNotFound) as e:
            logger.info(str(e))

        finally:
            if os.path.exists(self.dockerfile_path):
                logger.debug('Removing Dockerfile: %s', self.dockerfile_path)
                os.remove(self.dockerfile_path)
            logger.removeHandler(log_handler)

        return f"Linters ended with status {self.colin_result_status}"

    def get_source_info(self):
        url = f"https://api.github.com/repos/{self.artifact_info['repo']}/pulls/{self.artifact_info['pr_id']}"
        r = requests.get(url=url, headers=self.github_api_header)
        r.raise_for_status()
        self.artifact_info['source_repo'] = r.json()['head']['repo']['full_name']
        self.artifact_info['rev'] = r.json()['head']['sha']

    def report_to_github(self):
        url = f"{self.message['msg']['issue']['pull_request']['url']}/reviews"
        if self.colin_result_status == 'failed':
            event = 'REQUEST_CHANGES'
        else:
            event = 'APPROVE'

        res_json = {
            "commit_id": self.artifact_info['rev'],
            "body": f"Dockerfile linter {self.colin_result_status}, see {self.pastebin_url} for more info.",
            "event": event
        }

        r = requests.post(url=url, json=res_json, headers=self.github_api_header)
        r.raise_for_status()
        logger.info('Added review: %s', str(res_json))
