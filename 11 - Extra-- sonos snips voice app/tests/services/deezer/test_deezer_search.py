import mock, pytest
import requests

from snipssonos.entities.album import Album
from snipssonos.entities.artist import Artist
from snipssonos.entities.device import Device
from snipssonos.entities.track import Track
from snipssonos.services.deezer.music_search_and_play_service import DeezerMusicSearchService
from snipssonos.services.node.query_builder import NodeQueryBuilder
from snipssonos.exceptions import MusicSearchProviderConnectionError

BASE_ENDPOINT = "http://localhost:5005"


@pytest.fixture
def connected_device():
    return Device(
        name="Anthony's Sonos",
        identifier="RINCON_XXXX",
        volume=10
    )


@pytest.fixture
def deezer_music_search_service():
    connected_device = Device(
        name="Anthony's Sonos",
        identifier="RINCON_XXXX",
        volume=10
    )

    mock_device_discovery_service = mock.Mock()
    mock_device_discovery_service.get.return_value = connected_device
    deezer = DeezerMusicSearchService(mock_device_discovery_service)
    return deezer


@mock.patch('snipssonos.services.deezer.music_search_and_play_service.requests.Response')
@mock.patch('snipssonos.services.deezer.music_search_and_play_service.requests')
def test_music_search_provider_raises_exception_for_wrong_query_to_deezer_api(mock_requests, mock_response,
                                                                              deezer_music_search_service):
    mock_response.ok = False
    mock_requests.get.return_value = mock_response

    search_query = deezer_music_search_service.query_builder \
        .add_track_result_type() \
        .add_track_filter("Track") \
        .generate_search_query()

    with pytest.raises(MusicSearchProviderConnectionError) as e:
        deezer_music_search_service.execute_query(search_query)


@mock.patch('snipssonos.services.deezer.music_search_and_play_service.requests')
def test_music_search_provider_raises_exception_for_wrong_query_to_deezer_api(mock_requests,
                                                                              deezer_music_search_service):
    mock_requests.get.side_effect = requests.exceptions.ConnectionError

    search_query = deezer_music_search_service.query_builder \
        .add_track_result_type() \
        .add_track_filter("Track") \
        .generate_search_query()

    with pytest.raises(MusicSearchProviderConnectionError) as e:
        deezer_music_search_service.execute_query(search_query)


@mock.patch('snipssonos.services.deezer.music_search_and_play_service.requests.Response')
@mock.patch('snipssonos.services.deezer.music_search_and_play_service.requests')
def test_search_album(mock_requests, mock_response, deezer_music_search_service,
                      connected_device):
    # query builder
    # execute query

    result = deezer_music_search_service.search_album("favourite album")

    expected_query = "{}/{}/musicsearch/{}/{}/{}".format(BASE_ENDPOINT, connected_device.name, "deezer",
                                                         "album", "favourite album")
    mock_requests.get.assert_called_with(expected_query)
    assert len(result) == 1
    assert isinstance(result[0], Album)


@mock.patch('snipssonos.services.deezer.music_search_and_play_service.requests.Response')
@mock.patch('snipssonos.services.deezer.music_search_and_play_service.requests')
def test_search_album_for_artist(mock_requests, mock_response, deezer_music_search_service, connected_device):
    result = deezer_music_search_service.search_album_for_artist("favourite album", "favourite artist")

    expected_query = "{}/{}/musicsearch/{}/{}/{}".format(BASE_ENDPOINT, connected_device.name, "deezer",
                                                         "album", 'album:"favourite album":artist:"favourite artist"')

    mock_requests.get.assert_called_with(expected_query)
    assert len(result) == 1
    assert isinstance(result[0], Album)


@mock.patch('snipssonos.services.deezer.music_search_and_play_service.requests.Response')
@mock.patch('snipssonos.services.deezer.music_search_and_play_service.requests')
def test_search_album_in_playlist(mock_requests, mock_response, deezer_music_search_service, connected_device):
    result = deezer_music_search_service.search_album_in_playlist("favourite album", "vibing")
    expected_query = "{}/{}/musicsearch/{}/{}/{}".format(BASE_ENDPOINT, connected_device.name, "deezer",
                                                         "album", "favourite album")

    mock_requests.get.assert_called_with(expected_query)
    assert len(result) == 1
    assert isinstance(result[0], Album)


@mock.patch('snipssonos.services.deezer.music_search_and_play_service.requests.Response')
@mock.patch('snipssonos.services.deezer.music_search_and_play_service.requests')
def test_search_album_for_artist_and_for_playlist(mock_requests, mock_response, deezer_music_search_service,
                                                  connected_device):
    result = deezer_music_search_service.search_album_for_artist_and_for_playlist("favourite album", "favourite artist",
                                                                                  "balling")
    expected_query = "{}/{}/musicsearch/{}/{}/{}".format(BASE_ENDPOINT, connected_device.name, "deezer",
                                                         "album", 'album:"favourite album":artist:"favourite artist"')

    mock_requests.get.assert_called_with(expected_query)
    assert len(result) == 1
    assert isinstance(result[0], Album)


