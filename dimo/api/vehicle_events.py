

class VehicleEvents:

    def __init__(self, request_method, get_auth_headers):
        self._request = request_method
        self._get_auth_headers = get_auth_headers
        
    def list_webhooks(self, developer_jwt: str):
        pass

    def register_webhook(self, developer_jwt: str, request: str):
        pass

    def webhook_signals(self, developer_jwt: str):
        pass

    def update_webhook(self, developer_jwt: str, id: str, request: str):
        pass

    def delete_webhook(self, developer_jwt: str, id: str):
        pass
    
    def vehicle_subscriptions(self, developer_jwt: str):
        pass

    def subscribe_vehicle(self, developer_jwt: str, token_id: str, event_id: str):
        pass

    def unsubscribe_vehicle(self, developer_jwt: str, token_id: str, event_id: str):
        pass
    
    
    