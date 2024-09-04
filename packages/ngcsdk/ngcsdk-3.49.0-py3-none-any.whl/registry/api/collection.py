#
# Copyright (c) 2021, NVIDIA CORPORATION.  All rights reserved.
# Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.
"""API interface for Collections."""
import asyncio
import logging
import sys
from typing import Optional

from ngcbpc.api.configuration import Configuration
from ngcbpc.api.pagination import pagination_helper
from ngcbpc.api.utils import DotDict
from ngcbpc.constants import CANARY_ENV, PRODUCTION_ENV, STAGING_ENV
from ngcbpc.data.model.ArtifactListResponse import ArtifactListResponse
from ngcbpc.data.model.Collection import Collection
from ngcbpc.data.model.CollectionCreateRequest import CollectionCreateRequest
from ngcbpc.data.model.CollectionResponse import CollectionResponse
from ngcbpc.data.model.CollectionUpdateRequest import CollectionUpdateRequest
from ngcbpc.data.model.RequestStatus import RequestStatus
from ngcbpc.errors import NgcAPIError
from ngcbpc.transfer import utils as xfer_utils
from ngcbpc.util.utils import extra_args
from registry.api.utils import (
    apply_labels_update,
    get_auth_org_and_team,
    get_environ_tag,
    get_label_set_labels,
    SimpleRegistryTarget,
)
from registry.constants import CollectionArtifacts
from registry.printer.collection import CollectionPrinter

environ_tag = get_environ_tag()
env = {PRODUCTION_ENV: "prod", CANARY_ENV: "canary", STAGING_ENV: "stg"}.get(environ_tag)
ENDPOINT_VERSION = "v2"

logger = logging.getLogger(__name__)


