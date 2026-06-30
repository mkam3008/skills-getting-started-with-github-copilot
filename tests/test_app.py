def test_root_redirects_to_static_index(client):
    # Arrange + Act
    response = client.get("/", follow_redirects=False)

    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_get_activities_returns_activity_data(client):
    # Arrange + Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_adds_new_participant(client):
    # Arrange
    new_email = "new.student@mergington.edu"

    # Act
    response = client.post(
        "/activities/Chess Club/signup",
        params={"email": new_email},
    )

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {new_email} for Chess Club"}

    activities = client.get("/activities").json()
    assert new_email in activities["Chess Club"]["participants"]


def test_signup_rejects_duplicate_participant(client):
    # Arrange
    existing_email = "michael@mergington.edu"

    # Act
    response = client.post(
        "/activities/Chess Club/signup",
        params={"email": existing_email},
    )

    # Assert
    assert response.status_code == 400
    assert response.json() == {"detail": "Student already signed up for this activity"}


def test_signup_fails_for_missing_activity(client):
    # Arrange + Act
    response = client.post(
        "/activities/Unknown Club/signup",
        params={"email": "student@mergington.edu"},
    )

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_unregister_removes_participant(client):
    # Arrange
    email = "olivia@mergington.edu"

    # Act
    response = client.delete(f"/activities/Gym Class/participants/{email}")

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Unregistered {email} from Gym Class"}

    activities = client.get("/activities").json()
    assert email not in activities["Gym Class"]["participants"]


def test_unregister_fails_when_participant_missing(client):
    # Arrange + Act
    response = client.delete(
        "/activities/Chess Club/participants/not.enrolled@mergington.edu"
    )

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Participant not found in this activity"}


def test_unregister_fails_for_missing_activity(client):
    # Arrange + Act
    response = client.delete("/activities/Unknown Club/participants/student@mergington.edu")

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}
