import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool
from app.api import app, get_session


@pytest.fixture(name="session")
def session_fixture():
    # in-memory database for testing
    engine = create_engine(
        "sqlite:///testdb.db",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


def test_create_block(client: TestClient):
    response = client.post(
        "/blocks/", json={"name": "test block", "block_type": "test type"}
    )
    data = response.json()

    assert response.status_code == 200
    assert data["name"] == "test block"
    assert data["block_type"] == "test type"
    assert data["id"] is not None


def test_read_blocks(client: TestClient):
    response = client.get("/blocks/")
    assert response.status_code == 200


def test_read_block(client: TestClient):
    response = client.get("/blocks/1")
    assert response.status_code == 200


def test_update_block(client: TestClient):
    response = client.patch(
        "/blocks/1", json={"name": "updated block", "block_type": "updated type"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "updated block"
    assert data["block_type"] == "updated type"


def test_delete_block(client: TestClient):
    response = client.delete("/blocks/1")
    assert response.status_code == 200


def test_create_tunnel(client: TestClient):
    response = client.post("/tunnels/", json={"name": "test tunnel"})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "test tunnel"
    assert "id" in data


def test_read_tunnel(client: TestClient):
    response = client.get("/tunnels/1")
    assert response.status_code == 200


def test_update_tunnel(client: TestClient):
    response = client.patch("/tunnels/1", json={"name": "updated tunnel"})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "updated tunnel"


def test_delete_tunnel(client: TestClient):
    response = client.delete("/tunnels/1")
    assert response.status_code == 200
