from typing import List, Optional, Tuple

import click

from anyscale.cli_logger import BlockLogger
from anyscale.controllers.resource_quota_controller import ResourceQuotaController


log = BlockLogger()  # CLI Logger


@click.group("resource-quota", help="Anyscale resource quota commands.")
def resource_quota_cli() -> None:
    pass


@resource_quota_cli.command(
    name="create", help="Create a resource quota.",
)
@click.option(
    "-n", "--name", required=True, help="Name of the resource quota to create.",
)
@click.option(
    "--cloud",
    required=True,
    help="Name of the cloud that this resource quota applies to.",
)
@click.option(
    "--project",
    default=None,
    help="Name of the project that this resource quota applies to.",
)
@click.option(
    "--user-email",
    default=None,
    help="Email of the user that this resource quota applies to.",
)
@click.option(
    "--num-cpus",
    required=False,
    help="The quota limit for the number of CPUs.",
    type=int,
)
@click.option(
    "--num-instances",
    required=False,
    help="The quota limit for the number of instances.",
    type=int,
)
@click.option(
    "--num-gpus",
    required=False,
    help="The quota limit for the total number of GPUs.",
    type=int,
)
@click.option(
    "--num-accelerators",
    required=False,
    help="The quota limit for the number of accelerators. Example: --num-accelerators A100-80G 10",
    nargs=2,
    type=(str, int),
    multiple=True,
)
def create(  # noqa: PLR0913
    name: str,
    cloud: str,
    project: Optional[str],
    user_email: Optional[str],
    num_cpus: Optional[int],
    num_instances: Optional[int],
    num_gpus: Optional[int],
    num_accelerators: List[Tuple[str, int]],
) -> None:
    """Creates a resource quota.

    A name and cloud name must be provided.

    `$ anyscale resource-quota create -n my-resource-quota --cloud my-cloud --project my-project --user-email test@myorg.com --num-cpus 10 --num-instances 10 --num-gpus 10 --num-accelerators L4 5 --num-accelerators T4 10`
    """
    resource_quota_controller = ResourceQuotaController()
    resource_quota_controller.create(
        name=name,
        cloud=cloud,
        project=project,
        user_email=user_email,
        num_cpus=num_cpus,
        num_instances=num_instances,
        num_gpus=num_gpus,
        num_accelerators=dict(num_accelerators),
    )


@resource_quota_cli.command(
    name="list", help="List resource quotas.",
)
@click.option(
    "-n", "--name", required=False, help="The name filter for the resource quotas.",
)
@click.option(
    "--cloud", required=False, help="The cloud filter for the resource quotas.",
)
@click.option(
    "--creator_id",
    required=False,
    help="The creator ID filter for the resource quotas.",
)
@click.option(
    "--is-enabled",
    required=False,
    default=None,
    help="The is_enabled filter for the resource quotas.",
    type=bool,
)
@click.option(
    "--include-deleted",
    required=False,
    default=False,
    help="Include deleted resource quotas in the results.",
    type=bool,
)
def list_resource_quotas(
    name: Optional[str],
    cloud: Optional[str],
    creator_id: Optional[str],
    is_enabled: Optional[bool],
    include_deleted: Optional[bool],
) -> None:
    """List resource quotas.

    `$ anyscale resource-quota list -n my-resource-quota --cloud my-cloud`
    """
    resource_quota_controller = ResourceQuotaController()
    resource_quota_controller.list_resource_quotas(
        name=name,
        cloud=cloud,
        creator_id=creator_id,
        is_enabled=is_enabled,
        include_deleted=include_deleted,
    )
