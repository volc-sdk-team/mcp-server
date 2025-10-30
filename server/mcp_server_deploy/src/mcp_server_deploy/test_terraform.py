from unittest import TestCase

from src.mcp_server_deploy.terraform import (
    get_zone_id,
    has_already_create_container_registry,
    parse_user_deploy_conf,
)


class Test(TestCase):
    def test_get_zone_id(self):
        try:
            zone_id = get_zone_id(
                "",
                "",
                "cn-beijing",
            )
        except Exception as e:
            self.fail(f"get_zone_id failed, err: {str(e)}")
        self.assertIsNotNone(zone_id)
        print(f"zone_id: {zone_id}")

    def test_parse_user_deploy_conf(self):
        with open("deploy.yaml", "r") as f:
            d = parse_user_deploy_conf(f.read())
            print(d)

    def test_has_already_create_container_registry(self):
        v = has_already_create_container_registry(
            "",
            "",
            "cn-beijing",
            "default",
        )

        print(v)
