#  Copyright 2023 Synnax Labs, Inc.
#
#  Use of this software is governed by the Business Source License included in the file
#  licenses/BSL.txt.
#
#  As of the Change Date specified in that file, in accordance with the Business Source
#  License, use of this software will be governed by the Apache License, Version 2.0,
#  included in the file licenses/APL.txt.

from typing import overload

import pandas as pd
from alamos import NOOP, Instrumentation
from freighter import AsyncStreamClient, StreamClient, UnaryClient

from synnax.channel.payload import (
    ChannelKey,
    ChannelKeys,
    ChannelName,
    ChannelNames,
    ChannelParams,
    ChannelPayload,
    normalize_channel_params,
)
from synnax.channel.retrieve import ChannelRetriever
from synnax.exceptions import QueryError
from synnax.framer.adapter import ReadFrameAdapter, WriteFrameAdapter
from synnax.framer.frame import Frame, CrudeFrame
from synnax.framer.iterator import Iterator
from synnax.framer.streamer import AsyncStreamer, Streamer
from synnax.framer.writer import Writer, WriterMode, CrudeWriterMode
from synnax.framer.deleter import Deleter
from synnax.telem import CrudeTimeStamp, Series, TimeRange, TimeSpan, CrudeSeries
from synnax.telem.control import Authority, CrudeAuthority


