"""  A module to query Transport NSW (Australia) departure times.         """
"""  First created by Dav0815 ( https://pypi.org/user/Dav0815/)           """
"""  Extended by AndyStewart999 ( https://pypi.org/user/andystewart999/ ) """

from datetime import datetime, timedelta
from google.transit import gtfs_realtime_pb2
import requests.exceptions
import requests
import logging
import re
import json #For the output

ATTR_DUE_IN = 'due'

ATTR_ORIGIN_STOP_ID = 'origin_stop_id'
ATTR_ORIGIN_NAME = 'origin_name'
ATTR_DEPARTURE_TIME = 'departure_time'

ATTR_DESTINATION_STOP_ID = 'destination_stop_id'
ATTR_DESTINATION_NAME = 'destination_name'
ATTR_ARRIVAL_TIME = 'arrival_time'

ATTR_ORIGIN_TRANSPORT_TYPE = 'origin_transport_type'
ATTR_ORIGIN_TRANSPORT_NAME = 'origin_transport_name'
ATTR_ORIGIN_LINE_NAME = 'origin_line_name'
ATTR_ORIGIN_LINE_NAME_SHORT = 'origin_line_name_short'
ATTR_CHANGES = 'changes'

ATTR_OCCUPANCY = 'occupancy'

ATTR_REAL_TIME_TRIP_ID = 'real_time_trip_id'
ATTR_LATITUDE = 'latitude'
ATTR_LONGITUDE = 'longitude'

logger = logging.getLogger(__name__)

