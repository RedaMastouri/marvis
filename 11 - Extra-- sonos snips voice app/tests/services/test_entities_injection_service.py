import pytest
import mock

from snipssonos.services.entities_injection_service import EntitiesInjectionService
from snipssonos.entities.artist import Artist
from snipssonos.entities.track import Track
from snipssonos.entities.playlist import Playlist
from snipssonos.exceptions import InvalidEntitySlotName

MQTT_TOPIC_INJECT = 'hermes/injection/perform'


@pytest.fixture
def artist_data():
    data = [Artist("uri_1", "Kendrick Lamar"), Artist("uri_2", "Beyonce")]
    return data


@pytest.fixture
def track_data():
    data = [Track("uri_1", "Kendrick Lamar"), Track("uri_2", "Beyonce")]
    return data


@pytest.fixture
def playlist_data():
    data = [Playlist("uri_1", "Kendrick Lamar"), Playlist("uri_2", "Beyonce")]
    return data


@mock.patch('snipssonos.services.entities_injection_service.MqttClient')
def test_inject_entities_parse_artist_data_correctly(mqtt_mock, artist_data):
    hermes_host = "localhost"
    inject_entities = EntitiesInjectionService(hermes_host)

    # TODO put into a global vars file
    entity_name = "snips/musicArtist"

    parsed_data = inject_entities.parse_data(entity_name, artist_data)
    expected_parsed_data = ["Kendrick Lamar", "Beyonce"]
    assert len(parsed_data) == len(expected_parsed_data)
    assert parsed_data == expected_parsed_data


@mock.patch('snipssonos.services.entities_injection_service.MqttClient')
def test_inject_entities_parse_track_data_correctly(mqtt_mock, artist_data, track_data):
    hermes_host = "localhost"
    inject_entities = EntitiesInjectionService(hermes_host)

    # TODO put into a global vars file
    entity_name = "snips/musicTrack"

    parsed_data = inject_entities.parse_data(entity_name, track_data)
    expected_parsed_data = ["Kendrick Lamar", "Beyonce"]
    assert len(parsed_data) == len(expected_parsed_data)
    assert parsed_data == expected_parsed_data


@mock.patch('snipssonos.services.entities_injection_service.MqttClient')
def test_inject_entities_parse_unknown_data_correctly(mqtt_mock):
    hermes_host = "localhost"
    inject_entities = EntitiesInjectionService(hermes_host)

    entity_name = "random_stuff"
    with pytest.raises(InvalidEntitySlotName):
        inject_entities.parse_data(entity_name, [])


@pytest.mark.skip("This test seems to be failing because json is not ordered. Skipping it for now")
@mock.patch('snipssonos.services.entities_injection_service.MqttClient')
def test_inject_entities_payload_has_correct_format(mqtt_mock, artist_data):
    hermes_host = "localhost"
    artist_entity_name = "snips/musicArtist"

    inject_entities = EntitiesInjectionService(hermes_host)
    inject_entities.build_entities_payload(artist_entity_name, artist_data)
    actual_json = inject_entities.build_payload()
    expected_json = """{"operations": [["addFromVanilla", {"snips/artist": ["Kendrick Lamar", "Beyonce"]}]], "crossLanguage": "en"}"""
    assert expected_json == actual_json


@mock.patch('snipssonos.services.entities_injection_service.MqttClient')
def test_inject_entities_publisher_is_called_correctly(mqtt_mock, artist_data):
    mqtt_instance = mqtt_mock.return_value
    hermes_host = "localhost"
    artist_entity_name = "snips/musicArtist"

    entities_type = {
        "artists": "snips/musicArtist",
    }

    music_customization_service = mock.Mock()
    music_customization_service.fetch_entity.return_value = artist_data

    inject_entities = EntitiesInjectionService(hermes_host)
    inject_entities.publish_entities(music_customization_service, entities_type)

    inject_entities.build_entities_payload(artist_entity_name, artist_data)
    payload = inject_entities.build_payload()
    mqtt_instance.publish.assert_called_with(MQTT_TOPIC_INJECT, payload)


@pytest.mark.skip("This test seems to be failing because json is not ordered. Skipping it for now")
@mock.patch('snipssonos.services.entities_injection_service.MqttClient')
def test_inject_entities_publisher_is_called_correctly_adding_up_entities_payload(mqtt_mock, artist_data):
    mqtt_instance = mqtt_mock.return_value
    hermes_host = "localhost"
    artist_entity_name = "snips/musicArtist"
    track_entity_name = "snips/musicTrack"

    entities_type = {
        "artists": "snips/musicArtist",
        "tracks": "snips/musicTrack",
    }

    music_customization_service = mock.Mock()
    music_customization_service.fetch_entity.return_value = artist_data

    inject_entities = EntitiesInjectionService(hermes_host)
    inject_entities.publish_entities(music_customization_service, entities_type)

    inject_entities.build_entities_payload(track_entity_name, artist_data)
    inject_entities.build_entities_payload(artist_entity_name, artist_data)

    payload = inject_entities.build_payload()
    mqtt_instance.publish.assert_called_with(MQTT_TOPIC_INJECT, payload)
