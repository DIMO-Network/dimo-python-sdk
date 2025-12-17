from dimo.errors import check_type, check_optional_type, HTTPError
from typing import Dict, List, Optional, Any, Generator
from requests import Session, RequestException
import json


class Conversations:
    """
    Client for the DIMO Conversations API.

    This API enables developers to create conversational AI agents that can query
    vehicle data, telemetry data, and perform web searches on behalf of users.

    Key Features:
    - Create AI agents with access to specific vehicles
    - Query vehicle identity (make, model, owner) via GraphQL
    - Query real-time telemetry (speed, fuel, location) via GraphQL
    - Perform location-based web searches
    - Stream responses in real-time using Server-Sent Events (SSE)
    - Multi-agent delegation architecture with specialized subagents
    """

    def __init__(self, request_method, get_auth_headers, get_full_path, session: Session):
        self._request = request_method
        self._get_auth_headers = get_auth_headers
        self._get_full_path = get_full_path
        self._session = session

    def health_check(self) -> Dict:
        """
        Check the service status and configuration.

        Returns:
            dict: Service health information including status, version, proxy, and default_model

        Example:
            >>> dimo = DIMO("Production")
            >>> health = dimo.conversations.health_check()
            >>> print(health['status'])
        """
        response = self._request("GET", "Conversations", "/")
        return response

    def create_agent(
        self,
        developer_jwt: str,
        api_key: str,
        user_wallet: str,
        agent_type: str,
        vehicle_ids: Optional[str] = None,
        personality: str = "uncle_mechanic",
    ) -> Dict:
        """
        Create a new conversational agent with the specified configuration.

        Args:
            developer_jwt (str): Developer JWT token for authentication
            api_key (str): DIMO API key for the agent to access vehicle data
            user_wallet (str): User's wallet address (e.g., "0x2345...")
            agent_type (str): The type of agent to create (e.g., "driver_agent_v1")
            vehicle_ids (str, optional): JSON array string of vehicle token IDs (e.g., "[1, 2, 3]").
                If not provided, agent will have access to all vehicles owned by the user.
            personality (str, optional): Personality preset for the agent. Defaults to "uncle_mechanic"

        Returns:
            dict: Agent information including agentId and configuration details

        Behavior:
            - Creates a new agent with the specified type and configuration
            - Validates configuration and mode detection
            - Creates/reuses shared identity subagent
            - Creates per-vehicle telemetry subagents with token exchange
            - Creates shared websearch subagent if enabled

        Example:
            >>> dimo = DIMO("Production")
            >>> dev_jwt = "your_developer_jwt"
            >>> agent = dimo.conversations.create_agent(
            ...     developer_jwt=dev_jwt,
            ...     api_key="0x1234567890abcdef...",
            ...     user_wallet="0x86b04f6d1D9E79aD7eB31cDEAF37442B00d64605",
            ...     agent_type="driver_agent_v1",
            ...     vehicle_ids="[1, 2, 3]",
            ... )
            >>> print(agent['agentId'])
        """
        check_type("developer_jwt", developer_jwt, str)
        check_type("api_key", api_key, str)
        check_type("user_wallet", user_wallet, str)
        check_optional_type("vehicle_ids", vehicle_ids, str)
        check_type("agent_type", agent_type, str)
        check_type("personality", personality, str)

        # Build variables dict
        variables = {"USER_WALLET": user_wallet}
        if vehicle_ids is not None:
            variables["VEHICLE_IDS"] = vehicle_ids

        # Build request body
        body = {
            "personality": personality,
            "secrets": {"DIMO_API_KEY": api_key},
            "type": agent_type,
            "variables": variables,
        }

        response = self._request(
            "POST",
            "Conversations",
            "/agents",
            headers=self._get_auth_headers(developer_jwt),
            data=body,
        )
        return response

    def delete_agent(self, developer_jwt: str, agent_id: str) -> Dict:
        """
        Delete an agent and all associated resources.

        Args:
            developer_jwt (str): Developer JWT token for authentication
            agent_id (str): The agent ID to delete

        Returns:
            dict: Confirmation message

        Behavior:
            - Deletes Letta agent from server
            - Removes metadata from AgentManager
            - Cleanup errors are logged but don't fail the request

        Example:
            >>> dimo = DIMO("Production")
            >>> dev_jwt = "your_developer_jwt"
            >>> result = dimo.conversations.delete_agent(
            ...     developer_jwt=dev_jwt,
            ...     agent_id="agent-abc123"
            ... )
            >>> print(result['message'])
        """
        check_type("developer_jwt", developer_jwt, str)
        check_type("agent_id", agent_id, str)

        response = self._request(
            "DELETE",
            "Conversations",
            f"/agents/{agent_id}",
            headers=self._get_auth_headers(developer_jwt),
        )
        return response

    def send_message(
        self,
        developer_jwt: str,
        agent_id: str,
        message: str,
        vehicle_ids: Optional[List[int]] = None,
        user: Optional[str] = None,
    ) -> Dict:
        """
        Send a message to an agent and receive the complete response (synchronous).

        Args:
            developer_jwt (str): Developer JWT token for authentication
            agent_id (str): The agent ID to send the message to
            message (str): The message to send to the agent
            vehicle_ids (list[int], optional): Optional vehicle IDs override
            user (str, optional): Optional user override

        Returns:
            dict: Response including agentId, message, response, vehiclesQueried, and timestamp

        Behavior:
            - Synchronous request/response
            - Agent delegates to subagents as needed
            - Returns full response after agent completes reasoning
            - Timeout: 120 seconds for complex queries

        Example:
            >>> dimo = DIMO("Production")
            >>> dev_jwt = "your_developer_jwt"
            >>> response = dimo.conversations.send_message(
            ...     developer_jwt=dev_jwt,
            ...     agent_id="agent-abc123",
            ...     message="What's the make and model of my vehicle?"
            ... )
            >>> print(response['response'])
        """
        check_type("developer_jwt", developer_jwt, str)
        check_type("agent_id", agent_id, str)
        check_type("message", message, str)
        check_optional_type("vehicle_ids", vehicle_ids, list)
        check_optional_type("user", user, str)

        body = {"message": message}
        if vehicle_ids is not None:
            body["vehicleIds"] = vehicle_ids
        if user is not None:
            body["user"] = user

        response = self._request(
            "POST",
            "Conversations",
            f"/agents/{agent_id}/message",
            headers=self._get_auth_headers(developer_jwt),
            data=body,
        )
        return response

    def stream_message(
        self,
        developer_jwt: str,
        agent_id: str,
        message: str,
        vehicle_ids: Optional[List[int]] = None,
        user: Optional[str] = None,
    ) -> Generator[Dict[str, Any], None, None]:
        """
        Send a message and receive real-time token-by-token streaming response via SSE.

        Args:
            developer_jwt (str): Developer JWT token for authentication
            agent_id (str): The agent ID to send the message to
            message (str): The message to send to the agent
            vehicle_ids (list[int], optional): Optional vehicle IDs override
            user (str, optional): Optional user override

        Yields:
            dict: SSE events with either {"content": "token"} or {"done": true, ...metadata}

        Behavior:
            - Real-time streaming for better UX
            - Token-by-token generation from LLM
            - Final message includes metadata (agentId, vehiclesQueried)

        Example:
            >>> dimo = DIMO("Production")
            >>> dev_jwt = "your_developer_jwt"
            >>> for chunk in dimo.conversations.stream_message(
            ...     developer_jwt=dev_jwt,
            ...     agent_id="agent-abc123",
            ...     message="What's my current speed?"
            ... ):
            ...     if "content" in chunk:
            ...         print(chunk["content"], end="", flush=True)
            ...     elif "done" in chunk:
            ...         print(f"\\nVehicles queried: {chunk['vehiclesQueried']}")
        """
        check_type("developer_jwt", developer_jwt, str)
        check_type("agent_id", agent_id, str)
        check_type("message", message, str)
        check_optional_type("vehicle_ids", vehicle_ids, list)
        check_optional_type("user", user, str)

        body = {"message": message}
        if vehicle_ids is not None:
            body["vehicleIds"] = vehicle_ids
        if user is not None:
            body["user"] = user

        headers = self._get_auth_headers(developer_jwt)
        headers["Accept"] = "text/event-stream"
        headers["Content-Type"] = "application/json"

        # Build full URL
        url = self._get_full_path("Conversations", f"/agents/{agent_id}/stream")

        # Make streaming request directly with session
        try:
            response = self._session.request(
                method="POST",
                url=url,
                headers=headers,
                data=json.dumps(body),
                stream=True,
            )
            response.raise_for_status()
        except RequestException as exc:
            status = getattr(exc.response, "status_code", None)
            body_error = None
            try:
                body_error = exc.response.json()
            except Exception:
                body_error = exc.response.text if exc.response else None
            raise HTTPError(status=status or -1, message=str(exc), body=body_error)

        # Parse SSE stream
        for line in response.iter_lines():
            if line:
                line = line.decode("utf-8")
                if line.startswith("data: "):
                    data = line[6:]  # Remove "data: " prefix
                    try:
                        yield json.loads(data)
                    except json.JSONDecodeError:
                        # Skip malformed JSON
                        continue

    def get_history(
        self,
        developer_jwt: str,
        agent_id: str,
        limit: int = 100,
    ) -> Dict:
        """
        Retrieve all messages in a conversation.

        Args:
            developer_jwt (str): Developer JWT token for authentication
            agent_id (str): The agent ID to get history for
            limit (int): Maximum number of messages to return (default: 100)

        Returns:
            dict: Conversation history including agentId, messages array, and total count

        Behavior:
            - Retrieves from Letta server
            - Includes all message roles (user, agent, system)
            - Reverse chronological order (newest first)

        Example:
            >>> dimo = DIMO("Production")
            >>> dev_jwt = "your_developer_jwt"
            >>> history = dimo.conversations.get_history(
            ...     developer_jwt=dev_jwt,
            ...     agent_id="agent-abc123",
            ...     limit=50
            ... )
            >>> for msg in history['messages']:
            ...     print(f"{msg['role']}: {msg['content']}")
        """
        check_type("developer_jwt", developer_jwt, str)
        check_type("agent_id", agent_id, str)
        check_type("limit", limit, int)

        response = self._request(
            "GET",
            "Conversations",
            f"/agents/{agent_id}/history",
            headers=self._get_auth_headers(developer_jwt),
            params={"limit": limit},
        )
        return response
