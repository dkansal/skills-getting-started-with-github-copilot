from fastapi.testclient import TestClient


def test_root_redirects_to_static_index(client: TestClient):
    # Arrange
    expected_location = "/static/index.html"

    # Act
    response = client.get("/", follow_redirects=False)

    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == expected_location


def test_get_activities_returns_dictionary(client: TestClient):
    # Arrange

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "participants" in data["Chess Club"]


def test_signup_for_activity_adds_participant(client: TestClient):
    # Arrange
    activity = "Chess Club"
    email = "newstudent@mergington.edu"
    params = {"email": email}

    # Act
    response = client.post(f"/activities/{activity}/signup", params=params)

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for {activity}"}


def test_signup_for_same_student_returns_400(client: TestClient):
    # Arrange
    activity = "Chess Club"
    email = "duplicate@mergington.edu"
    params = {"email": email}

    # Act
    first_response = client.post(f"/activities/{activity}/signup", params=params)
    second_response = client.post(f"/activities/{activity}/signup", params=params)

    # Assert
    assert first_response.status_code == 200
    assert second_response.status_code == 400
    assert second_response.json()["detail"] == "Student already signed up"


def test_signup_for_missing_activity_returns_404(client: TestClient):
    # Arrange
    activity = "Nonexistent Activity"
    params = {"email": "student@mergington.edu"}

    # Act
    response = client.post(f"/activities/{activity}/signup", params=params)

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
