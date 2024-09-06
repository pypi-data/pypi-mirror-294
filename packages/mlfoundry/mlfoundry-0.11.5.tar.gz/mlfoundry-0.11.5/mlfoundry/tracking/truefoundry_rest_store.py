import typing
from functools import partial

from mlflow.config import config
from mlflow.entities import FileInfo
from mlflow.store.tracking import rest_store
from mlflow.tracking._tracking_service.utils import _get_default_host_creds
from mlflow.utils.rest_utils import http_request_safe

from mlfoundry.run_utils import append_path_to_rest_tracking_uri
from mlfoundry.tracking.entities import ArtifactCredential


class TruefoundryRestStore(rest_store.RestStore):
    # TODO (chiragjn): This method should be removed once TruefoundryArtifactRepository is removed
    def list_artifacts(self, run_id, path, **kwargs) -> typing.List[FileInfo]:
        infos = []
        page_size = 500
        page_token = None
        while True:
            json_body = config.ListRunArtifacts.request_dto(
                run_id=run_id,
                path=path,
                max_results=page_size,
                page_token=page_token,
            ).json()
            response = self._call_endpoint(config.ListRunArtifacts, json_body)
            artifact_list = response.files

            # If `path` is a file, ListRunArtifacts returns a single list element with the
            # same name as `path`. The list_artifacts API expects us to return an empty list in this
            # case, so we do so here.
            # TODO (chiragjn): should also check next_page_token being None because we are paging
            #   but it is fine as long as page_size > 1
            if (
                len(artifact_list) == 1
                and artifact_list[0].path == path
                and not artifact_list[0].is_dir
            ):
                return []
            for output_file in artifact_list:
                infos.append(FileInfo.from_dto(output_file))
            if len(artifact_list) == 0 or not response.next_page_token:
                break
            page_token = response.next_page_token
        return infos

    # TODO (chiragjn): This method should be removed once TruefoundryArtifactRepository is removed
    def get_artifact_read_credentials(self, run_id, path) -> ArtifactCredential:
        host_cred = self.get_host_creds()
        response = http_request_safe(
            host_creds=host_cred,
            endpoint="/api/2.0/mlflow/artifacts/credentials-read",
            method="get",
            params={"run_id": run_id, "path": path},
        )

        response = response.json()

        artifact_credential = ArtifactCredential(
            run_id=response["run_id"],
            path=response["path"],
            signed_uri=response["signed_uri"],
        )
        return artifact_credential

    # TODO (chiragjn): This method should be removed once TruefoundryArtifactRepository is removed
    def get_artifact_write_credential(self, run_id, path) -> ArtifactCredential:
        host_cred = self.get_host_creds()
        response = http_request_safe(
            host_creds=host_cred,
            endpoint="/api/2.0/mlflow/artifacts/credentials-write",
            method="get",
            params={"run_id": run_id, "path": path},
        )

        response = response.json()

        artifact_credential = ArtifactCredential(
            run_id=response["run_id"],
            path=response["path"],
            signed_uri=response["signed_uri"],
        )
        return artifact_credential


def get_rest_store(tracking_uri: str) -> TruefoundryRestStore:
    tracking_uri = append_path_to_rest_tracking_uri(tracking_uri)
    get_cred = partial(_get_default_host_creds, tracking_uri)
    return TruefoundryRestStore(get_cred)
