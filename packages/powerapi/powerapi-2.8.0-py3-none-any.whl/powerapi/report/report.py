# Copyright (c) 2021, INRIA
# Copyright (c) 2021, University of Lille
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# * Neither the name of the copyright holder nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from __future__ import annotations

from datetime import datetime
from typing import Dict, NewType, Tuple, List, Any
from powerapi.exception import PowerAPIExceptionWithMessage, PowerAPIException
from powerapi.message import Message

TIMESTAMP_KEY = 'timestamp'
SENSOR_KEY = 'sensor'
TARGET_KEY = 'target'
METADATA_KEY = 'metadata'
GROUPS_KEY = 'groups'

CSV_HEADER_COMMON = [TIMESTAMP_KEY, SENSOR_KEY, TARGET_KEY]
CsvLines = NewType('CsvLines', Tuple[List[str], Dict[str, str]])


class BadInputData(PowerAPIExceptionWithMessage):
    """
    Exception raised when input data can't be converted to a Report
    """

    def __init__(self, msg, input_data):
        PowerAPIExceptionWithMessage.__init__(self, msg)
        self.input_data = input_data


class DeserializationFail(PowerAPIException):
    """
    Exception raised when the
    in the good format
    """


class Report(Message):
    """
    Report abtract class.
    """

    def __init__(self, timestamp: datetime, sensor: str, target: str, metadata: Dict[str, Any] = {}):
        """
        Initialize a report using the given parameters.
        :param datetime timestamp: Timestamp
        :param str sensor: Sensor name.
        :param str target: Target name.
        """
        Message.__init__(self, None)
        self.timestamp = timestamp
        self.sensor = sensor
        self.target = target
        self.metadata = dict(metadata)

        #: id given by the dispatcher actor in order manage report order
        self.dispatcher_report_id = None

    def __str__(self):
        return '%s(%s, %s, %s)' % (self.__class__.__name__, self.timestamp, self.sensor, self.target)

    def __repr__(self):
        return '%s(%s, %s, %s)' % (self.__class__.__name__, self.timestamp, self.sensor, self.target)

    def __eq__(self, other):
        return (isinstance(other, type(self)) and
                self.timestamp == other.timestamp and
                self.sensor == other.sensor and
                self.target == other.target and
                self.metadata == other.metadata)

    @staticmethod
    def to_json(report: Report) -> Dict:
        """
        :return: a json dictionary, that can be converted into json format, from a given Report
        """
        json = report.__dict__
        # sender_name and dispatcher_report_id are not used
        json.pop('sender_name')
        json.pop('dispatcher_report_id')

        return json

    @staticmethod
    def _extract_timestamp(ts):
        # Unix timestamp format (in milliseconds)
        if isinstance(ts, int):
            return datetime.fromtimestamp(ts / 1000)

        # datetime object
        if isinstance(ts, datetime):
            return ts

        if isinstance(ts, str):
            try:
                # ISO 8601 date format
                return datetime.strptime(ts, "%Y-%m-%dT%H:%M:%S.%f")
            except ValueError:
                # Unix timestamp format (in milliseconds)
                return datetime.fromtimestamp(int(ts) / 1000)

        raise ValueError('Invalid timestamp format')

    @staticmethod
    def create_empty_report():
        """
        Creates an empty report
        """
        return Report(None, None, None)