class Client:
    """SegmentClient provides interfaces for reading and writing segmented
    telemetry from a Synnax Cluster. SegmentClient should not be instantiated
    directly, but rather used through the synnax.Synnax class.
    """

    __stream_client: StreamClient
    __async_client: AsyncStreamClient
    __unary_client: UnaryClient
    __channels: ChannelRetriever
    __deleter: Deleter
    instrumentation: Instrumentation

    def __init__(
        self,
        stream_client: StreamClient,
        async_client: AsyncStreamClient,
        unary_client: UnaryClient,
        retriever: ChannelRetriever,
        deleter: Deleter,
        instrumentation: Instrumentation = NOOP,
    ):
        self.__stream_client = stream_client
        self.__async_client = async_client
        self.__unary_client = unary_client
        self.__channels = retriever
        self.__deleter = deleter
        self.instrumentation = instrumentation

    def open_writer(
        self,
        start: CrudeTimeStamp,
        channels: ChannelParams,
        authorities: CrudeAuthority | list[CrudeAuthority] = Authority.ABSOLUTE,
        *,
        name: str = "",
        strict: bool = False,
        suppress_warnings: bool = False,
        mode: CrudeWriterMode = WriterMode.PERSIST_STREAM,
        err_on_unauthorized: bool = False,
        enable_auto_commit: bool = False,
        auto_index_persist_interval: TimeSpan = 1 * TimeSpan.SECOND,
        err_on_extra_chans: bool = True,
    ) -> Writer:
        """Opens a new writer on the given channels.

        :param start: Sets the starting timestamp for the first sample in the writer. If
        this timestamp overlaps with existing data for ANY of the provided channels,
        the writer will fail to open.
        :param channels: The channels to write to. This can be a single channel name,
        a list of channel names, a single channel key, or a list of channel keys.
        :param authorities: The control authority to set for each channel on the writer.
        Defaults to absolute authority. If not working with concurrent control,
        it's best to leave this as the default.
        :param name: The name of the writer used in control subject.
        :param strict: Sets whether the writer will fail to write if the data for a
        particular channel does not exactly match this data type. When False,
        the default, the writer will automatically convert the data to the correct
        type if possible.
        :param suppress_warnings: Suppress various print warnings that may be emitted
        by the writer.
        :param mode: sets the persistence and streaming mode of the writer. The default
        mode is WriterModePersistStream. See the WriterMode documentation for more.
        :param err_on_unauthorized: sets whether the writer should return an error if
        it attempts to write to a channel it does not have control over.
        :param enable_auto_commit: determines whether the writer will automatically
        commit. If enable_auto_commit is true, then the writer will commit after each
        write, and will flush that commit to index after the specified
        auto_index_persist_interval.
        :param auto_index_persist_interval: interval at which commits to the index will
        be persisted. To persist every commit to guarantee minimal loss of data, set
        auto_index_persist_interval to AlwaysAutoIndexPersist.
        """
        adapter = WriteFrameAdapter(self.__channels, err_on_extra_chans)
        adapter.update(channels)
        return Writer(
            start=start,
            adapter=adapter,
            client=self.__stream_client,
            strict=strict,
            suppress_warnings=suppress_warnings,
            authorities=authorities,
            name=name,
            mode=mode,
            err_on_unauthorized=err_on_unauthorized,
            enable_auto_commit=enable_auto_commit,
            auto_index_persist_interval=auto_index_persist_interval,
        )

    def open_iterator(
        self,
        tr: TimeRange,
        params: ChannelParams,
        chunk_size: int = 1e5,
    ) -> Iterator:
        """Opens a new iterator over the given channels within the provided time range.

        :param params: A list of channel keys to iterator over.
        :param tr: A time range to iterate over.
        :param chunk_size: The number of samples to read in a chunk with AutoSpan. Defaults to 100000
        :returns: An Iterator over the given channels within the provided time
        range. See the Iterator documentation for more.
        """
        adapter = ReadFrameAdapter(self.__channels)
        adapter.update(params)
        return Iterator(
            tr=tr,
            adapter=adapter,
            client=self.__stream_client,
            chunk_size=chunk_size,
            instrumentation=self.instrumentation,
        )

    @overload
    def write(
        self,
        start: CrudeTimeStamp,
        frame: CrudeFrame,
        strict: bool = False,
    ):
        ...

    @overload
    def write(
        self,
        start: CrudeTimeStamp,
        to: ChannelKey | ChannelName | ChannelPayload,
        data: CrudeSeries,
        strict: bool = False,
    ):
        """Writes telemetry to the given channel starting at the given timestamp.

        :param to: The key of the channel to write to.
        :param start: The starting timestamp of the first sample in data.
        :param data: The telemetry to write to the channel.
        :returns: None.
        """
        ...

    @overload
    def write(
        self,
        start: CrudeTimeStamp,
        to: ChannelKeys | ChannelNames | list[ChannelPayload],
        series: list[CrudeSeries],
        strict: bool = False,
    ):
        ...

    def write(
        self,
        start: CrudeTimeStamp,
        to: ChannelParams | ChannelPayload | list[ChannelPayload] | CrudeFrame,
        series: CrudeSeries | list[CrudeSeries] | None = None,
        strict: bool = False,
    ):
        channels = list()
        if isinstance(to, (list, ChannelKey, ChannelPayload, ChannelName)):
            channels = to
        elif isinstance(to, dict):
            channels = list(to.keys())
        elif isinstance(to, Frame):
            channels = to.channels
        elif isinstance(to, pd.DataFrame):
            channels = list(to.columns)
        with self.open_writer(
            start=start,
            channels=channels,
            strict=strict,
            mode=WriterMode.PERSIST,
            err_on_unauthorized=True,
            enable_auto_commit=True,
            auto_index_persist_interval=TimeSpan.MAX,
        ) as w:
            w.write(to, series)

    @overload
    def read(
        self,
        tr: TimeRange,
        params: ChannelKeys | ChannelNames,
    ) -> Frame:
        ...

    @overload
    def read(
        self,
        tr: TimeRange,
        params: ChannelKey | ChannelName,
    ) -> Series:
        ...

    def read(
        self,
        tr: TimeRange,
        params: ChannelParams,
    ) -> Series | Frame:
        """
        Reads telemetry from the channel between the two timestamps.

        :param tr: The time range to read from.
        :param params: The key or name of the channel to read from.

        :returns: A tuple where the first item is a numpy array containing the telemetry
        and the second item is the time range occupied by that array.

        :raises ContiguityError: If the telemetry between start and end is
        non-contiguous.
        """
        normal = normalize_channel_params(params)
        frame = self.__read_frame(tr, params)
        if len(normal.params) > 1:
            return frame
        series = frame.get(normal.params[0], None)
        if series is None:
            raise QueryError(
                f"""No data found for channel {normal.params[0]} between {tr}"""
            )
        return series

    def open_streamer(
        self,
        params: ChannelParams,
        from_: CrudeTimeStamp | None = None,
    ) -> Streamer:
        adapter = ReadFrameAdapter(self.__channels)
        adapter.update(params)
        return Streamer(
            from_=from_,
            adapter=adapter,
            client=self.__stream_client,
        )

    async def open_async_streamer(
        self,
        params: ChannelParams,
        from_: CrudeTimeStamp | None = None,
    ) -> AsyncStreamer:
        adapter = ReadFrameAdapter(self.__channels)
        adapter.update(params)
        s = AsyncStreamer(
            from_=from_,
            adapter=adapter,
            client=self.__async_client,
        )
        await s.open()
        return s

    def delete(self, channels: ChannelParams, tr: TimeRange) -> None:
        """
        delete deletes data in the specified channels in the specified time range.
        Note that the time range is start-inclusive and end-exclusive.
        Also note that deleting all data in a channel does not delete the channel; to
        delete a channel, use client.channels.delete().
        :param channels: channels to delete data from.
        :param tr: time range to delete data from.
        """
        self.__deleter.delete(channels, tr)

    def __read_frame(
        self,
        tr: TimeRange,
        params: ChannelParams,
    ) -> Frame:
        aggregate = Frame()
        with self.open_iterator(tr, params) as it:
            for fr in it:
                aggregate.append(fr)
        return aggregate
