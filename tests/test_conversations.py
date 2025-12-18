"""
Tests for the DIMO Conversations API.

These tests verify the functionality of the Conversations client including:
- Agent creation and deletion
- Synchronous and streaming message sending
- Conversation history retrieval
- Health checks
- Error handling
"""

import json
from unittest.mock import MagicMock, Mock, patch
import pytest
from dimo.dimo import DIMO
from dimo.errors import HTTPError, DimoTypeError


class TestConversationsHealthCheck:
    """Test the health_check endpoint."""

    def test_health_check_success(self, monkeypatch):
        """Test successful health check returns service status."""
        client = DIMO(env="Dev")
        
        # Mock the request method to return health data
        fake_request = MagicMock(return_value={
            "status": "healthy",
            "version": "1.0.0",
            "proxy": "active",
            "default_model": "gpt-4"
        })
        monkeypatch.setattr(client, "request", fake_request)
        
        result = client.conversations.health_check()
        
        # Verify the request was called correctly
        fake_request.assert_called_once_with("GET", "Conversations", "/")
        
        # Verify the response
        assert result["status"] == "healthy"
        assert result["version"] == "1.0.0"
        assert "default_model" in result


class TestConversationsCreateAgent:
    """Test the create_agent endpoint."""

    def test_create_agent_minimal(self, monkeypatch):
        """Test creating an agent with minimal required parameters (no vehicle_ids)."""
        client = DIMO(env="Dev")
        
        # Mock the request method
        fake_request = MagicMock(return_value={
            "agentId": "agent-abc123",
            "type": "driver_agent_v1",
            "personality": "uncle_mechanic",
            "createdAt": "2024-01-01T00:00:00Z"
        })
        monkeypatch.setattr(client, "request", fake_request)
        
        dev_jwt = "test_developer_jwt"
        api_key = "0x1234567890abcdef"
        user_wallet = "0x86b04f6d1D9E79aD7eB31cDEAF37442B00d64605"
        
        result = client.conversations.create_agent(
            developer_jwt=dev_jwt,
            api_key=api_key,
            user_wallet=user_wallet,
            agent_type="driver_agent_v1"
        )
        
        # Verify the request was called correctly
        fake_request.assert_called_once()
        args, kwargs = fake_request.call_args
        
        assert args[0] == "POST"
        assert args[1] == "Conversations"
        assert args[2] == "/agents"
        assert kwargs["data"]["type"] == "driver_agent_v1"
        assert kwargs["data"]["personality"] == "uncle_mechanic"
        assert kwargs["data"]["secrets"]["DIMO_API_KEY"] == api_key
        assert kwargs["data"]["variables"]["USER_WALLET"] == user_wallet
        assert "VEHICLE_IDS" not in kwargs["data"]["variables"]
        
        # Verify the response
        assert result["agentId"] == "agent-abc123"
        assert result["type"] == "driver_agent_v1"

    def test_create_agent_with_vehicle_ids(self, monkeypatch):
        """Test creating an agent with specific vehicle IDs."""
        client = DIMO(env="Dev")
        
        fake_request = MagicMock(return_value={
            "agentId": "agent-def456",
            "type": "driver_agent_v1",
            "createdAt": "2024-01-01T00:00:00Z"
        })
        monkeypatch.setattr(client, "request", fake_request)
        
        dev_jwt = "test_developer_jwt"
        api_key = "0xabcdef123456"
        user_wallet = "0x86b04f6d1D9E79aD7eB31cDEAF37442B00d64605"
        vehicle_ids = "[872, 1234]"
        
        result = client.conversations.create_agent(
            developer_jwt=dev_jwt,
            api_key=api_key,
            user_wallet=user_wallet,
            agent_type="driver_agent_v1",
            vehicle_ids=vehicle_ids
        )
        
        # Verify the request
        args, kwargs = fake_request.call_args
        assert kwargs["data"]["secrets"]["DIMO_API_KEY"] == api_key
        assert kwargs["data"]["variables"]["USER_WALLET"] == user_wallet
        assert kwargs["data"]["variables"]["VEHICLE_IDS"] == vehicle_ids
        
        # Verify the response
        assert result["agentId"] == "agent-def456"

    def test_create_agent_with_custom_personality(self, monkeypatch):
        """Test creating an agent with custom personality preset."""
        client = DIMO(env="Dev")
        
        fake_request = MagicMock(return_value={
            "agentId": "agent-ghi789",
            "type": "driver_agent_v1",
            "personality": "helpful_assistant",
            "createdAt": "2024-01-01T00:00:00Z"
        })
        monkeypatch.setattr(client, "request", fake_request)
        
        result = client.conversations.create_agent(
            developer_jwt="test_jwt",
            api_key="0xapikey",
            user_wallet="0xwallet",
            agent_type="driver_agent_v1",
            personality="helpful_assistant"
        )
        
        # Verify the request
        args, kwargs = fake_request.call_args
        assert kwargs["data"]["personality"] == "helpful_assistant"
        
        # Verify the response
        assert result["personality"] == "helpful_assistant"

    def test_create_agent_full_config(self, monkeypatch):
        """Test creating an agent with all configuration options."""
        client = DIMO(env="Dev")
        
        fake_request = MagicMock(return_value={
            "agentId": "agent-full123",
            "type": "driver_agent_v1",
            "personality": "uncle_mechanic",
            "createdAt": "2024-01-01T00:00:00Z"
        })
        monkeypatch.setattr(client, "request", fake_request)
        
        result = client.conversations.create_agent(
            developer_jwt="test_jwt",
            api_key="0x1234567890abcdef",
            user_wallet="0x86b04f6d1D9E79aD7eB31cDEAF37442B00d64605",
            vehicle_ids="[1, 2, 3]",
            agent_type="driver_agent_v1",
            personality="uncle_mechanic"
        )
        
        # Verify all fields are in request
        args, kwargs = fake_request.call_args
        assert kwargs["data"]["type"] == "driver_agent_v1"
        assert kwargs["data"]["personality"] == "uncle_mechanic"
        assert kwargs["data"]["secrets"]["DIMO_API_KEY"] == "0x1234567890abcdef"
        assert kwargs["data"]["variables"]["USER_WALLET"] == "0x86b04f6d1D9E79aD7eB31cDEAF37442B00d64605"
        assert kwargs["data"]["variables"]["VEHICLE_IDS"] == "[1, 2, 3]"

    def test_create_agent_invalid_types(self):
        """Test that type checking is enforced for parameters."""
        client = DIMO(env="Dev")
        
        # Test invalid developer_jwt type
        with pytest.raises(DimoTypeError):
            client.conversations.create_agent(
                developer_jwt=123,  # Should be string
                api_key="0xapikey",
                user_wallet="0xwallet",
                agent_type="driver_agent_v1"
            )
        
        # Test invalid api_key type
        with pytest.raises(DimoTypeError):
            client.conversations.create_agent(
                developer_jwt="test_jwt",
                api_key=123,  # Should be string
                user_wallet="0xwallet",
                agent_type="driver_agent_v1"
            )
        
        # Test invalid user_wallet type
        with pytest.raises(DimoTypeError):
            client.conversations.create_agent(
                developer_jwt="test_jwt",
                api_key="0xapikey",
                user_wallet=123,  # Should be string
                agent_type="driver_agent_v1"
            )
        
        # Test invalid agent_type type
        with pytest.raises(DimoTypeError):
            client.conversations.create_agent(
                developer_jwt="test_jwt",
                api_key="0xapikey",
                user_wallet="0xwallet",
                agent_type=123  # Should be string
            )
        
        # Test invalid vehicle_ids type
        with pytest.raises(DimoTypeError):
            client.conversations.create_agent(
                developer_jwt="test_jwt",
                api_key="0xapikey",
                user_wallet="0xwallet",
                agent_type="driver_agent_v1",
                vehicle_ids=123  # Should be string or None
            )
        
        # Test invalid personality type
        with pytest.raises(DimoTypeError):
            client.conversations.create_agent(
                developer_jwt="test_jwt",
                api_key="0xapikey",
                user_wallet="0xwallet",
                agent_type="driver_agent_v1",
                personality=123  # Should be string
            )