@mock.patch('snipssonos.services.deezer.music_search_and_play_service.requests.Response')
@mock.patch('snipssonos.services.deezer.music_search_and_play_service.requests')
def test_search_track(mock_requests, mock_response, deezer_music_search_service, connected_device):
    result = deezer_music_search_service.search_track("my fav track")

    expected_query = "{}/{}/musicsearch/{}/{}/{}".format(BASE_ENDPOINT, connected_device.name, "deezer",
                                                         "song", "my fav track")
    mock_requests.get.assert_called_with(expected_query)

    assert len(result) == 1
    assert isinstance(result[0], Track)


@mock.patch('snipssonos.services.deezer.music_search_and_play_service.requests.Response')
@mock.patch('snipssonos.services.deezer.music_search_and_play_service.requests')
def test_search_track_for_artist(mock_requests, mock_response, deezer_music_search_service, connected_device):
    result = deezer_music_search_service.search_track_for_artist("my fav track", "my fav artist")

    expected_query = "{}/{}/musicsearch/{}/{}/{}".format(BASE_ENDPOINT, connected_device.name, "deezer",
                                                         "song", 'track:"my fav track":artist:"my fav artist"')
    mock_requests.get.assert_called_with(expected_query)
    assert len(result) == 1
    assert isinstance(result[0], Track)
    assert len(result[0].artists) > 0
    assert isinstance(result[0].artists[0], Artist)


@mock.patch('snipssonos.services.deezer.music_search_and_play_service.requests.Response')
@mock.patch('snipssonos.services.deezer.music_search_and_play_service.requests')
def test_search_track_for_album(mock_requests, mock_response, deezer_music_search_service, connected_device):
    result = deezer_music_search_service.search_track_for_album("my fav track", "a very good album")

    expected_query = "{}/{}/musicsearch/{}/{}/{}".format(BASE_ENDPOINT, connected_device.name, "deezer",
                                                         "song", 'track:"my fav track":album:"a very good album"')
    mock_requests.get.assert_called_with(expected_query)
    assert len(result) == 1
    assert isinstance(result[0], Track)


@mock.patch('snipssonos.services.deezer.music_search_and_play_service.requests.Response')
@mock.patch('snipssonos.services.deezer.music_search_and_play_service.requests')
def test_search_track_for_playlist(mock_requests, mock_response, deezer_music_search_service, connected_device):
    deezer_music_search_service.search_track_for_playlist("my fav track", "a very good playlist")

    expected_query = "{}/{}/musicsearch/{}/{}/{}".format(BASE_ENDPOINT, connected_device.name, "deezer",
                                                         "song", "my fav track")
    mock_requests.get.assert_called_with(expected_query)


@mock.patch('snipssonos.services.deezer.music_search_and_play_service.requests.Response')
@mock.patch('snipssonos.services.deezer.music_search_and_play_service.requests')
def search_track_for_album_and_for_artist(mock_requests, mock_response, deezer_music_search_service, connected_device):
    deezer_music_search_service.search_track_for_album_and_for_artist("my fav track", "a very good album",
                                                                      "my fav artist")

    expected_query = "{}/{}/musicsearch/{}/{}/{}".format(BASE_ENDPOINT, connected_device.name, "deezer",
                                                         "song", "my fav track my fav artist")
    mock_requests.get.assert_called_with(expected_query)


@mock.patch('snipssonos.services.deezer.music_search_and_play_service.requests.Response')
@mock.patch('snipssonos.services.deezer.music_search_and_play_service.requests')
def search_track_for_album_and_for_playlist(mock_requests, mock_response, deezer_music_search_service,
                                            connected_device):
    deezer_music_search_service.search_track_for_album_and_for_playlist("my fav track", "a very good album",
                                                                        "good vibes")

    expected_query = "{}/{}/musicsearch/{}/{}/{}".format(BASE_ENDPOINT, connected_device.name, "deezer",
                                                         "song", "my fav track")
    mock_requests.get.assert_called_with(expected_query)


@mock.patch('snipssonos.services.deezer.music_search_and_play_service.requests.Response')
@mock.patch('snipssonos.services.deezer.music_search_and_play_service.requests')
def search_track_for_album_and_for_playlist(mock_requests, mock_response, deezer_music_search_service,
                                            connected_device):
    deezer_music_search_service.search_track_for_artist_and_for_playlist("my fav track", "a very good artist",
                                                                         "good vibes")

    expected_query = "{}/{}/musicsearch/{}/{}/{}".format(BASE_ENDPOINT, connected_device.name, "deezer",
                                                         "song", "my fav track a very good artist")
    mock_requests.get.assert_called_with(expected_query)