class TransportNSWv2(object):
    """The Class for handling the data retrieval."""

    # The application requires an API key. You can register for
    # free on the service NSW website for it.
    # You need to register for both the Trip Planner and Realtime Vehicle Position APIs

    def __init__(self):
        """Initialize the data object with default values."""
        self.origin_id = None
        self.destination_id = None
        self.api_key = None
        self.journey_wait_time = None
        self.transport_type = None
        self.strict_transport_type = None
        self.raw_output = None
        self.journeys_to_return = None
        self.info = {
            ATTR_DUE_IN : 'n/a',
            ATTR_ORIGIN_STOP_ID : 'n/a',
            ATTR_ORIGIN_NAME : 'n/a',
            ATTR_DEPARTURE_TIME : 'n/a',
            ATTR_DESTINATION_STOP_ID : 'n/a',
            ATTR_DESTINATION_NAME : 'n/a',
            ATTR_ARRIVAL_TIME : 'n/a',
            ATTR_ORIGIN_TRANSPORT_TYPE : 'n/a',
            ATTR_ORIGIN_TRANSPORT_NAME : 'n/a',
            ATTR_ORIGIN_LINE_NAME : 'n/a',
            ATTR_ORIGIN_LINE_NAME_SHORT : 'n/a',
            ATTR_CHANGES : 'n/a',
            ATTR_OCCUPANCY : 'n/a',
            ATTR_REAL_TIME_TRIP_ID : 'n/a',
            ATTR_LATITUDE : 'n/a',
            ATTR_LONGITUDE : 'n/a'
            }

    def get_trip(self, name_origin, name_destination , api_key, journey_wait_time = 0, transport_type = 0, \
                 strict_transport_type = False, raw_output = False, journeys_to_return = 1):
        """Get the latest data from Transport NSW."""
        fmt = '%Y-%m-%dT%H:%M:%SZ'

        self.name_origin = name_origin
        self.destination = name_destination
        self.api_key = api_key
        self.journey_wait_time = journey_wait_time
        self.transport_type = transport_type
        self.strict_transport_type = strict_transport_type
        self.raw_output = raw_output
        self.journeys_to_return = journeys_to_return

        # This query always uses the current date and time - but add in any 'journey_wait_time' minutes
        now_plus_wait = datetime.now() + timedelta(minutes = journey_wait_time)
        itdDate = now_plus_wait.strftime('%Y%m%d')
        itdTime = now_plus_wait.strftime('%H%M')

        # We don't control how many journeys are returned any more, so need to be careful of running out of valid journeys if there is a filter in place, particularly a strict filter
        # It would be more efficient to return one journey, check if the filter is met and then retrieve the next one via a new query if not, but for now we'll only be making use of the journeys we've been given

        # Build the entire URL
        url = \
            'https://api.transport.nsw.gov.au/v1/tp/trip?' \
            'outputFormat=rapidJSON&coordOutputFormat=EPSG%3A4326' \
            '&depArrMacro=dep&itdDate=' + itdDate + '&itdTime=' + itdTime + \
            '&type_origin=any&name_origin=' + self.name_origin + \
            '&type_destination=any&name_destination=' + self.destination + \
            '&TfNSWTR=true'
            # '&calcNumberOfTrips=' + str(journeys_to_retrieve) + \


        auth = 'apikey ' + self.api_key
        header = {'Accept': 'application/json', 'Authorization': auth}

        # Send the query and return an error if something goes wrong
        # Otherwise store the response
        try:
            response = requests.get(url, headers=header, timeout=10)
        except:
            logger.warning("Network or Timeout error")
            return error_return(self.info, raw_output)

        # If we get bad status code, log error and return with n/a or an empty string
        if response.status_code != 200:
            logger.warning("Error with the request sent; check api key")
            return error_return(self.info, raw_output)

        # Parse the result as a JSON object
        result = response.json()

        # The API will always return a valid trip, so it's just a case of grabbing what we need...
        # We're only reporting on the origin and destination, it's out of scope to discuss the specifics of the ENTIRE journey
        # This isn't a route planner, just a 'how long until the next journey I've specified' tool
        # The assumption is that the travelee will know HOW to make the defined journey, they're just asking WHEN it's happening next
        # All we potentially have to do is find the first trip that matches the transport_type filter

        if raw_output == True:
            # Just return the raw output
            return json.dumps(result)
            exit

        retrieved_journeys = len(result['journeys'])
        print ("retrieved_journeys = " + str(retrieved_journeys))

        # Loop through the results applying filters where required, and generate the appropriate JSON output including an array of in-scope trips
        json_output=''
        found_journeys = 0
        no_valid_journeys = False

        for current_journey_index in range (0, retrieved_journeys, 1):
            print(current_journey_index)
            if transport_type == 0:
                # Just grab the next trip
                journey = result['journeys'][current_journey_index]
                next_journey_index = current_journey_index + 1
            else:
                # Look for a trip with a matching class filter in at least one of its legs.  Either ANY, or the first leg, depending on how strict we're being
                print ("transport_type = " + str(transport_type))
                journey, next_journey_index = self.find_next_journey(result['journeys'], current_journey_index, transport_type, strict_transport_type)
                if (journey is None):
                    print ("Just called find_next_journey")
                    print ("journey is None")

            if ((journey is None) or (journey['legs']) is None):
                print ("This journey isn't valid, moving to the next one")

            else:
                legs = journey['legs']
                first_leg = self.find_first_leg(legs, transport_type, strict_transport_type)
                last_leg = self.find_last_leg(legs, transport_type, strict_transport_type)
                changes = self.find_changes(legs, transport_type)

                origin = first_leg['origin']
                first_stop = first_leg['destination']
                destination = last_leg['destination']
                transportation = first_leg['transportation']

                # Origin info
                origin_stop_id = origin['id']
                origin_name = origin['name']
                origin_departure_time = origin['departureTimeEstimated']

                # How long until it leaves?
                due = self.get_due(datetime.strptime(origin_departure_time, fmt))

                # Destination info
                destination_stop_id = destination['id']
                destination_name = destination['name']
                destination_arrival_time = destination['arrivalTimeEstimated']

                # Origin type info - train, bus, etc
                origin_mode_temp = transportation['product']['class']
                origin_mode = self.get_mode(origin_mode_temp)
                origin_mode_name = transportation['product']['name']

                # RealTimeTripID info so we can try and get the current location later
                realtimetripid = 'n/a'
                if 'properties' in transportation:
                    if 'RealtimeTripId' in transportation['properties']:
                        realtimetripid = transportation['properties']['RealtimeTripId']

                # Line info
                origin_line_name_short = "unknown"
                if 'disassembledName' in transportation:
                    origin_line_name_short = transportation['disassembledName']

                origin_line_name = "unknown"
                if 'number' in transportation:
                    origin_line_name = transportation['number']

                # Occupancy info, if it's there
                occupancy = 'unknown'
                if 'properties' in first_stop:
                    if 'occupancy' in first_stop['properties']:
                        occupancy = first_stop['properties']['occupancy']

                # Now might be a good time to see if we can also find the latitude and longitude
                # Using the Realtime Vehicle Positions API
                latitude = 'n/a'
                longitude = 'n/a'

                if realtimetripid != 'n/a':
                    # Build the URL
                    url = \
                        'https://api.transport.nsw.gov.au/v1/gtfs/vehiclepos' \
                        + self.get_url(origin_mode)
                    auth = 'apikey ' + self.api_key
                    header = {'Authorization': auth}

                    response = requests.get(url, headers=header, timeout=10)
                    # Only try and process the results if we got a good return code
                    if response.status_code == 200:
                        # Search the feed and see if we can find the trip_id
                        # If we do, capture the latitude and longitude
                        feed = gtfs_realtime_pb2.FeedMessage()
                        feed.ParseFromString(response.content)

                        # Unfortunately we need to do some mucking about for train-based trip_ids
                        # Define the appropriate regular expression to search for - usually just the full text
                        print ( feed.entity[0] )
                        bFindLocation = True

                        if origin_mode == 'Train':
                            triparray = realtimetripid.split('.')
                            if len(triparray) == 7:
                                trip_id_wild = triparray[0] + '.' + triparray[1] + '.' + triparray[2] + '.+.' + triparray[4] + '.' + triparray[5] + '.' + triparray[6]
                            else:
                                # Hmm, it's not the right length (this happens rarely) - give up
                                bFindLocation = False
                        else:
                            trip_id_wild = realtimetripid

                        if bFindLocation:
                            reg = re.compile(trip_id_wild)

                            for entity in feed.entity:
                                if bool(re.match(reg, entity.vehicle.trip.trip_id)):
                                    latitude = entity.vehicle.position.latitude
                                    longitude = entity.vehicle.position.longitude
                                    # We found it, so break out
                                    break

                    self.info = {
                        ATTR_DUE_IN: due,
                        ATTR_ORIGIN_STOP_ID : origin_stop_id,
                        ATTR_ORIGIN_NAME : origin_name,
                        ATTR_DEPARTURE_TIME : origin_departure_time,
                        ATTR_DESTINATION_STOP_ID : destination_stop_id,
                        ATTR_DESTINATION_NAME : destination_name,
                        ATTR_ARRIVAL_TIME : destination_arrival_time,
                        ATTR_ORIGIN_TRANSPORT_TYPE : origin_mode,
                        ATTR_ORIGIN_TRANSPORT_NAME: origin_mode_name,
                        ATTR_ORIGIN_LINE_NAME : origin_line_name,
                        ATTR_ORIGIN_LINE_NAME_SHORT : origin_line_name_short,
                        ATTR_CHANGES: changes,
                        ATTR_OCCUPANCY : occupancy,
                        ATTR_REAL_TIME_TRIP_ID : realtimetripid,
                        ATTR_LATITUDE : latitude,
                        ATTR_LONGITUDE : longitude
                        }

                    found_journeys = found_journeys + 1

                    # Add to the return array
                    if (no_valid_journeys == True):
                        break

                    if (found_journeys >= 2):
                        json_output = json_output + ',' + json.dumps(self.info)
                    else:
                        json_output = json_output + json.dumps(self.info)

                    if (found_journeys == journeys_to_return):
                        break

                    current_journey_index = next_journey_index

        json_output='{"journeys_to_return": ' + str(self.journeys_to_return) + ', "journeys_with_data": ' + str(found_journeys) + ', "journeys": [' + json_output + ']}'
        return json_output