class TestConversationsDeleteAgent:
    """Test the delete_agent endpoint."""

    def test_delete_agent_success(self, monkeypatch):
        """Test successful agent deletion."""
        client = DIMO(env="Dev")
        
        fake_request = MagicMock(return_value={
            "message": "Agent deleted successfully",
            "agentId": "agent-abc123"
        })
        monkeypatch.setattr(client, "request", fake_request)
        
        dev_jwt = "test_developer_jwt"
        agent_id = "agent-abc123"
        
        result = client.conversations.delete_agent(
            developer_jwt=dev_jwt,
            agent_id=agent_id
        )
        
        # Verify the request
        fake_request.assert_called_once()
        args, kwargs = fake_request.call_args
        
        assert args[0] == "DELETE"
        assert args[1] == "Conversations"
        assert args[2] == "/agents/agent-abc123"
        
        # Verify the response
        assert result["message"] == "Agent deleted successfully"
        assert result["agentId"] == agent_id

    def test_delete_agent_invalid_types(self):
        """Test that type checking is enforced."""
        client = DIMO(env="Dev")
        
        with pytest.raises(DimoTypeError):
            client.conversations.delete_agent(
                developer_jwt=123,  # Should be string
                agent_id="agent-abc123"
            )
        
        with pytest.raises(DimoTypeError):
            client.conversations.delete_agent(
                developer_jwt="test_jwt",
                agent_id=123  # Should be string
            )


