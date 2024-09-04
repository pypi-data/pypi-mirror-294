"""
Type annotations for medialive service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_medialive.client import MediaLiveClient
    from mypy_boto3_medialive.paginator import (
        DescribeSchedulePaginator,
        ListChannelsPaginator,
        ListCloudWatchAlarmTemplateGroupsPaginator,
        ListCloudWatchAlarmTemplatesPaginator,
        ListEventBridgeRuleTemplateGroupsPaginator,
        ListEventBridgeRuleTemplatesPaginator,
        ListInputDeviceTransfersPaginator,
        ListInputDevicesPaginator,
        ListInputSecurityGroupsPaginator,
        ListInputsPaginator,
        ListMultiplexProgramsPaginator,
        ListMultiplexesPaginator,
        ListOfferingsPaginator,
        ListReservationsPaginator,
        ListSignalMapsPaginator,
    )

    session = Session()
    client: MediaLiveClient = session.client("medialive")

    describe_schedule_paginator: DescribeSchedulePaginator = client.get_paginator("describe_schedule")
    list_channels_paginator: ListChannelsPaginator = client.get_paginator("list_channels")
    list_cloud_watch_alarm_template_groups_paginator: ListCloudWatchAlarmTemplateGroupsPaginator = client.get_paginator("list_cloud_watch_alarm_template_groups")
    list_cloud_watch_alarm_templates_paginator: ListCloudWatchAlarmTemplatesPaginator = client.get_paginator("list_cloud_watch_alarm_templates")
    list_event_bridge_rule_template_groups_paginator: ListEventBridgeRuleTemplateGroupsPaginator = client.get_paginator("list_event_bridge_rule_template_groups")
    list_event_bridge_rule_templates_paginator: ListEventBridgeRuleTemplatesPaginator = client.get_paginator("list_event_bridge_rule_templates")
    list_input_device_transfers_paginator: ListInputDeviceTransfersPaginator = client.get_paginator("list_input_device_transfers")
    list_input_devices_paginator: ListInputDevicesPaginator = client.get_paginator("list_input_devices")
    list_input_security_groups_paginator: ListInputSecurityGroupsPaginator = client.get_paginator("list_input_security_groups")
    list_inputs_paginator: ListInputsPaginator = client.get_paginator("list_inputs")
    list_multiplex_programs_paginator: ListMultiplexProgramsPaginator = client.get_paginator("list_multiplex_programs")
    list_multiplexes_paginator: ListMultiplexesPaginator = client.get_paginator("list_multiplexes")
    list_offerings_paginator: ListOfferingsPaginator = client.get_paginator("list_offerings")
    list_reservations_paginator: ListReservationsPaginator = client.get_paginator("list_reservations")
    list_signal_maps_paginator: ListSignalMapsPaginator = client.get_paginator("list_signal_maps")
    ```
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    DescribeScheduleRequestDescribeSchedulePaginateTypeDef,
    DescribeScheduleResponseTypeDef,
    ListChannelsRequestListChannelsPaginateTypeDef,
    ListChannelsResponseTypeDef,
    ListCloudWatchAlarmTemplateGroupsRequestListCloudWatchAlarmTemplateGroupsPaginateTypeDef,
    ListCloudWatchAlarmTemplateGroupsResponseTypeDef,
    ListCloudWatchAlarmTemplatesRequestListCloudWatchAlarmTemplatesPaginateTypeDef,
    ListCloudWatchAlarmTemplatesResponseTypeDef,
    ListEventBridgeRuleTemplateGroupsRequestListEventBridgeRuleTemplateGroupsPaginateTypeDef,
    ListEventBridgeRuleTemplateGroupsResponseTypeDef,
    ListEventBridgeRuleTemplatesRequestListEventBridgeRuleTemplatesPaginateTypeDef,
    ListEventBridgeRuleTemplatesResponseTypeDef,
    ListInputDevicesRequestListInputDevicesPaginateTypeDef,
    ListInputDevicesResponseTypeDef,
    ListInputDeviceTransfersRequestListInputDeviceTransfersPaginateTypeDef,
    ListInputDeviceTransfersResponseTypeDef,
    ListInputSecurityGroupsRequestListInputSecurityGroupsPaginateTypeDef,
    ListInputSecurityGroupsResponseTypeDef,
    ListInputsRequestListInputsPaginateTypeDef,
    ListInputsResponseTypeDef,
    ListMultiplexesRequestListMultiplexesPaginateTypeDef,
    ListMultiplexesResponseTypeDef,
    ListMultiplexProgramsRequestListMultiplexProgramsPaginateTypeDef,
    ListMultiplexProgramsResponseTypeDef,
    ListOfferingsRequestListOfferingsPaginateTypeDef,
    ListOfferingsResponseTypeDef,
    ListReservationsRequestListReservationsPaginateTypeDef,
    ListReservationsResponseTypeDef,
    ListSignalMapsRequestListSignalMapsPaginateTypeDef,
    ListSignalMapsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "DescribeSchedulePaginator",
    "ListChannelsPaginator",
    "ListCloudWatchAlarmTemplateGroupsPaginator",
    "ListCloudWatchAlarmTemplatesPaginator",
    "ListEventBridgeRuleTemplateGroupsPaginator",
    "ListEventBridgeRuleTemplatesPaginator",
    "ListInputDeviceTransfersPaginator",
    "ListInputDevicesPaginator",
    "ListInputSecurityGroupsPaginator",
    "ListInputsPaginator",
    "ListMultiplexProgramsPaginator",
    "ListMultiplexesPaginator",
    "ListOfferingsPaginator",
    "ListReservationsPaginator",
    "ListSignalMapsPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class DescribeSchedulePaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Paginator.DescribeSchedule)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/paginators/#describeschedulepaginator)
    """
    def paginate(
        self, **kwargs: Unpack[DescribeScheduleRequestDescribeSchedulePaginateTypeDef]
    ) -> _PageIterator[DescribeScheduleResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Paginator.DescribeSchedule.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/paginators/#describeschedulepaginator)
        """

class ListChannelsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Paginator.ListChannels)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/paginators/#listchannelspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListChannelsRequestListChannelsPaginateTypeDef]
    ) -> _PageIterator[ListChannelsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Paginator.ListChannels.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/paginators/#listchannelspaginator)
        """

class ListCloudWatchAlarmTemplateGroupsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Paginator.ListCloudWatchAlarmTemplateGroups)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/paginators/#listcloudwatchalarmtemplategroupspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListCloudWatchAlarmTemplateGroupsRequestListCloudWatchAlarmTemplateGroupsPaginateTypeDef
        ],
    ) -> _PageIterator[ListCloudWatchAlarmTemplateGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Paginator.ListCloudWatchAlarmTemplateGroups.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/paginators/#listcloudwatchalarmtemplategroupspaginator)
        """

class ListCloudWatchAlarmTemplatesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Paginator.ListCloudWatchAlarmTemplates)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/paginators/#listcloudwatchalarmtemplatespaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListCloudWatchAlarmTemplatesRequestListCloudWatchAlarmTemplatesPaginateTypeDef
        ],
    ) -> _PageIterator[ListCloudWatchAlarmTemplatesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Paginator.ListCloudWatchAlarmTemplates.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/paginators/#listcloudwatchalarmtemplatespaginator)
        """

class ListEventBridgeRuleTemplateGroupsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Paginator.ListEventBridgeRuleTemplateGroups)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/paginators/#listeventbridgeruletemplategroupspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListEventBridgeRuleTemplateGroupsRequestListEventBridgeRuleTemplateGroupsPaginateTypeDef
        ],
    ) -> _PageIterator[ListEventBridgeRuleTemplateGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Paginator.ListEventBridgeRuleTemplateGroups.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/paginators/#listeventbridgeruletemplategroupspaginator)
        """

class ListEventBridgeRuleTemplatesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Paginator.ListEventBridgeRuleTemplates)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/paginators/#listeventbridgeruletemplatespaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListEventBridgeRuleTemplatesRequestListEventBridgeRuleTemplatesPaginateTypeDef
        ],
    ) -> _PageIterator[ListEventBridgeRuleTemplatesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Paginator.ListEventBridgeRuleTemplates.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/paginators/#listeventbridgeruletemplatespaginator)
        """

class ListInputDeviceTransfersPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Paginator.ListInputDeviceTransfers)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/paginators/#listinputdevicetransferspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[ListInputDeviceTransfersRequestListInputDeviceTransfersPaginateTypeDef],
    ) -> _PageIterator[ListInputDeviceTransfersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Paginator.ListInputDeviceTransfers.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/paginators/#listinputdevicetransferspaginator)
        """

class ListInputDevicesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Paginator.ListInputDevices)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/paginators/#listinputdevicespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListInputDevicesRequestListInputDevicesPaginateTypeDef]
    ) -> _PageIterator[ListInputDevicesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Paginator.ListInputDevices.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/paginators/#listinputdevicespaginator)
        """

class ListInputSecurityGroupsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Paginator.ListInputSecurityGroups)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/paginators/#listinputsecuritygroupspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListInputSecurityGroupsRequestListInputSecurityGroupsPaginateTypeDef]
    ) -> _PageIterator[ListInputSecurityGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Paginator.ListInputSecurityGroups.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/paginators/#listinputsecuritygroupspaginator)
        """

class ListInputsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Paginator.ListInputs)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/paginators/#listinputspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListInputsRequestListInputsPaginateTypeDef]
    ) -> _PageIterator[ListInputsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Paginator.ListInputs.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/paginators/#listinputspaginator)
        """

class ListMultiplexProgramsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Paginator.ListMultiplexPrograms)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/paginators/#listmultiplexprogramspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListMultiplexProgramsRequestListMultiplexProgramsPaginateTypeDef]
    ) -> _PageIterator[ListMultiplexProgramsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Paginator.ListMultiplexPrograms.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/paginators/#listmultiplexprogramspaginator)
        """

class ListMultiplexesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Paginator.ListMultiplexes)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/paginators/#listmultiplexespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListMultiplexesRequestListMultiplexesPaginateTypeDef]
    ) -> _PageIterator[ListMultiplexesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Paginator.ListMultiplexes.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/paginators/#listmultiplexespaginator)
        """

class ListOfferingsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Paginator.ListOfferings)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/paginators/#listofferingspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListOfferingsRequestListOfferingsPaginateTypeDef]
    ) -> _PageIterator[ListOfferingsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Paginator.ListOfferings.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/paginators/#listofferingspaginator)
        """

class ListReservationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Paginator.ListReservations)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/paginators/#listreservationspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListReservationsRequestListReservationsPaginateTypeDef]
    ) -> _PageIterator[ListReservationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Paginator.ListReservations.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/paginators/#listreservationspaginator)
        """

class ListSignalMapsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Paginator.ListSignalMaps)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/paginators/#listsignalmapspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListSignalMapsRequestListSignalMapsPaginateTypeDef]
    ) -> _PageIterator[ListSignalMapsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive.html#MediaLive.Paginator.ListSignalMaps.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_medialive/paginators/#listsignalmapspaginator)
        """
