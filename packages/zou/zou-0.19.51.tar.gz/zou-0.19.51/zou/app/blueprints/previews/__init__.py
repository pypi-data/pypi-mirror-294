from flask import Blueprint
from zou.app.utils.api import configure_api_from_blueprint

from zou.app.blueprints.previews.resources import (
    AttachmentThumbnailResource,
    CreatePreviewFilePictureResource,
    PreviewFileLowMovieResource,
    PreviewFileMovieResource,
    PreviewFileMovieDownloadResource,
    PreviewFileThumbnailResource,
    PreviewFileResource,
    PreviewFileDownloadResource,
    PreviewFileThumbnailSquareResource,
    PreviewFilePreviewResource,
    PreviewFileOriginalResource,
    PreviewFileTileResource,
    OrganisationThumbnailResource,
    CreateOrganisationThumbnailResource,
    ProjectThumbnailResource,
    CreateProjectThumbnailResource,
    PersonThumbnailResource,
    CreatePersonThumbnailResource,
    RunningPreviewFiles,
    SetMainPreviewResource,
    UpdateAnnotationsResource,
    UpdatePreviewPositionResource,
    ExtractFrameFromPreview,
    ExtractTileFromPreview,
    CreatePreviewBackgroundFileResource,
    PreviewBackgroundFileThumbnailResource,
    PreviewBackgroundFileResource,
)

routes = [
    ("/data/playlists/preview-files/running", RunningPreviewFiles),
    (
        "/pictures/preview-files/<instance_id>",
        CreatePreviewFilePictureResource,
    ),
    (
        "/movies/originals/preview-files/<instance_id>.mp4",
        PreviewFileMovieResource,
    ),
    (
        "/movies/originals/preview-files/<instance_id>/download",
        PreviewFileMovieDownloadResource,
    ),
    (
        "/movies/low/preview-files/<instance_id>.mp4",
        PreviewFileLowMovieResource,
    ),
    (
        "/pictures/thumbnails/preview-files/<instance_id>.png",
        PreviewFileThumbnailResource,
    ),
    (
        "/pictures/thumbnails/attachment-files/<attachment_file_id>.png",
        AttachmentThumbnailResource,
    ),
    (
        "/pictures/thumbnails-square/preview-files/<instance_id>.png",
        PreviewFileThumbnailSquareResource,
    ),
    (
        "/pictures/originals/preview-files/<instance_id>.png",
        PreviewFileOriginalResource,
    ),
    (
        "/pictures/originals/preview-files/<instance_id>.<extension>",
        PreviewFileResource,
    ),
    (
        "/pictures/originals/preview-files/<instance_id>/download",
        PreviewFileDownloadResource,
    ),
    (
        "/pictures/previews/preview-files/<instance_id>.png",
        PreviewFilePreviewResource,
    ),
    (
        "/movies/tiles/preview-files/<instance_id>.png",
        PreviewFileTileResource,
    ),
    (
        "/pictures/thumbnails/organisations/<instance_id>",
        CreateOrganisationThumbnailResource,
    ),
    (
        "/pictures/thumbnails/organisations/<instance_id>.png",
        OrganisationThumbnailResource,
    ),
    (
        "/pictures/thumbnails/persons/<instance_id>",
        CreatePersonThumbnailResource,
    ),
    (
        "/pictures/thumbnails/persons/<instance_id>.png",
        PersonThumbnailResource,
    ),
    (
        "/pictures/thumbnails/projects/<instance_id>",
        CreateProjectThumbnailResource,
    ),
    (
        "/pictures/thumbnails/projects/<instance_id>.png",
        ProjectThumbnailResource,
    ),
    (
        "/pictures/preview-background-files/<instance_id>",
        CreatePreviewBackgroundFileResource,
    ),
    (
        "/pictures/thumbnails/preview-background-files/<instance_id>.png",
        PreviewBackgroundFileThumbnailResource,
    ),
    (
        "/pictures/preview-background-files/<instance_id>.<extension>",
        PreviewBackgroundFileResource,
    ),
    (
        "/actions/preview-files/<preview_file_id>/set-main-preview",
        SetMainPreviewResource,
    ),
    (
        "/actions/preview-files/<preview_file_id>/extract-frame",
        ExtractFrameFromPreview,
    ),
    (
        "/actions/preview-files/<preview_file_id>/update-position",
        UpdatePreviewPositionResource,
    ),
    (
        "/actions/preview-files/<preview_file_id>/update-annotations",
        UpdateAnnotationsResource,
    ),
    (
        "/actions/preview-files/<preview_file_id>/extract-tile",
        ExtractTileFromPreview,
    ),
]
blueprint = Blueprint("thumbnails", "thumbnails")
api = configure_api_from_blueprint(blueprint, routes)
