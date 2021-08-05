import unittest
from typing import List, Optional

from parameterized import parameterized

from metrics import Deployment


def _fixtures() -> List[List[Optional[str]]]:
    return [
        ['marketplace-api', 'v1.1.1', 'staging', None],
        ['marketplace-api', 'v1.1.1', 'staging', 'test'],
    ]


class DeploymentValueObjectTest(unittest.TestCase):

    @parameterized.expand(_fixtures())
    def test_encapsulates_the_right_data(self, application_id, version, environment, service) -> None:
        deployment = Deployment(application_id, version, environment)

        self.assertEqual(application_id, deployment.application_id)
        self.assertEqual(version, deployment.version)
        self.assertEqual(environment, deployment.environment)
        self.assertIsNone(deployment.service)
        self.assertEqual('-'.join([application_id, version]), deployment.id())

        if service is not None:
            deployment = Deployment(application_id, version, environment, service)
            self.assertEqual(service, deployment.service)
            self.assertEqual('-'.join([application_id, version, service]), deployment.id())


if __name__ == '__main__':
    unittest.main()
