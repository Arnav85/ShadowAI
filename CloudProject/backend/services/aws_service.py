import boto3
from botocore.exceptions import BotoCoreError, ClientError
from backend.core.config import settings


def _ec2_client(region: str):
    return boto3.client(
        "ec2",
        region_name=region,
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID or None,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY or None,
    )


def scan_orphaned_resources(region: str) -> list[dict]:
    """Scan for unattached EBS volumes and unused Elastic IPs."""
    resources = []
    try:
        ec2 = _ec2_client(region)

        # Unattached EBS volumes
        volumes = ec2.describe_volumes(
            Filters=[{"Name": "status", "Values": ["available"]}]
        )
        for vol in volumes.get("Volumes", []):
            resources.append({
                "type": "EBS Volume",
                "id": vol["VolumeId"],
                "size_gb": vol["Size"],
                "state": vol["State"],
                "created": str(vol.get("CreateTime", "")),
            })

        # Unused Elastic IPs
        eips = ec2.describe_addresses()
        for eip in eips.get("Addresses", []):
            if "AssociationId" not in eip:
                resources.append({
                    "type": "Elastic IP",
                    "id": eip.get("AllocationId", eip.get("PublicIp")),
                    "ip": eip.get("PublicIp"),
                    "state": "unassociated",
                    "created": "",
                })

    except (BotoCoreError, ClientError) as e:
        return [{"error": str(e)}]

    return resources


def delete_resources(resource_ids: list[str], region: str) -> dict:
    """Delete specified EBS volumes or release Elastic IPs."""
    ec2 = _ec2_client(region)
    deleted = []
    errors = []

    for rid in resource_ids:
        try:
            if rid.startswith("vol-"):
                ec2.delete_volume(VolumeId=rid)
                deleted.append(rid)
            elif rid.startswith("eipalloc-"):
                ec2.release_address(AllocationId=rid)
                deleted.append(rid)
            else:
                errors.append(f"Unknown resource type for id: {rid}")
        except (BotoCoreError, ClientError) as e:
            errors.append(f"{rid}: {str(e)}")

    return {"deleted": deleted, "errors": errors}
