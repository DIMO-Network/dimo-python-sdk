class Telemetry:
    def __init__(self, dimo_instance):
        self.dimo = dimo_instance
    
    # Primary query method
    def query(self, query, token):
        return self.dimo.query('Telemetry', query, token=token)
    
    # Sample query - get signals latest
    def get_signals_latest(self, token, token_id):
        query = """
        query GetSignalsLatest($tokenId: Int!) {
            signalsLatest(tokenId: $tokenId){
                powertrainTransmissionTravelledDistance{
                    timestamp
                    value
                }
                exteriorAirTemperature{
                    timestamp
                    value
                }
                speed {
                    timestamp
                    value
                }
                powertrainType{
                    timestamp
                    value
                }
            }
        }
        """
        variables = {
            "tokenId": token_id
        }

        return self.dimo.query('Telemetry', query, token=token, variables=variables)
    
    # Sample query - daily signals from autopi
    def get_daily_signals_autopi(self, token, token_id, start_date, end_date):
        query = """
        query GetDailySignalsAutopi($tokenId: Int!, $startDate: Time!, $endDate: Time!) {
            signals(
                tokenId: $tokenId,
                interval: "24h",
                from: $startDate, 
                to: $endDate,
                filter: {
                    source: "autopi"
                })
                {
                    speed(agg: MED)
                    powertrainType(agg: RAND)
                    powertrainRange(agg: MIN) 
                    exteriorAirTemperature(agg: MAX)
                    chassisAxleRow1WheelLeftTirePressure(agg: MIN)
                    timestamp
                }
            }
            """
        variables = {
            "tokenId": token_id,
            "startDate": start_date,
            "endDate": end_date
        }

        return self.dimo.query('Telemetry', query, token=token, variables=variables)
    
    # Sample query - daily average speed of a specific vehicle
    def get_daily_average_speed(self, token, token_id, start_date, end_date):
        query = """
        query GetDailyAverageSpeed($tokenId: Int!, $startDate: Time!, $endDate: Time!) {
         signals (
            tokenId: $tokenId,
            from: $startDate,
            to: $endDate,
            interval: "24h"
            )
        {
            timestamp
            avgSpeed: speed(agg: AVG)
        }
        }
        """
        variables = {
            "tokenId": token_id,
            "startDate": start_date,
            "endDate": end_date
        }

        return self.dimo.query('Telemetry', query, token=token, variables=variables)
    
    # Sample query - daily max speed of a specific vehicle
    def get_daily_max_speed(self, token, token_id, start_date, end_date):
        query = """
        query GetMaxSpeed($tokenId: Int!, $startDate: Time!, $endDate: Time!) {
            signals(
                tokenId: $tokenId,
                from: $startDate,
                to: $endDate,
                interval: "24h"
            )
        {
            timestamp
            maxSpeed: speed(agg: MAX)
        }
        }
        """
        variables = {
            "tokenId": token_id,
            "startDate": start_date,
            "endDate": end_date
        }

        return self.dimo.query('Telemetry', query, token=token, variables=variables)
    
    # TODO: Update with Attestation API 
    # Sample query - get the VIN of a specific vehicle 
    # async def get_vin(self, token, token_id):
    #     query = """
    #     query GetVIN($tokenId: Int!) {
    #         vinVCLatest (tokenId: $tokenId) {
    #             vin
    #         }
    #     }"""
    #     variables = {
    #         "tokenId": token_id
    #     }

    #     return await self.dimo.query('Telemetry', query, token=token, variables=variables)

