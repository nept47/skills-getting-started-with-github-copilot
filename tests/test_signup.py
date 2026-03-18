"""Tests for signup endpoints."""


def test_signup_success(client):
    """Test successful signup for an activity."""
    # Arrange
    activity_name = "Chess Club"
    email = "student@example.com"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert email in data["message"]

    # Verify participant was added
    activities_response = client.get("/activities")
    activities = activities_response.json()
    assert email in activities[activity_name]["participants"]


def test_signup_duplicate(client):
    """Test duplicate signup returns 400."""
    # Arrange
    activity_name = "Chess Club"
    email = "duplicate@example.com"

    # First signup
    client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Act - second signup
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data


def test_signup_nonexistent_activity(client):
    """Test signup for non-existent activity returns 404."""
    # Arrange
    activity_name = "NonExistent Activity"
    email = "student@example.com"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data


def test_unsignup_success(client):
    """Test successful unregistration from an activity."""
    # Arrange
    activity_name = "Programming Class"
    email = "student@example.com"

    # First signup
    client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Act
    response = client.delete(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "message" in data

    # Verify participant was removed
    activities_response = client.get("/activities")
    activities = activities_response.json()
    assert email not in activities[activity_name]["participants"]


def test_unsignup_nonexistent_student(client):
    """Test unregistration of non-existent student returns 400."""
    # Arrange
    activity_name = "Programming Class"
    email = "nonexistent@example.com"

    # Act
    response = client.delete(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data


def test_unsignup_nonexistent_activity(client):
    """Test unregistration from non-existent activity returns 404."""
    # Arrange
    activity_name = "NonExistent Activity"
    email = "student@example.com"

    # Act
    response = client.delete(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data