#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
#
# Copyright (C) 2015-2021, Wazuh Inc.
# Created by Wazuh, Inc. <info@wazuh.com>.
# This program is free software; you can redistribute
# it and/or modify it under the terms of GPLv2

"""Unit tests for integration module."""

import os
import sys
from unittest.mock import patch

import pytest

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..'))  # noqa: E501
from integration import WazuhGCloudSubscriber

test_data_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                              'data')

credentials_file = 'credentials.json'
project = 'wazuh-dev'
subscription_id = 'testing'
test_message = 'test-message'.encode()


@patch('integration.pubsub.subscriber.Client.from_service_account_file')
def get_wazuhgcloud_subscriber(mock_client):
    """Return a WazuhGCloudSubscriber client."""
    client = WazuhGCloudSubscriber(credentials_file, project, subscription_id)
    return client


def test_get_subscriber():
    """Check if an instance of WazuhGCloudSubscriber is created properly."""
    expected_attributes = ['wazuh_path', 'wazuh_version', 'wazuh_queue',
                           'subscriber', 'subscription_path']

    client = get_wazuhgcloud_subscriber()

    assert isinstance(client, WazuhGCloudSubscriber)

    for attribute in expected_attributes:
        assert hasattr(client, attribute)


@patch('integration.socket.socket')
def test_send_message_ok(mock_socket):
    """Test if messages are sent to Wazuh queue socket."""
    client = get_wazuhgcloud_subscriber()
    client.send_message(test_message)


def test_send_message_ko():
    """Test send_message method when a socket exception happens."""
    with pytest.raises(OSError):
        client = get_wazuhgcloud_subscriber()
        client.send_message(test_message)


def test_format_msg():
    """Test if messages are formatted properly before to be sent."""
    client = get_wazuhgcloud_subscriber()
    formatted_message = client.format_msg(test_message)

    assert type(formatted_message) is str