#    def find_first_journey(self, journeys, journeytype, strictness):
#        # Find the first journey that has a leg is of the requested type
#        journey_count = len(journeys)
#        for journey in range (0, journey_count, 1):
#            leg = self.find_first_leg(journeys[journey]['legs'], journeytype, strictness)
#            if leg is not None:
#                return journeys[journey]
#
#        # Hmm, we didn't find one
#        return None


    def find_next_journey(self, journeys, start_journey_index, journeytype, strict):
        # Fnd the next journey that has a leg of the requested type
        journey_count = len(journeys)
        print ("(find_next_journey): start_journey_index = " + str(start_journey_index))
        print ("(find_next_journey): journey_count = " + str(journey_count))

        # Some basic error checking
        if start_journey_index > journey_count:
            print ("None, None")
            return None, None

        for journey_index in range (start_journey_index, journey_count, 1):
            leg = self.find_first_leg(journeys[journey_index]['legs'], journeytype, strict)
            if leg is not None:
                print ("leg is not None")
                return journeys[journey_index], journey_index + 1
            else:
                print ("leg is None, None")
                return None, None

        # Hmm, we didn't find one
        return None, None


    def find_first_leg(self, legs, legtype, strict):
        # Find the first leg of the requested type
        leg_count = len(legs)
        print ("leg_count = " + str(leg_count))
        for leg_index in range (0, leg_count, 1):
            leg_class = legs[leg_index]['transportation']['product']['class']
            print("leg_class = " + str(leg_class))
            # We've got a filter, and the leg type matches it, so return that leg
            if legtype != 0 and leg_class == legtype:
                return legs[leg_index]

            # We don't have a filter, and this is the first non-walk/cycle leg so return that leg
            if  legtype == 0 and leg_class < 99:
                return legs[leg_index]

            # Exit if we're doing strict filtering and we haven't found that type in the first leg
            if legtype != 0 and strict == True:
                return None

        # Hmm, we didn't find one
        print ("Fell through to None")
        return None


    def find_last_leg(self, legs, legtype, strict):
        # Find the last leg of the requested type
        leg_count = len(legs)
        for leg_index in range (leg_count - 1, -1, -1):
            leg_class = legs[leg_index]['transportation']['product']['class']

            # We've got a filter, and the leg type matches it, so return that leg
            if legtype != 0 and leg_class == legtype:
                return legs[leg_index]

            # We don't have a filter, and this is the first non-walk/cycle leg so return that leg
            if  legtype == 0 and leg_class < 99:
                return legs[leg_index]

            # Exit if we're doing strict filtering and we haven't found that type in the first leg
            if legtype != 0 and strict == True:
                return None

        # Hmm, we didn't find one
        return None


    def find_changes(self, legs, legtype):
        # Find out how often we have to change
        changes = 0
        leg_count = len(legs)

        for leg_index in range (0, leg_count, 1):
            leg_class = legs[leg_index]['transportation']['product']['class']
            if leg_class == legtype or legtype == 0:
                changes = changes + 1

        return changes - 1


    def get_mode(self, iconId):
        """Map the iconId to a full text string"""
        modes = {
            1: "Train",
            4: "Light rail",
            5: "Bus",
            7: "Coach",
            9: "Ferry",
            11: "School bus",
            99: "Walk",
            100: "Walk",
            107: "Cycle"
        }
        return modes.get(iconId, None)


    def get_url(self, mode):
        """Map the journey mode to the proper real time location URL """

        url_options = {
            "Train"      : "/sydneytrains",
            "Light rail" : "/lightrail/innerwest",
            "Bus"        : "/buses",
            "Coach"      : "/buses",
            "Ferry"      : "/ferries/sydneyferries",
            "School bus" : "/buses"
        }
        return url_options.get(mode, None)


    def get_due(self, estimated):
        """Min until departure"""
        due = 0
        if estimated > datetime.utcnow():
            due = round((estimated - datetime.utcnow()).seconds / 60)
        return due