class TestConversationsSendMessage:
    """Test the send_message endpoint (synchronous)."""

    def test_send_message_basic(self, monkeypatch):
        """Test sending a basic message and receiving a response."""
        client = DIMO(env="Dev")
        
        fake_request = MagicMock(return_value={
            "agentId": "agent-abc123",
            "message": "What's my car's make and model?",
            "response": "Your vehicle is a 2020 Tesla Model 3.",
            "vehiclesQueried": [872],
            "timestamp": "2024-01-01T00:00:00Z"
        })
        monkeypatch.setattr(client, "request", fake_request)
        
        dev_jwt = "test_developer_jwt"
        agent_id = "agent-abc123"
        message = "What's my car's make and model?"
        
        result = client.conversations.send_message(
            developer_jwt=dev_jwt,
            agent_id=agent_id,
            message=message
        )
        
        # Verify the request
        args, kwargs = fake_request.call_args
        
        assert args[0] == "POST"
        assert args[1] == "Conversations"
        assert args[2] == "/agents/agent-abc123/message"
        assert kwargs["data"]["message"] == message
        
        # Verify the response
        assert result["agentId"] == agent_id
        assert result["response"] == "Your vehicle is a 2020 Tesla Model 3."
        assert result["vehiclesQueried"] == [872]

    def test_send_message_with_vehicle_ids_override(self, monkeypatch):
        """Test sending a message with vehicle IDs override."""
        client = DIMO(env="Dev")
        
        fake_request = MagicMock(return_value={
            "agentId": "agent-abc123",
            "message": "What's the speed?",
            "response": "Current speed is 65 mph.",
            "vehiclesQueried": [1234],
            "timestamp": "2024-01-01T00:00:00Z"
        })
        monkeypatch.setattr(client, "request", fake_request)
        
        result = client.conversations.send_message(
            developer_jwt="test_jwt",
            agent_id="agent-abc123",
            message="What's the speed?",
            vehicle_ids=[1234]
        )
        
        # Verify vehicle_ids was included in request body
        args, kwargs = fake_request.call_args
        assert kwargs["data"]["vehicleIds"] == [1234]
        assert result["vehiclesQueried"] == [1234]

    def test_send_message_with_user_override(self, monkeypatch):
        """Test sending a message with user override."""
        client = DIMO(env="Dev")
        
        fake_request = MagicMock(return_value={
            "agentId": "agent-abc123",
            "message": "Hello",
            "response": "Hi there!",
            "vehiclesQueried": [],
            "timestamp": "2024-01-01T00:00:00Z"
        })
        monkeypatch.setattr(client, "request", fake_request)
        
        result = client.conversations.send_message(
            developer_jwt="test_jwt",
            agent_id="agent-abc123",
            message="Hello",
            user="0xnewuser"
        )
        
        # Verify user was included in request body
        args, kwargs = fake_request.call_args
        assert kwargs["data"]["user"] == "0xnewuser"

    def test_send_message_invalid_types(self):
        """Test that type checking is enforced."""
        client = DIMO(env="Dev")
        
        with pytest.raises(DimoTypeError):
            client.conversations.send_message(
                developer_jwt=123,  # Should be string
                agent_id="agent-abc123",
                message="Hello"
            )
        
        with pytest.raises(DimoTypeError):
            client.conversations.send_message(
                developer_jwt="test_jwt",
                agent_id="agent-abc123",
                message=123  # Should be string
            )


