from unittest import TestCase
from unittest.mock import ANY, MagicMock, Mock, patch
from parameterized import parameterized

from samcli.commands.sync.command import do_cli, execute_code_sync
from samcli.lib.providers.provider import ResourceIdentifier
from samcli.commands._utils.options import DEFAULT_BUILD_DIR, DEFAULT_CACHE_DIR


def get_mock_sam_config():
    mock_sam_config = MagicMock()
    mock_sam_config.exists = MagicMock(return_value=True)
    return mock_sam_config


MOCK_SAM_CONFIG = get_mock_sam_config()


class TestSyncCliCommand(TestCase):
    def setUp(self):

        self.template_file = "input-template-file"
        self.stack_name = "stack-name"
        self.resource_id = []
        self.resource = []
        self.image_repository = "123456789012.dkr.ecr.us-east-1.amazonaws.com/test1"
        self.image_repositories = None
        self.mode = "mode"
        self.s3_prefix = "s3-prefix"
        self.kms_key_id = "kms-key-id"
        self.notification_arns = []
        self.parameter_overrides = {"a": "b"}
        self.capabilities = ("CAPABILITY_IAM",)
        self.tags = {"c": "d"}
        self.role_arn = "role_arn"
        self.metadata = {}
        self.region = None
        self.profile = None
        self.base_dir = None
        self.clean = True
        self.config_env = "mock-default-env"
        self.config_file = "mock-default-filename"
        MOCK_SAM_CONFIG.reset_mock()

    @parameterized.expand([(True, False), (False, False)])
    @patch("samcli.commands.sync.command.execute_code_sync")
    @patch("samcli.commands.build.command.click")
    @patch("samcli.commands.build.build_context.BuildContext")
    @patch("samcli.commands.package.command.click")
    @patch("samcli.commands.package.package_context.PackageContext")
    @patch("samcli.commands.deploy.command.click")
    @patch("samcli.commands.deploy.deploy_context.DeployContext")
    @patch("samcli.commands.build.command.os")
    def test_infra_must_succeed_sync(
        self,
        infra,
        code,
        os_mock,
        DeployContextMock,
        mock_deploy_click,
        PackageContextMock,
        mock_package_click,
        BuildContextMock,
        mock_build_click,
        execute_code_sync_mock,
    ):

        build_context_mock = Mock()
        BuildContextMock.return_value.__enter__.return_value = build_context_mock
        package_context_mock = Mock()
        PackageContextMock.return_value.__enter__.return_value = package_context_mock
        deploy_context_mock = Mock()
        DeployContextMock.return_value.__enter__.return_value = deploy_context_mock

        do_cli(
            self.template_file,
            infra,
            code,
            self.resource_id,
            self.resource,
            self.stack_name,
            self.region,
            self.profile,
            self.base_dir,
            self.parameter_overrides,
            self.mode,
            self.image_repository,
            self.image_repositories,
            self.s3_prefix,
            self.kms_key_id,
            self.capabilities,
            self.role_arn,
            self.notification_arns,
            self.tags,
            self.metadata,
            self.config_file,
            self.config_env,
        )

        BuildContextMock.assert_called_with(
            resource_identifier=None,
            template_file=self.template_file,
            base_dir=self.base_dir,
            build_dir=DEFAULT_BUILD_DIR,
            cache_dir=DEFAULT_CACHE_DIR,
            clean=True,
            use_container=False,
            parallel=True,
            parameter_overrides=self.parameter_overrides,
            mode=self.mode,
            cached=True,
        )

        PackageContextMock.assert_called_with(
            template_file=ANY,
            s3_bucket=ANY,
            image_repository=self.image_repository,
            image_repositories=self.image_repositories,
            s3_prefix=self.s3_prefix,
            kms_key_id=self.kms_key_id,
            output_template_file=ANY,
            no_progressbar=True,
            metadata=self.metadata,
            region=self.region,
            profile=self.profile,
            use_json=False,
            force_upload=True,
        )

        DeployContextMock.assert_called_with(
            template_file=ANY,
            stack_name=self.stack_name,
            s3_bucket=ANY,
            image_repository=self.image_repository,
            image_repositories=self.image_repositories,
            no_progressbar=True,
            s3_prefix=self.s3_prefix,
            kms_key_id=self.kms_key_id,
            parameter_overrides=self.parameter_overrides,
            capabilities=self.capabilities,
            role_arn=self.role_arn,
            notification_arns=self.notification_arns,
            tags=self.tags,
            region=self.region,
            profile=self.profile,
            no_execute_changeset=True,
            fail_on_empty_changeset=True,
            confirm_changeset=False,
            use_changeset=False,
            force_upload=True,
            signing_profiles=None,
        )
        package_context_mock.run.assert_called_with()
        self.assertEqual(package_context_mock.run.call_count, 1)
        deploy_context_mock.run.assert_called_with()
        self.assertEqual(deploy_context_mock.run.call_count, 1)
        execute_code_sync_mock.assert_not_called()

    @parameterized.expand([(False, True)])
    @patch("samcli.commands.sync.command.execute_code_sync")
    @patch("samcli.commands.build.command.click")
    @patch("samcli.commands.build.build_context.BuildContext")
    @patch("samcli.commands.package.command.click")
    @patch("samcli.commands.package.package_context.PackageContext")
    @patch("samcli.commands.deploy.command.click")
    @patch("samcli.commands.deploy.deploy_context.DeployContext")
    @patch("samcli.commands.build.command.os")
    def test_code_must_succeed_sync(
        self,
        infra,
        code,
        os_mock,
        DeployContextMock,
        mock_deploy_click,
        PackageContextMock,
        mock_package_click,
        BuildContextMock,
        mock_build_click,
        execute_code_sync_mock,
    ):

        build_context_mock = Mock()
        BuildContextMock.return_value.__enter__.return_value = build_context_mock
        package_context_mock = Mock()
        PackageContextMock.return_value.__enter__.return_value = package_context_mock
        deploy_context_mock = Mock()
        DeployContextMock.return_value.__enter__.return_value = deploy_context_mock

        do_cli(
            self.template_file,
            infra,
            code,
            self.resource_id,
            self.resource,
            self.stack_name,
            self.region,
            self.profile,
            self.base_dir,
            self.parameter_overrides,
            self.mode,
            self.image_repository,
            self.image_repositories,
            self.s3_prefix,
            self.kms_key_id,
            self.capabilities,
            self.role_arn,
            self.notification_arns,
            self.tags,
            self.metadata,
            self.config_file,
            self.config_env,
        )
        execute_code_sync_mock.assert_called_once_with(
            self.template_file, build_context_mock, deploy_context_mock, self.resource_id, self.resource
        )


