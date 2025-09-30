from google.cloud import dialogflow_v2beta1
from google.api_core.client_options import ClientOptions
from google.cloud import storage

import time
import google.auth
import participant_management
import conversation_management

# At the time of this writing, this sample relies on an unreleased version of the dialogflow_v2beta1 python library:
# https://cloud.google.com/dialogflow/priv/docs/reference/libraries

PROJECT_ID="lucid-volt-361004"
CONVERSATION_PROFILE_ID="mHFMNCKQQa6YaBOdu1dp1w"
BUCKET_NAME="audio-experiments-798656365078"

# SAMPLE_RATE = 48000
SAMPLE_RATE = 24000
# Calculate the bytes with Sample_rate_hertz * bit Depth / 8 -> bytes
# 48000(sample/second) * 16(bits/sample) / 8 = 96000 byte per second,
# 96000 / 10 = 9600 we send 0.1 second to the stream API
POINT_ONE_SECOND_IN_BYTES = 9600
FOLDER_PTAH_FOR_CUSTOMER_AUDIO="audio/END_USER.wav"
FOLDER_PTAH_FOR_AGENT_AUDIO="audio/HUMAN_AGENT.wav"
client_options = ClientOptions(api_endpoint="dialogflow.googleapis.com")
credentials, _ = google.auth.default(scopes=["https://www.googleapis.com/auth/cloud-platform",
                                             "https://www.googleapis.com/auth/dialogflow"])

storage_client = storage.Client(credentials = credentials, project=PROJECT_ID)

participant_client = dialogflow_v2beta1.ParticipantsClient(client_options=client_options,
                                                           credentials=credentials)

def download_blob(bucket_name, folder_path, audio_array : list):
    """Uploads a file to the bucket."""
    bucket = storage_client.bucket(bucket_name, user_project=PROJECT_ID)
    blobs = bucket.list_blobs(prefix=folder_path)
    for blob in blobs:
      if not blob.name.endswith('/'):
          audio_array.append(blob.download_as_string())

def request_iterator(participant : dialogflow_v2beta1.Participant, audios):
    """Iterate the request for bidi streaming analyze content
    """
    yield dialogflow_v2beta1.BidiStreamingAnalyzeContentRequest(
        config={
            "participant": participant.name,
            "voice_session_config": {
                "input_audio_encoding": dialogflow_v2beta1.AudioEncoding.AUDIO_ENCODING_LINEAR_16,
                "input_audio_sample_rate_hertz": SAMPLE_RATE,
            },
        }
    )
    print(f"participant {participant}")

    for i in range(0, len(audios)):
      audios_array = audio_request_iterator(audios[i])
      for chunk in audios_array:
        if not chunk:
            break
        yield dialogflow_v2beta1.BidiStreamingAnalyzeContentRequest(
        input={
            "audio":chunk
            },
        )
        time.sleep(0.1)
    yield dialogflow_v2beta1.BidiStreamingAnalyzeContentRequest(
        config={
            "participant": participant.name,
        }
    )
    time.sleep(0.1)

def participant_bidi_streaming_analyze_content(participant, audios):
    """call bidi streaming analyze content API
    """
    bidi_responses = participant_client.bidi_streaming_analyze_content(
        requests=request_iterator(participant, audios)
    )

    for response in bidi_responses:
        bidi_streaming_analyze_content_response_handler(response)

def bidi_streaming_analyze_content_response_handler(response: dialogflow_v2beta1.BidiStreamingAnalyzeContentResponse):
    """Call Bidi Streaming Analyze Content
    """
    if  response.recognition_result:
         print(f"Recognition result: { response.recognition_result.transcript}", )

def audio_request_iterator(audio):
    """Iterate the request for bidi streaming analyze content
    """
    total_audio_length = len(audio)
    print(f"total audio length {total_audio_length}")
    array = []
    for i in range(0, total_audio_length, POINT_ONE_SECOND_IN_BYTES):
        chunk = audio[i : i + POINT_ONE_SECOND_IN_BYTES]
        array.append(chunk)
        if not chunk:
            break
    return array

def python_client_handler(conversation_id):
    """Downloads audios from the google cloud storage bucket and stream to
    the Bidi streaming AnalyzeContent site.
    """
    print("Start streaming")
    conversation = conversation_management.create_conversation(
        project_id=PROJECT_ID, conversation_profile_id=CONVERSATION_PROFILE_ID, conversation_id=conversation_id
    )
    conversation_id = conversation.name.split("conversations/")[1].rstrip()
    human_agent = human_agent = participant_management.create_participant(
        project_id=PROJECT_ID, conversation_id=conversation_id, role="HUMAN_AGENT"
    )

    end_user =    end_user = participant_management.create_participant(
        project_id=PROJECT_ID, conversation_id=conversation_id, role="END_USER"
    )

    end_user_requests = []
    agent_request= []
    download_blob(BUCKET_NAME, FOLDER_PTAH_FOR_CUSTOMER_AUDIO, end_user_requests)
    download_blob(BUCKET_NAME, FOLDER_PTAH_FOR_AGENT_AUDIO, agent_request)

    # print(conversation)
    # print(conversation_id)
    # print(human_agent)
    # print(end_user)

    participant_bidi_streaming_analyze_content( human_agent, agent_request)
    participant_bidi_streaming_analyze_content( end_user, end_user_requests)

    conversation_management.complete_conversation(PROJECT_ID, conversation_id)

python_client_handler(conversation_id="abc223456780")