class TestConversationsStreamMessage:
    """Test the stream_message endpoint (SSE streaming)."""

    def test_stream_message_success(self, monkeypatch):
        """Test streaming a message and receiving token-by-token response."""
        client = DIMO(env="Dev")
        
        # Mock SSE response data
        sse_lines = [
            b"data: {\"content\": \"Your\"}",
            b"data: {\"content\": \" vehicle\"}",
            b"data: {\"content\": \" is\"}",
            b"data: {\"content\": \" a\"}",
            b"data: {\"content\": \" Tesla.\"}",
            b"data: {\"done\": true, \"agentId\": \"agent-abc123\", \"vehiclesQueried\": [872]}"
        ]
        
        # Mock response object
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.iter_lines = Mock(return_value=sse_lines)
        mock_response.raise_for_status = Mock()
        
        # Mock session.request
        mock_session = Mock()
        mock_session.request = Mock(return_value=mock_response)
        monkeypatch.setattr(client.conversations, "_session", mock_session)
        
        dev_jwt = "test_developer_jwt"
        agent_id = "agent-abc123"
        message = "What's my car?"
        
        # Collect streamed chunks
        chunks = list(client.conversations.stream_message(
            developer_jwt=dev_jwt,
            agent_id=agent_id,
            message=message
        ))
        
        # Verify we got all chunks
        assert len(chunks) == 6
        assert chunks[0] == {"content": "Your"}
        assert chunks[1] == {"content": " vehicle"}
        assert chunks[-1]["done"] is True
        assert chunks[-1]["agentId"] == "agent-abc123"
        assert chunks[-1]["vehiclesQueried"] == [872]
        
        # Verify the request was made correctly
        mock_session.request.assert_called_once()
        call_args = mock_session.request.call_args
        assert call_args[1]["method"] == "POST"
        assert "/agents/agent-abc123/stream" in call_args[1]["url"]
        assert call_args[1]["stream"] is True
        assert call_args[1]["headers"]["Accept"] == "text/event-stream"

    def test_stream_message_with_overrides(self, monkeypatch):
        """Test streaming with vehicle_ids and user overrides."""
        client = DIMO(env="Dev")
        
        # Mock minimal SSE response
        sse_lines = [
            b"data: {\"content\": \"Hello\"}",
            b"data: {\"done\": true, \"agentId\": \"agent-abc123\", \"vehiclesQueried\": [1234]}"
        ]
        
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.iter_lines = Mock(return_value=sse_lines)
        mock_response.raise_for_status = Mock()
        
        mock_session = Mock()
        mock_session.request = Mock(return_value=mock_response)
        monkeypatch.setattr(client.conversations, "_session", mock_session)
        
        # Call with overrides
        chunks = list(client.conversations.stream_message(
            developer_jwt="test_jwt",
            agent_id="agent-abc123",
            message="Hello",
            vehicle_ids=[1234],
            user="0xnewuser"
        ))
        
        # Verify the request included overrides in body
        call_args = mock_session.request.call_args
        body = json.loads(call_args[1]["data"])
        assert body["message"] == "Hello"
        assert body["vehicleIds"] == [1234]
        assert body["user"] == "0xnewuser"

    def test_stream_message_handles_malformed_json(self, monkeypatch):
        """Test that malformed JSON is skipped gracefully."""
        client = DIMO(env="Dev")
        
        # Mock SSE with malformed data
        sse_lines = [
            b"data: {\"content\": \"Good\"}",
            b"data: {malformed json here",  # This should be skipped
            b"data: {\"content\": \"data\"}",
            b"data: {\"done\": true, \"agentId\": \"agent-abc123\", \"vehiclesQueried\": []}"
        ]
        
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.iter_lines = Mock(return_value=sse_lines)
        mock_response.raise_for_status = Mock()
        
        mock_session = Mock()
        mock_session.request = Mock(return_value=mock_response)
        monkeypatch.setattr(client.conversations, "_session", mock_session)
        
        # Collect chunks - malformed one should be skipped
        chunks = list(client.conversations.stream_message(
            developer_jwt="test_jwt",
            agent_id="agent-abc123",
            message="Test"
        ))
        
        # Should have 3 valid chunks (malformed one skipped)
        assert len(chunks) == 3
        assert chunks[0] == {"content": "Good"}
        assert chunks[1] == {"content": "data"}
        assert chunks[2]["done"] is True

    def test_stream_message_http_error(self, monkeypatch):
        """Test that HTTP errors are properly raised."""
        from requests import RequestException
        
        client = DIMO(env="Dev")
        
        # Mock a failed request
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json = Mock(return_value={"error": "Agent not found"})
        
        mock_exception = RequestException("Not found")
        mock_exception.response = mock_response
        
        mock_session = Mock()
        mock_session.request = Mock(side_effect=mock_exception)
        monkeypatch.setattr(client.conversations, "_session", mock_session)
        
        # Verify HTTPError is raised
        with pytest.raises(HTTPError) as exc_info:
            list(client.conversations.stream_message(
                developer_jwt="test_jwt",
                agent_id="bad-agent-id",
                message="Test"
            ))
        
        assert exc_info.value.status == 404