class ExecuteCodeSync(TestCase):
    def setUp(self) -> None:
        self.template_file = "template.yaml"
        self.build_context = MagicMock()
        self.deploy_context = MagicMock()

    @patch("samcli.commands.sync.command.SamLocalStackProvider.get_stacks")
    @patch("samcli.commands.sync.command.SyncFlowFactory")
    @patch("samcli.commands.sync.command.SyncFlowExecutor")
    @patch("samcli.commands.sync.command.get_unique_resource_ids")
    def test_execute_code_sync_single_resource(
        self,
        get_unique_resource_ids_mock,
        sync_flow_executor_mock,
        sync_flow_factory_mock,
        get_stacks_mock,
    ):

        resource_identifier_strings = ["Function1"]
        resource_types = []
        sync_flows = [MagicMock()]
        sync_flow_factory_mock.return_value.create_sync_flow.side_effect = sync_flows
        get_unique_resource_ids_mock.return_value = {
            ResourceIdentifier("Function1"),
        }

        execute_code_sync(
            self.template_file, self.build_context, self.deploy_context, resource_identifier_strings, resource_types
        )

        sync_flow_factory_mock.return_value.create_sync_flow.assert_called_once_with(ResourceIdentifier("Function1"))
        sync_flow_executor_mock.return_value.add_sync_flow.assert_called_once_with(sync_flows[0])

        get_unique_resource_ids_mock.assert_called_once_with(
            get_stacks_mock.return_value[0], resource_identifier_strings, []
        )

    @patch("samcli.commands.sync.command.SamLocalStackProvider.get_stacks")
    @patch("samcli.commands.sync.command.SyncFlowFactory")
    @patch("samcli.commands.sync.command.SyncFlowExecutor")
    @patch("samcli.commands.sync.command.get_unique_resource_ids")
    def test_execute_code_sync_multiple_resource(
        self,
        get_unique_resource_ids_mock,
        sync_flow_executor_mock,
        sync_flow_factory_mock,
        get_stacks_mock,
    ):

        resource_identifier_strings = ["Function1", "Function2"]
        resource_types = []
        sync_flows = [MagicMock(), MagicMock()]
        sync_flow_factory_mock.return_value.create_sync_flow.side_effect = sync_flows
        get_unique_resource_ids_mock.return_value = {
            ResourceIdentifier("Function1"),
            ResourceIdentifier("Function2"),
        }

        execute_code_sync(
            self.template_file, self.build_context, self.deploy_context, resource_identifier_strings, resource_types
        )

        sync_flow_factory_mock.return_value.create_sync_flow.assert_any_call(ResourceIdentifier("Function1"))
        sync_flow_executor_mock.return_value.add_sync_flow.assert_any_call(sync_flows[0])

        sync_flow_factory_mock.return_value.create_sync_flow.assert_any_call(ResourceIdentifier("Function2"))
        sync_flow_executor_mock.return_value.add_sync_flow.assert_any_call(sync_flows[1])

        self.assertEqual(sync_flow_factory_mock.return_value.create_sync_flow.call_count, 2)
        self.assertEqual(sync_flow_executor_mock.return_value.add_sync_flow.call_count, 2)

        get_unique_resource_ids_mock.assert_called_once_with(
            get_stacks_mock.return_value[0], resource_identifier_strings, []
        )

    @patch("samcli.commands.sync.command.SamLocalStackProvider.get_stacks")
    @patch("samcli.commands.sync.command.SyncFlowFactory")
    @patch("samcli.commands.sync.command.SyncFlowExecutor")
    @patch("samcli.commands.sync.command.get_unique_resource_ids")
    def test_execute_code_sync_single_type_resource(
        self,
        get_unique_resource_ids_mock,
        sync_flow_executor_mock,
        sync_flow_factory_mock,
        get_stacks_mock,
    ):

        resource_identifier_strings = ["Function1", "Function2"]
        resource_types = ["Type1"]
        sync_flows = [MagicMock(), MagicMock(), MagicMock()]
        sync_flow_factory_mock.return_value.create_sync_flow.side_effect = sync_flows
        get_unique_resource_ids_mock.return_value = {
            ResourceIdentifier("Function1"),
            ResourceIdentifier("Function2"),
            ResourceIdentifier("Function3"),
        }
        execute_code_sync(
            self.template_file, self.build_context, self.deploy_context, resource_identifier_strings, resource_types
        )

        sync_flow_factory_mock.return_value.create_sync_flow.assert_any_call(ResourceIdentifier("Function1"))
        sync_flow_executor_mock.return_value.add_sync_flow.assert_any_call(sync_flows[0])

        sync_flow_factory_mock.return_value.create_sync_flow.assert_any_call(ResourceIdentifier("Function2"))
        sync_flow_executor_mock.return_value.add_sync_flow.assert_any_call(sync_flows[1])

        sync_flow_factory_mock.return_value.create_sync_flow.assert_any_call(ResourceIdentifier("Function3"))
        sync_flow_executor_mock.return_value.add_sync_flow.assert_any_call(sync_flows[2])

        self.assertEqual(sync_flow_factory_mock.return_value.create_sync_flow.call_count, 3)
        self.assertEqual(sync_flow_executor_mock.return_value.add_sync_flow.call_count, 3)

        get_unique_resource_ids_mock.assert_called_once_with(
            get_stacks_mock.return_value[0], resource_identifier_strings, ["Type1"]
        )

    @patch("samcli.commands.sync.command.SamLocalStackProvider.get_stacks")
    @patch("samcli.commands.sync.command.SyncFlowFactory")
    @patch("samcli.commands.sync.command.SyncFlowExecutor")
    @patch("samcli.commands.sync.command.get_unique_resource_ids")
    def test_execute_code_sync_multiple_type_resource(
        self,
        get_unique_resource_ids_mock,
        sync_flow_executor_mock,
        sync_flow_factory_mock,
        get_stacks_mock,
    ):
        resource_identifier_strings = ["Function1", "Function2"]
        resource_types = ["Type1", "Type2"]
        sync_flows = [MagicMock(), MagicMock(), MagicMock(), MagicMock()]
        sync_flow_factory_mock.return_value.create_sync_flow.side_effect = sync_flows
        get_unique_resource_ids_mock.return_value = {
            ResourceIdentifier("Function1"),
            ResourceIdentifier("Function2"),
            ResourceIdentifier("Function3"),
            ResourceIdentifier("Function4"),
        }
        execute_code_sync(
            self.template_file, self.build_context, self.deploy_context, resource_identifier_strings, resource_types
        )

        sync_flow_factory_mock.return_value.create_sync_flow.assert_any_call(ResourceIdentifier("Function1"))
        sync_flow_executor_mock.return_value.add_sync_flow.assert_any_call(sync_flows[0])

        sync_flow_factory_mock.return_value.create_sync_flow.assert_any_call(ResourceIdentifier("Function2"))
        sync_flow_executor_mock.return_value.add_sync_flow.assert_any_call(sync_flows[1])

        sync_flow_factory_mock.return_value.create_sync_flow.assert_any_call(ResourceIdentifier("Function3"))
        sync_flow_executor_mock.return_value.add_sync_flow.assert_any_call(sync_flows[2])

        sync_flow_factory_mock.return_value.create_sync_flow.assert_any_call(ResourceIdentifier("Function4"))
        sync_flow_executor_mock.return_value.add_sync_flow.assert_any_call(sync_flows[3])

        self.assertEqual(sync_flow_factory_mock.return_value.create_sync_flow.call_count, 4)
        self.assertEqual(sync_flow_executor_mock.return_value.add_sync_flow.call_count, 4)

        get_unique_resource_ids_mock.assert_any_call(
            get_stacks_mock.return_value[0], resource_identifier_strings, ["Type1", "Type2"]
        )

    @patch("samcli.commands.sync.command.SamLocalStackProvider.get_stacks")
    @patch("samcli.commands.sync.command.SyncFlowFactory")
    @patch("samcli.commands.sync.command.SyncFlowExecutor")
    @patch("samcli.commands.sync.command.get_resource_ids_by_type")
    @patch("samcli.commands.sync.command.get_all_resource_ids")
    def test_execute_code_sync_default_all_resources(
        self,
        get_all_resource_ids_mock,
        get_resource_ids_by_type_mock,
        sync_flow_executor_mock,
        sync_flow_factory_mock,
        get_stacks_mock,
    ):
        sync_flows = [MagicMock(), MagicMock(), MagicMock(), MagicMock()]
        sync_flow_factory_mock.return_value.create_sync_flow.side_effect = sync_flows
        get_all_resource_ids_mock.return_value = [
            ResourceIdentifier("Function1"),
            ResourceIdentifier("Function2"),
            ResourceIdentifier("Function3"),
            ResourceIdentifier("Function4"),
        ]
        execute_code_sync(self.template_file, self.build_context, self.deploy_context, "", [])

        sync_flow_factory_mock.return_value.create_sync_flow.assert_any_call(ResourceIdentifier("Function1"))
        sync_flow_executor_mock.return_value.add_sync_flow.assert_any_call(sync_flows[0])

        sync_flow_factory_mock.return_value.create_sync_flow.assert_any_call(ResourceIdentifier("Function2"))
        sync_flow_executor_mock.return_value.add_sync_flow.assert_any_call(sync_flows[1])

        sync_flow_factory_mock.return_value.create_sync_flow.assert_any_call(ResourceIdentifier("Function3"))
        sync_flow_executor_mock.return_value.add_sync_flow.assert_any_call(sync_flows[2])

        sync_flow_factory_mock.return_value.create_sync_flow.assert_any_call(ResourceIdentifier("Function4"))
        sync_flow_executor_mock.return_value.add_sync_flow.assert_any_call(sync_flows[3])

        self.assertEqual(sync_flow_factory_mock.return_value.create_sync_flow.call_count, 4)
        self.assertEqual(sync_flow_executor_mock.return_value.add_sync_flow.call_count, 4)

        get_all_resource_ids_mock.assert_called_once_with(get_stacks_mock.return_value[0])
