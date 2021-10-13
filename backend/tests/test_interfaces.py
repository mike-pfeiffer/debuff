import pytest
from debuff import __version__
from debuff.services.interfaces import show_all_interface_names


def test_version():
    assert __version__ == "0.1.0"


@pytest.mark.parametrize(
    "interface, status_code", [("test", 422), (show_all_interface_names()[0], 200)]
)
def test_get_interface_details(test_app, interface, status_code):
    response = test_app.get(f"/api/interfaces/details?interface={interface}")
    assert response.status_code == status_code


@pytest.mark.parametrize(
    "interface, status_code", [("test", 422), (show_all_interface_names()[0], 200)]
)
def test_get_interface_buffers(test_app, interface, status_code):
    response = test_app.get(f"/api/interfaces/details?interface={interface}")
    assert response.status_code == status_code


def test_get_interface_names(test_app):
    response = test_app.get("/api/interfaces/names")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.parametrize("interface, state, status_code", [("test", "up", 422)])
def test_post_interface_state(test_app, interface, state, status_code):
    response = test_app.post(
        f"/api/interfaces/state?interface={interface}&state={state}"
    )
    assert response.status_code == status_code


@pytest.mark.parametrize(
    "interface, rx_ring, tx_ring, status_code", [("test", "10", "10", 422)]
)
def test_post_interface_buffers(test_app, interface, rx_ring, tx_ring, status_code):
    response = test_app.post(
        f"/api/interfaces/buffers?interface={interface}&rx_ring={rx_ring}&tx_ring={tx_ring}"
    )
    assert response.status_code == status_code