class TestConversationsGetHistory:
    """Test the get_history endpoint."""

    def test_get_history_default_limit(self, monkeypatch):
        """Test retrieving conversation history with default limit."""
        client = DIMO(env="Dev")
        
        fake_request = MagicMock(return_value={
            "agentId": "agent-abc123",
            "messages": [
                {"role": "user", "content": "Hello", "timestamp": "2024-01-01T00:00:00Z"},
                {"role": "agent", "content": "Hi there!", "timestamp": "2024-01-01T00:00:01Z"}
            ],
            "total": 2
        })
        monkeypatch.setattr(client, "request", fake_request)
        
        dev_jwt = "test_developer_jwt"
        agent_id = "agent-abc123"
        
        result = client.conversations.get_history(
            developer_jwt=dev_jwt,
            agent_id=agent_id
        )
        
        # Verify the request
        args, kwargs = fake_request.call_args
        
        assert args[0] == "GET"
        assert args[1] == "Conversations"
        assert args[2] == "/agents/agent-abc123/history"
        assert kwargs["params"]["limit"] == 100  # Default limit
        
        # Verify the response
        assert result["agentId"] == agent_id
        assert len(result["messages"]) == 2
        assert result["total"] == 2

    def test_get_history_custom_limit(self, monkeypatch):
        """Test retrieving conversation history with custom limit."""
        client = DIMO(env="Dev")
        
        fake_request = MagicMock(return_value={
            "agentId": "agent-abc123",
            "messages": [
                {"role": "user", "content": "Test", "timestamp": "2024-01-01T00:00:00Z"}
            ],
            "total": 1
        })
        monkeypatch.setattr(client, "request", fake_request)
        
        result = client.conversations.get_history(
            developer_jwt="test_jwt",
            agent_id="agent-abc123",
            limit=50
        )
        
        # Verify custom limit was used
        args, kwargs = fake_request.call_args
        assert kwargs["params"]["limit"] == 50

    def test_get_history_invalid_types(self):
        """Test that type checking is enforced."""
        client = DIMO(env="Dev")
        
        with pytest.raises(DimoTypeError):
            client.conversations.get_history(
                developer_jwt=123,  # Should be string
                agent_id="agent-abc123"
            )
        
        with pytest.raises(DimoTypeError):
            client.conversations.get_history(
                developer_jwt="test_jwt",
                agent_id=123  # Should be string
            )
        
        with pytest.raises(DimoTypeError):
            client.conversations.get_history(
                developer_jwt="test_jwt",
                agent_id="agent-abc123",
                limit="not_an_int"  # Should be int
            )


class TestConversationsIntegration:
    """Integration tests demonstrating complete workflows."""

    def test_full_agent_lifecycle(self, monkeypatch):
        """Test creating an agent, sending messages, and deleting it."""
        client = DIMO(env="Dev")
        
        # Track which endpoints are called
        calls_made = []
        
        def fake_request(*args, **kwargs):
            calls_made.append((args[0], args[2]))
            if args[0] == "POST" and args[2] == "/agents":
                return {
                    "agentId": "agent-test123",
                    "type": "driver_agent_v1",
                    "personality": "uncle_mechanic",
                    "createdAt": "2024-01-01T00:00:00Z"
                }
            elif args[0] == "POST" and "/message" in args[2]:
                return {
                    "agentId": "agent-test123",
                    "response": "Your vehicle is a Tesla.",
                    "vehiclesQueried": [872]
                }
            elif args[0] == "DELETE":
                return {"message": "Agent deleted successfully"}
            return {}
        
        monkeypatch.setattr(client, "request", fake_request)
        
        # 1. Create agent
        agent = client.conversations.create_agent(
            developer_jwt="test_jwt",
            api_key="0x1234567890abcdef",
            user_wallet="0x86b04f6d1D9E79aD7eB31cDEAF37442B00d64605",
            agent_type="driver_agent_v1",
            vehicle_ids="[872]"
        )
        assert agent["agentId"] == "agent-test123"
        assert ("POST", "/agents") in calls_made
        
        # 2. Send message
        response = client.conversations.send_message(
            developer_jwt="test_jwt",
            agent_id=agent["agentId"],
            message="What's my vehicle?"
        )
        assert response["agentId"] == "agent-test123"
        assert "Tesla" in response["response"]
        
        # 3. Delete agent
        delete_result = client.conversations.delete_agent(
            developer_jwt="test_jwt",
            agent_id=agent["agentId"]
        )
        assert "deleted" in delete_result["message"].lower()
        assert len(calls_made) == 3  # Verify all 3 operations were called