@mock.patch('snipssonos.services.deezer.music_search_and_play_service.requests.Response')
@mock.patch('snipssonos.services.deezer.music_search_and_play_service.requests')
def search_track_for_album_and_for_artist_and_for_playlist(mock_requests, mock_response, deezer_music_search_service,
                                                           connected_device):
    deezer_music_search_service.search_track_for_artist_and_for_playlist("my fav track", "a nice album",
                                                                         "a very good artist", "good vibes")

    expected_query = "{}/{}/musicsearch/{}/{}/{}".format(BASE_ENDPOINT, connected_device.name, "deezer",
                                                         "song", "my fav track a very good artist")
    mock_requests.get.assert_called_with(expected_query)


@mock.patch('snipssonos.services.deezer.music_search_and_play_service.requests.Response')
@mock.patch('snipssonos.services.deezer.music_search_and_play_service.requests')
def test_search_artist_for_playlist(mock_requests, mock_response, deezer_music_search_service, connected_device):
    deezer_music_search_service.search_artist_for_playlist("my fav artist", "a playlist a used to like")

    expected_query = "{}/{}/musicsearch/{}/{}/{}".format(BASE_ENDPOINT, connected_device.name, "deezer",
                                                         "song", "my fav artist")
    mock_requests.get.assert_called_with(expected_query)


@mock.patch('snipssonos.services.deezer.music_search_and_play_service.requests.Response')
@mock.patch('snipssonos.services.deezer.music_search_and_play_service.requests')
def test_search_playlist(mock_requests, mock_response, deezer_music_search_service, connected_device):
    deezer_music_search_service.search_playlist("good vibesssss")

    expected_query = "{}/{}/musicsearch/{}/{}/{}".format(BASE_ENDPOINT, connected_device.name, "deezer",
                                                         "playlist", "good vibesssss")
    mock_requests.get.assert_called_with(expected_query)


@mock.patch('snipssonos.services.deezer.music_search_and_play_service.requests.Response')
@mock.patch('snipssonos.services.deezer.music_search_and_play_service.requests')
def test_error_raised_on_request(mock_requests, mock_response, deezer_music_search_service, connected_device):
    mock_response.ok = False
    mock_requests.get.return_value = mock_response

    with pytest.raises(MusicSearchProviderConnectionError):
        deezer_music_search_service.search_playlist("good vibesssss")


def test_method_dispatch_album_in_playlist_to_album(deezer_music_search_service):
    deezer_music_search_service.search_album = mock.Mock()
    deezer_music_search_service.search_album_in_playlist("album_name", "playlist_name")

    deezer_music_search_service.search_album.assert_called()


def test_method_dispatch_album_for_artist_in_playlist_to_album_for_artist(deezer_music_search_service):
    deezer_music_search_service.search_album_for_artist = mock.Mock()
    deezer_music_search_service.search_album_for_artist_and_for_playlist("album_name", "artist_name", "playlist_name")

    deezer_music_search_service.search_album_for_artist.assert_called()


def test_method_dispatch_track_for_playlist_to_track(deezer_music_search_service):
    deezer_music_search_service.search_track = mock.Mock()
    deezer_music_search_service.search_track_for_playlist("track_name", "playlist_name")

    deezer_music_search_service.search_track.assert_called()


def test_method_dispatch_track_for_album_and_for_artist_to_track_for_artist(deezer_music_search_service):
    deezer_music_search_service.search_track_for_artist = mock.Mock()
    deezer_music_search_service.search_track_for_album_and_for_artist("track_name", "album_name", "artist_name")

    deezer_music_search_service.search_track_for_artist.assert_called()


def test_method_dispatch_track_for_album_and_for_playlist_to_track(deezer_music_search_service):
    deezer_music_search_service.search_track = mock.Mock()
    deezer_music_search_service.search_track_for_album_and_for_playlist("track_name", "album_name", "artist_name")

    deezer_music_search_service.search_track.assert_called()


def test_method_dispatch_search_track_for_artist_and_for_playlist_to_search_track_for_artist(
        deezer_music_search_service):
    deezer_music_search_service.search_track_for_artist = mock.Mock()
    deezer_music_search_service.search_track_for_artist_and_for_playlist("track_name", "artist_name", "playlist_name")

    deezer_music_search_service.search_track_for_artist.assert_called()


def test_method_dispatch_track_for_album_and_for_artist_and_for_playlist_to_track_for_artist(
        deezer_music_search_service):
    deezer_music_search_service.search_track_for_artist = mock.Mock()
    deezer_music_search_service.search_track_for_album_and_for_artist_and_for_playlist("track", "album_name", "artist",
                                                                                       "playlist_name")

    deezer_music_search_service.search_track_for_artist.assert_called()
