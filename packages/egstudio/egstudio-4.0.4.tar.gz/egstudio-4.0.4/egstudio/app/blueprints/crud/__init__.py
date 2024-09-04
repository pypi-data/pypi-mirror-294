from flask import Blueprint

from egstudio.app.utils.api import configure_api_from_blueprint

from egstudio.app.blueprints.crud.asset_instance import (
    AssetInstanceResource,
    AssetInstancesResource,
)
from egstudio.app.blueprints.crud.attachment_file import (
    AttachmentFilesResource,
    AttachmentFileResource,
)
from egstudio.app.blueprints.crud.comments import CommentsResource, CommentResource
from egstudio.app.blueprints.crud.custom_action import (
    CustomActionsResource,
    CustomActionResource,
)
from egstudio.app.blueprints.crud.status_automation import (
    StatusAutomationsResource,
    StatusAutomationResource,
)
from egstudio.app.blueprints.crud.day_off import DayOffsResource, DayOffResource
from egstudio.app.blueprints.crud.department import (
    DepartmentsResource,
    DepartmentResource,
)
from egstudio.app.blueprints.crud.entity import EntityResource, EntitiesResource
from egstudio.app.blueprints.crud.entity_type import (
    EntityTypesResource,
    EntityTypeResource,
)
from egstudio.app.blueprints.crud.entity_link import (
    EntityLinksResource,
    EntityLinkResource,
)
from egstudio.app.blueprints.crud.event import EventsResource, EventResource
from egstudio.app.blueprints.crud.file_status import (
    FileStatusesResource,
    FileStatusResource,
)
from egstudio.app.blueprints.crud.metadata_descriptor import (
    MetadataDescriptorsResource,
    MetadataDescriptorResource,
)
from egstudio.app.blueprints.crud.milestone import (
    MilestonesResource,
    MilestoneResource,
)
from egstudio.app.blueprints.crud.notification import (
    NotificationsResource,
    NotificationResource,
)
from egstudio.app.blueprints.crud.organisation import (
    OrganisationsResource,
    OrganisationResource,
)
from egstudio.app.blueprints.crud.output_file import (
    OutputFilesResource,
    OutputFileResource,
)
from egstudio.app.blueprints.crud.output_type import (
    OutputTypeResource,
    OutputTypesResource,
)
from egstudio.app.blueprints.crud.news import NewssResource, NewsResource
from egstudio.app.blueprints.crud.person import PersonResource, PersonsResource
from egstudio.app.blueprints.crud.preview_file import (
    PreviewFilesResource,
    PreviewFileResource,
)
from egstudio.app.blueprints.crud.playlist import (
    PlaylistsResource,
    PlaylistResource,
)
from egstudio.app.blueprints.crud.project import (
    ProjectResource,
    ProjectsResource,
    ProjectTaskTypeLinksResource,
)
from egstudio.app.blueprints.crud.project_status import (
    ProjectStatusResource,
    ProjectStatussResource,
)
from egstudio.app.blueprints.crud.schedule_item import (
    ScheduleItemsResource,
    ScheduleItemResource,
)
from egstudio.app.blueprints.crud.subscription import (
    SubscriptionsResource,
    SubscriptionResource,
)
from egstudio.app.blueprints.crud.search_filter import (
    SearchFiltersResource,
    SearchFilterResource,
)
from egstudio.app.blueprints.crud.search_filter_group import (
    SearchFilterGroupsResource,
    SearchFilterGroupResource,
)
from egstudio.app.blueprints.crud.software import (
    SoftwaresResource,
    SoftwareResource,
)
from egstudio.app.blueprints.crud.task_type import (
    TaskTypesResource,
    TaskTypeResource,
)
from egstudio.app.blueprints.crud.task_status import (
    TaskStatusesResource,
    TaskStatusResource,
)
from egstudio.app.blueprints.crud.task import TasksResource, TaskResource
from egstudio.app.blueprints.crud.time_spent import (
    TimeSpentsResource,
    TimeSpentResource,
)
from egstudio.app.blueprints.crud.working_file import (
    WorkingFilesResource,
    WorkingFileResource,
)
from egstudio.app.blueprints.crud.preview_background_file import (
    PreviewBackgroundFileResource,
    PreviewBackgroundFilesResource,
)

