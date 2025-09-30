#!/usr/bin/env python

# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Dialogflow API Python sample showing how to manage Conversations.
"""

import logging
from google.cloud import dialogflow_v2beta1 as dialogflow


# [START dialogflow_create_conversation]
def create_conversation(project_id, conversation_profile_id, conversation_id):
    """Creates a conversation with given values

    Args:
        project_id:  The GCP project linked with the conversation.
        conversation_profile_id: The conversation profile id used to create
        conversation."""

    client = dialogflow.ConversationsClient()
    conversation_profile_client = dialogflow.ConversationProfilesClient()
    project_path = client.common_project_path(project_id)
    conversation_profile_path = conversation_profile_client.conversation_profile_path(
        project_id, conversation_profile_id
    )

    conversation = {"conversation_profile": conversation_profile_path}
    request = dialogflow.CreateConversationRequest(
        parent=project_path, conversation=conversation, conversation_id=conversation_id
    )

    response = client.create_conversation(request=request)

    logging.info(f"lifecycle_state: {response.lifecycle_state}")
    logging.info(f"conversation_profile: {response.conversation_profile}")
    logging.info(f"name: {response.name}")
    return response

# [END dialogflow_create_conversation]

# [START dialogflow_get_conversation]
def get_conversation(project_id, conversation_id):
    """Gets a specific conversation profile.

    Args:
        project_id: The GCP project linked with the conversation.
        conversation_id: Id of the conversation."""

    client = dialogflow.ConversationsClient()
    conversation_path = client.conversation_path(project_id, conversation_id)

    response = client.get_conversation(name=conversation_path)

    logging.info(f"lifecycle_state: {response.lifecycle_state}")
    logging.info(f"conversation_profile: {response.conversation_profile}")
    logging.info(f"name: {response.name}")
    return response

# [END dialogflow_get_conversation]

# [START dialogflow_complete_conversation]
def complete_conversation(project_id, conversation_id):
    """
    Completes the specified conversation. Finished conversations
    are purged from the database after 30 days.

    Args:
        project_id: The GCP project linked with the conversation.
        conversation_id: Id of the conversation."""

    client = dialogflow.ConversationsClient()
    conversation_path = client.conversation_path(project_id, conversation_id)
    conversation = client.complete_conversation(name=conversation_path)
    logging.info("Completed Conversation.")
    logging.info(f"lifecycle_state: {conversation.lifecycle_state}")
    logging.info(f"conversation_profile: {conversation.conversation_profile}")
    logging.info(f"name: {conversation.name}")
    return conversation

# [END dialogflow_complete_conversation]
