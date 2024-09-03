import pandas as pd
from rest_adaptor import RestAdaptor
from utilis.utilis import remove_empty_params
from helpers.helpers import multiple_json_normalize
from typing import Union
import websocket
import json

"""
TODO: create a method for POST BMS device setpoints
"""


class MeasurementsResource(RestAdaptor):

    """
    Class for measurements resource.


    args:
        resource - measurements resource endpoint
    
    """

    def __init__(
            self,
            rest_adaptor: RestAdaptor) -> None:
        
        super().__init__(
            user=rest_adaptor.user,
            password=rest_adaptor.password
        )
        self.resource = '/measurement/measurements'


    def get_all_measurements(self, id:str, date_start:str, date_end:str, **kwargs) -> Union[pd.DataFrame,str]:
        """
        return all Result data available as pandas dataframe.
        args:
            id - device id. see device_list.csv for reference.
            date_start - start date of measurement. format YYYY-MM-DD
            date_end - end date of measurment. format YYYY-MM-DD
            kwargs - (optional params) https://www.cumulocity.com/api/core/#operation/getMeasurementCollectionResource
        """
        kwargs = kwargs or {}
        request_params ={
            'dateFrom': date_start,
            'dateTo': date_end,
            'currentPage': 1,
            'pageSize': 2000,
            'valueFragmentType': kwargs.get('valueFragmentType'),
            'valueFragmentSeries': kwargs.get('valueFragmentSeries'),
            'source': id,
            'revert': kwargs.get('revert'),
            **kwargs
        }

        request_params = remove_empty_params(request_params)

        results_df = pd.DataFrame()
        result_messages = []
        while True:
            result = self.get(endpoint = self.resource, ep_params=request_params)
            result_data_measurements = result.data.get('measurements',None)
            result_messages.append(result.message)
            if not result_data_measurements:
                break
            df = multiple_json_normalize(result_data_measurements)
            results_df = pd.concat([results_df,df],ignore_index=True)
            request_params['currentPage'] +=1

        pages_scraped = len(result_messages)
        ok = result_messages.count('OK')
        message = f"{ok}/{pages_scraped} pages scraped successfully."

        return results_df,message

    def get_all_aggregated_measurements(
            self, 
            aggregate_period:str, 
            id:str, 
            date_start:str,
            date_end:str, 
            **kwargs
              ) -> Union[pd.DataFrame,str]:
        """
        return all min max value of the aggregated period data as pandas dataframe. 
        result will provide up to 5000 values. Reduce the date range if required.
        args:
            id - device id. see device_list.csv for reference.
            aggregation_type - aggregation period for the data. Accept "DAILY" "HOURLY" "MINUTELY"
            date_start - start date of measurement
            date_end - end date of measurment.
            kwargs - (optional params) https://www.cumulocity.com/api/core/#operation/getMeasurementSeriesResource
        """

        request_params ={
            'aggregationType': aggregate_period,
            'dateFrom': date_start,
            'dateTo': date_end,
            'type': kwargs.get('type'), #don't use it for source only method
            'series': kwargs.get('valueFragmentSeries'),
            'source': id,
            'revert': kwargs.get('revert'),
            **kwargs

        }

        resource = self.resource + '/series'

        request_params = remove_empty_params(request_params)
        result = self.get(endpoint = resource, ep_params=request_params)
        results_data = result.data

        df = multiple_json_normalize(results_data, id, aggregated=True)

        additional = ''
        if result.data.get('truncated'):
            additional = f'data is trancated. Reduce the date range of the query'

        rows = len(df)
        message = f"{rows} {aggregate_period} aggregated data return successfully.{additional}"
            
        return df, message
    
    def set_operation(self, OPC_tag:str, value:Union[str,float], description:str = '') -> str:
        """
        To control the selected BMS devices via the OPC_tag.
        args:  
            OPC_tag - address of the device to be controlled.
            value - value to be set.


        """
        resource = '/devicecontrol/operations'

        body = {
                "deviceId": "78194421", #fixed, BMS VM
                "c8y_ua_command_WriteValue": {
                    "values": {
                        {OPC_tag}: {
                            "value": f"{value}"
                        }
                    }
                },
                "description": {description}
            }

        result = self.post(endpoint = resource, data= body)
        message = result.message
        print(message)



    def __stream_measurements(self, id:str, stream_method = 'application/json-stream', timeout=10) -> None:
        """
        WIP
        stream measurements from the selected device.
        args:
            id - device id. see device_list.csv for reference.
            stream_method - stream method. default is application/json-stream.
        """
        url = self.base_url +  self.resource

        stream_method_type = ('application/json-stream','text/csv', 'application/vnd.ms-excel', 'application/xlsx')

        if stream_method not in stream_method_type:
            raise ValueError("Invalid stream_method. Supported methods are: text/csv, application/vnd.ms-excel, application/xlsx")

        #text/csv
        headers = {
            "Accept": stream_method,
            'X-Cumulocity-System-Of-Units': 'metric'
        }

        request_params ={
            'source': id,
            'pageSize': 1
        }
        
        while True:
  
            response = self.get(self.resource, ep_params=request_params, stream = True, headers = headers, timeout=timeout)
            for line in response.iter_lines(decode_unicode=True):
                if line:
                    print(line)

        


    # def stream_measurements(self, id:str):
    #     auth = self.base64_encoded_credential()
    #     url = f'{self.websocket_url}/measurement/notifications'

    #     headers = {
    #         "Authorization": f"Basic {auth}"
    #     }

    #             # Define a callback function to handle incoming messages
    #     def on_message(ws, message):
    #         data = json.loads(message)
    #         print(f"Received measurement notification: {data}")

    #     # Define a callback function to handle errors
    #     def on_error(ws, error):
    #         print(f"Error: {error}")

    #     # Define a callback function to handle connection closure
    #     def on_close(ws):
    #         print("### WebSocket closed ###")

    #     # Define a callback function to handle successful connection
    #     def on_open(ws):
    #         print("WebSocket connection opened")

    #         subscription_message = {
    #             "channel": f"/measurements/{id}"
    #         }

    #         ws.send(json.dumps(subscription_message))
    #         print(f"Subscribed to /measurements/{id}")

    #     # Create WebSocket connection
    #     ws = websocket.WebSocketApp(
    #         url,
    #         header=headers,
    #         on_message=on_message,
    #         on_error=on_error,
    #         on_close=on_close
    #     )

    #     # Start the WebSocket connection and run it indefinitely
    #     ws.on_open = on_open
    #     ws.run_forever()


 