routes = [
    ("/data/persons", PersonsResource),
    ("/data/persons/<instance_id>", PersonResource),
    ("/data/projects", ProjectsResource),
    ("/data/projects/<instance_id>", ProjectResource),
    ("/data/project-status", ProjectStatussResource),
    ("/data/project-status/<instance_id>", ProjectStatusResource),
    ("/data/entity-types", EntityTypesResource),
    ("/data/entity-types/<instance_id>", EntityTypeResource),
    ("/data/entities", EntitiesResource),
    ("/data/entities/<instance_id>", EntityResource),
    ("/data/task-types", TaskTypesResource),
    ("/data/task-types/<instance_id>", TaskTypeResource),
    ("/data/task-type-links", ProjectTaskTypeLinksResource),
    ("/data/task-status", TaskStatusesResource),
    ("/data/task-status/<instance_id>", TaskStatusResource),
    ("/data/tasks", TasksResource),
    ("/data/tasks/<instance_id>", TaskResource),
    ("/data/departments", DepartmentsResource),
    ("/data/departments/<instance_id>", DepartmentResource),
    ("/data/organisations", OrganisationsResource),
    ("/data/organisations/<instance_id>", OrganisationResource),
    ("/data/file-status/", FileStatusesResource),
    ("/data/file-status/<instance_id>", FileStatusResource),
    ("/data/softwares", SoftwaresResource),
    ("/data/softwares/<instance_id>", SoftwareResource),
    ("/data/output-files", OutputFilesResource),
    ("/data/output-files/<instance_id>", OutputFileResource),
    ("/data/output-types", OutputTypesResource),
    ("/data/output-types/<instance_id>", OutputTypeResource),
    ("/data/preview-files", PreviewFilesResource),
    ("/data/preview-files/<instance_id>", PreviewFileResource),
    ("/data/working-files", WorkingFilesResource),
    ("/data/working-files/<instance_id>", WorkingFileResource),
    ("/data/attachment-files", AttachmentFilesResource),
    ("/data/attachment-files/<instance_id>", AttachmentFileResource),
    ("/data/comments", CommentsResource),
    ("/data/comments/<instance_id>", CommentResource),
    ("/data/time-spents/", TimeSpentsResource),
    ("/data/time-spents/<instance_id>", TimeSpentResource),
    ("/data/day-offs/", DayOffsResource),
    ("/data/day-offs/<instance_id>", DayOffResource),
    ("/data/custom-actions/", CustomActionsResource),
    ("/data/custom-actions/<instance_id>", CustomActionResource),
    ("/data/status-automations/", StatusAutomationsResource),
    ("/data/status-automations/<instance_id>", StatusAutomationResource),
    ("/data/asset-instances/", AssetInstancesResource),
    ("/data/asset-instances/<instance_id>", AssetInstanceResource),
    ("/data/playlists/", PlaylistsResource),
    ("/data/playlists/<instance_id>", PlaylistResource),
    ("/data/events/", EventsResource),
    ("/data/events/<instance_id>", EventResource),
    ("/data/notifications/", NotificationsResource),
    ("/data/notifications/<instance_id>", NotificationResource),
    ("/data/search-filters/", SearchFiltersResource),
    ("/data/search-filters/<instance_id>", SearchFilterResource),
    ("/data/search-filter-groups/", SearchFilterGroupsResource),
    ("/data/search-filter-groups/<instance_id>", SearchFilterGroupResource),
    ("/data/schedule-items/", ScheduleItemsResource),
    ("/data/schedule-items/<instance_id>", ScheduleItemResource),
    ("/data/news/", NewssResource),
    ("/data/news/<instance_id>", NewsResource),
    ("/data/milestones/", MilestonesResource),
    ("/data/milestones/<instance_id>", MilestoneResource),
    ("/data/metadata-descriptors/", MetadataDescriptorsResource),
    ("/data/metadata-descriptors/<instance_id>", MetadataDescriptorResource),
    ("/data/subscriptions/", SubscriptionsResource),
    ("/data/subscriptions/<instance_id>", SubscriptionResource),
    ("/data/entity-links/", EntityLinksResource),
    ("/data/entity-links/<instance_id>", EntityLinkResource),
    ("/data/preview-background-files", PreviewBackgroundFilesResource),
    (
        "/data/preview-background-files/<instance_id>",
        PreviewBackgroundFileResource,
    ),
]

blueprint = Blueprint("/data", "data")
api = configure_api_from_blueprint(blueprint, routes)