class CollectionAPI:  # noqa: D101
    def __init__(self, connection, api_client=None):
        self.connection = connection
        self.api_client = api_client
        self.resource_type = "COLLECTION"
        self.printer = CollectionPrinter()
        self.config = Configuration()

    @staticmethod
    def _get_guest_base_endpoint():
        """Build out the base collection endpoint which can be extended to all possible endpoints (/v2/collections)."""
        return [ENDPOINT_VERSION, "collections"]

    def _get_guest_endpoint(self, org, team=None):
        """Interpolate org and team parameters onto guest endpoint in the form `/v2/collections/{org}[/team]`."""
        endpoint = self._get_guest_base_endpoint()
        endpoint.append(org)
        if team:
            endpoint.append(team)
        return endpoint

    @staticmethod
    def _get_auth_endpoint(org, team=None):
        """Build base auth endpoint which requires org in all cases, unlike the guest endpoint.  Construct in the form
        /v2/org/{org}/[team/{team}/]collections
        """  # noqa: D205, D415
        endpoint = [ENDPOINT_VERSION, "org", org]
        if team:
            endpoint.extend(["team", team])
        endpoint.append("collections")
        return endpoint

    @staticmethod
    def _get_find_endpoint(org, artifact_type, artifact_name, team=None, has_key=False):
        """Build the find endpoint which takes on a different form than the rest of the ones in the collections
        controller.  The authenticated endpoint is in the form
            /v2/org/{org}/[team/{team}/]{artifact_type}/{artifact_name}/collections
        The guest endpoints is in the form
            /v2/{artifact_type}/org/{org}/team/{team}/{artifact_name}/collections
        """  # noqa: D205, D415
        endpoint = [ENDPOINT_VERSION]
        org_team = ["org", org]
        if team:
            org_team.append("team")
            org_team.append(team)

        if has_key:
            endpoint.extend(org_team)
            endpoint.append(artifact_type)
        else:
            endpoint.append(artifact_type)
            endpoint.extend(org_team)

        endpoint.append(artifact_name)
        endpoint.append("collections")

        return endpoint

    def create(
        self,
        target,
        display_name,
        label_set,
        label,
        logo,
        overview_filename,
        built_by,
        publisher,
        short_desc,
        category,
        images,
        charts,
        models,
        resources,
    ) -> CollectionResponse:
        """Create a collection."""
        self.config.validate_configuration()

        reg_target = SimpleRegistryTarget(target, org_required=True, name_required=True)
        collection_create_request = CollectionCreateRequest(
            {
                "name": reg_target.name,
                "displayName": display_name,
                "labels": None,
                "labelsV2": get_label_set_labels(
                    self.api_client.registry.label_set, self.resource_type, label_set, label
                ),
                "logo": logo,
                "description": overview_filename,  # Read from the markdown file
                "builtBy": built_by,
                "publisher": publisher,
                "shortDescription": short_desc,
                "category": category,
            }
        )

        collection_response = self.create_collection(collection_create_request, reg_target)

        artifacts_response, errors = self.make_artifacts_requests(
            images, charts, models, resources, reg_target, verb="PUT"
        )

        return (collection_response, artifacts_response, errors)

    def create_collection(self, collection_create_request, reg_target):
        """Call API to create collection."""
        endpoint = "/".join(self._get_auth_endpoint(reg_target.org, team=reg_target.team))

        collection_response = self.connection.make_api_request(
            "POST",
            endpoint,
            payload=collection_create_request.toJSON(),
            auth_org=reg_target.org,
            auth_team=reg_target.team,
            operation_name="post collection",
        )
        collection_response = CollectionResponse(collection_response)
        if not collection_response.collection:
            collection_response.collection = Collection()
        return collection_response

    def update(
        self,
        collection_target,
        display_name,
        add_label,
        remove_label,
        label_set,
        label,
        logo,
        overview_filename,
        built_by,
        publisher,
        short_desc,
        category,
        add_images,
        add_charts,
        add_models,
        add_resources,
        remove_images,
        remove_charts,
        remove_models,
        remove_resources,
    ):
        """Update a collection."""
        self.config.validate_configuration(guest_mode_allowed=False)
        reg_target = SimpleRegistryTarget(collection_target, org_required=True, name_required=True)
        # API layer should also validation
        # if (args.label or args.label_set) and (args.add_label or args.remove_label):
        #     raise argparse.ArgumentTypeError(
        #         "Declaritive arguments `labels` or `label_set` "
        #         "cannot be used with imperative arguments `add_label` or `remove_label`"
        #     )

        labels_v2 = []
        if label or label_set:
            labels_v2 = get_label_set_labels(self.api_client.registry.label_set, self.resource_type, label_set, label)
        else:
            for response in self.get_info(reg_target.org, reg_target.team, reg_target.name, has_key=True):
                if "collection" in response:
                    labels_v2 = CollectionResponse(response).collection.labels or []
                    break
        collection_update_request = CollectionUpdateRequest(
            {
                "displayName": display_name,
                "labels": None,
                "labelsV2": apply_labels_update(labels_v2, add_label or [], remove_label or []),
                "logo": logo,
                "description": overview_filename,  # Read from the markdown file
                "builtBy": built_by,
                "publisher": publisher,
                "shortDescription": short_desc,
                "category": category,
            }
        )

        collection_response = self.update_collection(collection_update_request, reg_target)

        _, add_errors = self.make_artifacts_requests(
            add_images, add_charts, add_models, add_resources, reg_target, verb="PUT"
        )

        _, remove_errors = self.make_artifacts_requests(
            remove_images, remove_charts, remove_models, remove_resources, reg_target, verb="DELETE"
        )

        return (collection_response, add_errors, remove_errors)

    def update_collection(self, collection_update_request, reg_target):
        """Call API to update collection."""
        endpoint = self._get_auth_endpoint(reg_target.org, team=reg_target.team)
        endpoint.append(reg_target.name)
        endpoint = "/".join(endpoint)

        collection_response = self.connection.make_api_request(
            "PATCH",
            endpoint,
            payload=collection_update_request.toJSON(),
            auth_org=reg_target.org,
            auth_team=reg_target.team,
            operation_name="patch collection",
        )
        return CollectionResponse(collection_response)

    def make_artifacts_requests(self, images, charts, models, resources, reg_target, verb="PUT"):
        """Create artifacts for a collection."""
        header_apitarget_artifacts = (
            ("Images", CollectionArtifacts["IMAGES"].value, images),
            ("Charts", CollectionArtifacts["HELM_CHARTS"].value, charts),
            ("Models", CollectionArtifacts["MODELS"].value, models),
            ("Resources", CollectionArtifacts["RESOURCES"].value, resources),
        )

        request_dict = {}
        for header, apitarget, artifacts in header_apitarget_artifacts:
            request_dict[header] = set()
            for artifact in artifacts:
                artifact_target = SimpleRegistryTarget(artifact, org_required=True, name_required=True)
                request_dict[header].add((artifact_target.org, artifact_target.team, artifact_target.name, apitarget))
        endpoint = "/".join(self._get_auth_endpoint(reg_target.org, team=reg_target.team))
        if sys.version_info[0] == 3 and sys.version_info[1] >= 8 and sys.platform.startswith("win"):
            # Windows has been unable to close the asyncio loop successfully. This line of code is a fix
            # to handle the asyncio loop failures. Without it, code is unable to CTRL-C or finish.
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        return asyncio.run(
            self._make_artifacts_requests(
                endpoint, request_dict, reg_target.org, reg_target.name, reg_target.team, verb
            )
        )

    @staticmethod
    def _flatten_request_items(request_dict):
        flat = []
        for key, requests in request_dict.items():
            flat.extend([(key, itm) for itm in requests])
        return flat

    async def _make_artifacts_requests(self, endpoint, request_dict, org, collection_name, team, verb):
        response_dict = {key: [] for key in request_dict}
        error_dict = {key: [] for key in request_dict}
        request_items = self._flatten_request_items(request_dict)
        results = await xfer_utils.gather(
            [
                self._artifact_request(collection_name, verb, endpoint, key, request, org, team)
                for key, request in request_items
            ],
        )
        for success, fail in results:
            for key, val in success.items():
                response_dict[key].append(val)
            for key, val in fail.items():
                error_dict[key].append(val)
        return response_dict, error_dict

    async def _artifact_request(self, collection_name, verb, endpoint, key, request, org, team):
        succeed = {}
        fail = {}
        artifact_org, artifact_team, artifact_name, api_target = request
        org_team = ["org", artifact_org]
        if artifact_team:
            org_team.append("team")
            org_team.append(artifact_team)
        org_team = "/".join(org_team)
        artifact_target = [artifact_org]
        if artifact_team:
            artifact_target.append(artifact_team)
        artifact_target.append(artifact_name)
        artifact_target = "/".join(artifact_target)
        try:
            response = await self.connection.make_async_api_request(
                verb,
                f"{endpoint}/{collection_name}/artifacts/{org_team}/{api_target}/{artifact_name}",
                auth_org=org,
                auth_team=team,
                operation_name="put collection artifact",
            )
            response = RequestStatus(response["requestStatus"])
            succeed[key] = (artifact_target, response)
        except NgcAPIError as e:
            request_status = e.explanation["requestStatus"]
            response = RequestStatus(request_status)
            fail[key] = (artifact_target, response)
        return succeed, fail

    def list(self, target: Optional[str]):
        """Get a list of available collection in the registry."""
        self.config.validate_configuration(guest_mode_allowed=True, csv_allowed=True)
        org = self.config.org_name
        team = self.config.team_name
        # If target specified then need to parse and validate
        if target:
            srt = SimpleRegistryTarget(target, name_required=True, glob_allowed=True)
            org, team = get_auth_org_and_team(srt.org, srt.team, org, team)

        return self.api_client.registry.search.search_collections(org, team, target or "*")

    def list_collections(self, org=None, team=None):  # noqa: D102
        endpoint = self._get_guest_base_endpoint()
        if org:
            endpoint = self._get_auth_endpoint(org, team=team)

        endpoint = "/".join(endpoint) + "?"  # Hack to mark the end of the API and start of params from pagination
        for page in pagination_helper(
            self.connection, endpoint, org_name=org, team_name=team, operation_name="get collection list"
        ):
            yield page

    def info(self, target) -> DotDict:
        """Get information about a collection in the registry."""
        self.config.validate_configuration(guest_mode_allowed=True)
        srt = SimpleRegistryTarget(target, org_required=True, name_required=True)
        has_key = bool(self.config.app_key)
        org, team = get_auth_org_and_team(srt.org, srt.team, self.config.org_name, self.config.team_name)
        target = srt.name
        # Reponses are asynchronous and come in any order, need to construct into relevant objects
        collection = CollectionResponse()
        artifacts_dict = {"Images": [], "Charts": [], "Models": [], "Resources": []}
        for response in self.get_info(org, team, target, has_key):
            if "collection" in response:
                collection = CollectionResponse(response)
            elif "artifacts" in response and response["artifacts"]:
                artifacts = ArtifactListResponse(response).artifacts
                if artifacts[0].artifactType == "MODEL":
                    artifacts_dict["Models"] = artifacts
                elif artifacts[0].artifactType == "REPOSITORY":
                    artifacts_dict["Images"] = artifacts
                elif artifacts[0].artifactType == "HELM_CHART":
                    artifacts_dict["Charts"] = artifacts
                elif artifacts[0].artifactType == "MODEL_SCRIPT":
                    artifacts_dict["Resources"] = artifacts
                else:
                    raise ValueError(f"Unrecognized response type '{artifacts[0].artifactType}'")

        return DotDict({"collection": collection.collection, "artifacts": artifacts_dict})

    def get_info(self, org, team, name, has_key=False):  # noqa: D102
        urls = []
        base = []
        if has_key:
            base = self._get_auth_endpoint(org, team)
        else:
            base = self._get_guest_endpoint(org, team)
        base.append(name)

        urls.append("/".join(base))
        for artifact in CollectionArtifacts:
            base = urls[0]
            urls.append(base + f"/artifacts/{artifact.value}")

        # Parameterize URL encodings
        params = [None] * len(urls)
        params[0] = {"resolve-labels": "false"}

        resp = self.connection.make_multiple_request(
            "GET", urls, params=params, auth_org=org, auth_team=team, operation_name="get collection"
        )

        return resp

    def remove(self, org, name, team=None):  # noqa: D102
        endpoint = self._get_auth_endpoint(org, team=team)
        endpoint.append(name)
        endpoint = "/".join(endpoint)
        return self.connection.make_api_request(
            "DELETE", endpoint, auth_org=org, auth_team=team, operation_name="delete collection"
        )

    def find(self, org, artifact_type, artifact_name, team=None, has_key=False):
        """Get list of collections containing a an artifact."""
        endpoint = self._get_find_endpoint(org, artifact_type, artifact_name, team=team, has_key=has_key)

        endpoint = "/".join(endpoint) + "?"  # Hack to mark the end of the API and start of params from pagination
        for page in pagination_helper(
            self.connection, endpoint, org_name=org, team_name=team, operation_name="get artifact collection list"
        ):
            yield page

    @extra_args
    def publish(
        self,
        target,
        source: Optional[str] = None,
        metadata_only=False,
        visibility_only=False,
        allow_guest: Optional[bool] = False,
        discoverable: Optional[bool] = False,
        public: Optional[bool] = False,
    ):
        """Publishes a collection with options for metadata, and visibility.

        This method manages the publication of a collection of artifacts, handling
        different aspects of the publication such as metadata only, and
        visibility adjustments. It validates the combination of arguments provided
        and processes the publication accordingly.
        """  # noqa: D401
        self.config.validate_configuration(guest_mode_allowed=False)
        self.api_client.registry.publish.publish(
            self.resource_type,
            self.config.org_name,
            self.config.team_name,
            target,
            source,
            metadata_only,
            False,
            visibility_only,
            allow_guest,
            discoverable,
            public,
        )
