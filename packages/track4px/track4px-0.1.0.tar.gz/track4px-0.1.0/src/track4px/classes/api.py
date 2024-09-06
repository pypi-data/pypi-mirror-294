from datetime import datetime

import json

from .http import HTTPRequest
from .shipment import Shipment, Event

class Track4PX:
    """ 4PX API 
    
    This API is used to track packages from 4PX.
    """

    SEARCH = "https://track.4px.com/track/v2/front/listTrackV3"

    def tracking(self, tracking_number: str, **kwargs):
        """ Search for a tracking number """

        wrap = kwargs.get("wrap", False)

        request = HTTPRequest(self.SEARCH)

        payload = {
            "queryCodes": [tracking_number],
            "language": "en-us"
        }

        request.add_json_payload(payload)

        response = request.execute()

        if not wrap:
            return response

        """
        {"result":1,"message":"操作成功","data":[{"queryCode":"4PX3001291278502CN","serverCode":"06215215333330","shipperCode":"4PX3001291278502CN","channelTrackCode":null,"ctStartCode":"CN","ctEndCode":"AT","ctEndName":"AT","ctStartName":"China","status":1,"duration":3.0,"tracks":[{"tkCode":"FPX_I_RCUK","tkDesc":"Released from customs: customs cleared.","tkLocation":"","tkTimezone":null,"tkDate":"2024-09-05T18:18:00.000+0000","tkDateStr":"2024-09-06 02:18:00","tkCategoryCode":"I","tkCategoryName":"Import Clearance","spTkSummary":null,"spTkZipCode":null},{"tkCode":"FPX_M_ATA","tkDesc":"Arrival to the destination airport","tkLocation":"","tkTimezone":"UTC+02:00","tkDate":"2024-09-05T16:18:00.000+0000","tkDateStr":"2024-09-06 00:18:00","tkCategoryCode":"M","tkCategoryName":"Transiting by Air or Ship","spTkSummary":null,"spTkZipCode":null},{"tkCode":"FPX_M_DFOA","tkDesc":"Departure from the original airport","tkLocation":"","tkTimezone":"UTC+08:00","tkDate":"2024-09-05T05:09:00.000+0000","tkDateStr":"2024-09-05 13:09:00","tkCategoryCode":"M","tkCategoryName":"Transiting by Air or Ship","spTkSummary":null,"spTkZipCode":null},{"tkCode":"FPX_M_HA","tkDesc":"Hand over to airline.","tkLocation":"","tkTimezone":"UTC+08:00","tkDate":"2024-09-04T07:07:11.000+0000","tkDateStr":"2024-09-04 15:07:11","tkCategoryCode":"M","tkCategoryName":"Transiting by Air or Ship","spTkSummary":null,"spTkZipCode":null},{"tkCode":"FPX_C_ADFF","tkDesc":"Depart from facility to service provider.","tkLocation":"ShaTian,DongGuan","tkTimezone":"UTC+08:00","tkDate":"2024-09-03T00:19:17.000+0000","tkDateStr":"2024-09-03 08:19:17","tkCategoryCode":"C","tkCategoryName":"Operations in Warehouse","spTkSummary":null,"spTkZipCode":null},{"tkCode":"FPX_C_AAF","tkDesc":"Shipment arrived at facility and measured.","tkLocation":"ShaTian,DongGuan","tkTimezone":"UTC+08:00","tkDate":"2024-09-02T17:19:48.000+0000","tkDateStr":"2024-09-03 01:19:48","tkCategoryCode":"C","tkCategoryName":"Operations in Warehouse","spTkSummary":null,"spTkZipCode":null},{"tkCode":"FPX_C_SPLS","tkDesc":"4px picked up shipment.","tkLocation":"ShaTian,DongGuan","tkTimezone":"UTC+08:00","tkDate":"2024-09-02T17:19:47.000+0000","tkDateStr":"2024-09-03 01:19:47","tkCategoryCode":"C","tkCategoryName":"Operations in Warehouse","spTkSummary":null,"spTkZipCode":null},{"tkCode":"FPX_O_IR","tkDesc":"Order data transmitted","tkLocation":"AUSTRIA","tkTimezone":"UTC+01:00","tkDate":"2024-09-02T11:30:00.000+0000","tkDateStr":"2024-09-02 19:30:00","tkCategoryCode":null,"tkCategoryName":null,"spTkSummary":null,"spTkZipCode":null},{"tkCode":"FPX_L_RPIF","tkDesc":"Parcel information received","tkLocation":"","tkTimezone":"UTC+08:00","tkDate":"2024-09-02T06:30:19.000+0000","tkDateStr":"2024-09-02 14:30:19","tkCategoryCode":"L","tkCategoryName":"Picking in Origin Country","spTkSummary":null,"spTkZipCode":null}],"hawbCodeSet":["4PX3001291278502CN","06215215333330"],"mutiPackage":false,"masterOrderNum":null,"returnStatusFlag":null,"channelContact":null}],"tag":"21"}
        """

        shipment = Shipment()
        shipment.tracking_number = response["data"][0]["queryCode"]
        shipment.courier = self.__class__.__name__

        shipment.events = []

        for event in response["data"][0]["tracks"]:
            event_obj = Event()

            if "tkLocation" in event and event["tkLocation"]:
                event_obj.location = event["tkLocation"]

            event_obj.category = event["tkCategoryName"]
            event_obj.timestamp = datetime.strptime(event["tkDate"], "%Y-%m-%dT%H:%M:%S.%f%z")
            event_obj.description = event['tkDesc']
            event_obj.raw = json.dumps(event)

            shipment.events.append(event_obj)

        shipment.raw = json.dumps(response)

        return shipment
