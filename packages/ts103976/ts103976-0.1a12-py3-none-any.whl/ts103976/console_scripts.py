import logging
import argparse
import sys
import json

from .lea import LEA
from .rps import RPS, DeliveryBehaviourEnum

from .validator import TS103120Validator, TS103976Validator

def lea_console():
    parser = argparse.ArgumentParser(
        description="Generates JSON messages for simple example requests following TS 103 976, \
                                          encapsulated in TS 103 120. This is an example implementation for testing \
                                          and demonstration purposes, and should not be used in production environments.",

    )
    parser.add_argument("-s", "--sendercc", default="XX", help="Sender Country Code used in the TS 103 120 header")
    parser.add_argument("-u", "--senderid", default="SENDER", help="Sender Unique ID used in the TS 103 120 header")
    parser.add_argument("-r", "--receivercc", default="XX", help="Receiver Country Code used in the TS 103 120 header")
    parser.add_argument("-i", "--receiverid", default="RECEIVER", help="Receiver Unique ID used in the TS 103 120 header")
    parser.add_argument("-t", "--taskref", default="XX-1-234", help="Task Reference (LDID) used in the TS 103 120 LDTaskRequest")
    parser.add_argument("-d", "--deliveryurl", help="Delivery URL included in the TS 103 120 LDTaskRequest, as a destination for results")

    group = parser.add_mutually_exclusive_group()
    group.add_argument("-v", "--vin", help="VIN to query as a RequestValue in the TS 103 120 LDTaskRequest")
    group.add_argument("-m", "--imsi", help="IMSI to query as a RequestValue in the TS 103 120 LDTaskRequest")

    args = parser.parse_args()

    lea = LEA(args.sendercc, args.senderid, args.deliveryurl)

    if (args.vin is not None):        
        json_doc = lea.generate_vin_to_comms_id(
            args.receivercc, args.receiverid, args.taskref, args.vin
        )
    elif (args.imsi is not None):
        json_doc = lea.generate_comms_id_to_vin(
            args.receivercc, args.receiverid, args.taskref, args.imsi
        )
    else:
        json_doc = lea.generate_vin_to_comms_id(
            args.receivercc, args.receiverid, args.taskref, "1G9Y817H34LSP7293"
        )

    print(json.dumps(json_doc))


def rps_console():
    parser = argparse.ArgumentParser(
        description="Responds to JSON messages for simple example requests following TS 103 976, \
                     encapsulated in TS 103 120, and produces simple example responses. \
                     TS 103 120 response messages will be written to stdout. The DELIVER message \
                     containing any results will either be set to the delivery address specified in the LDTaskRequest \
                     or written to disk\
                     This is an example implementation for testing \
                     and demonstration purposes, and should not be used in production environments.",
)

    parser.add_argument("-r", "--receivercc", default="XX", help="Receiver Country Code for the TS 103 120 receiver. Messages with other Receiver Country Code values will be rejected unless the '--allowanyid' flag is set.")
    parser.add_argument("-i", "--receiverid", default="RECEIVER", help="Receiver Unique ID for the TS 103 120 receiver. Messages with other Receiver Unique ID values will be rejected unless the '--allowanyid' flag is set.")
    parser.add_argument("-a", "--allowanyid", default=False, help="Respond to messages to any Receiver ID, regardless of the values set by '--receivercc' or '--receiverid'.")
    parser.add_argument("-d", "--delivery", type=lambda b: DeliveryBehaviourEnum.from_string(b), choices=list(DeliveryBehaviourEnum), default=DeliveryBehaviourEnum.SKIPDELIVERY, help="Behaviour if a request does not specify a delivery address")
    parser.add_argument("--defaultaddress", default=None, help="Default delivery address. Implies --delivery delivertodefault")
    parser.add_argument("-j", "--input", type=argparse.FileType("r"), default=sys.stdin, help="Path to input file (if absent, stdin is used)")
    parser.add_argument("-v", "--verbose", action="count", help="Verbosity. Can be specified multiple times for extra verbosity")

    args = parser.parse_args()

    match args.verbose:
        case None:
            logging.basicConfig(level=logging.ERROR)
        case 1:
            logging.basicConfig(level=logging.WARN)
        case 2:
            logging.basicConfig(level=logging.INFO)
        case 3:
            logging.basicConfig(level=logging.DEBUG)

    logging.debug(args)
    
    instance_doc = json.loads(args.input.read())
    args.input.close()
    logging.debug("Input:")
    logging.debug(instance_doc)

    logging.debug("Creating RPS instance")
    rps = RPS(args.receivercc, args.receiverid, args.allowanyid, args.delivery, args.defaultaddress)
    
    logging.debug("Responding to input")
    response = rps.respond_to(instance_doc)
    
    logging.debug("Response from RPS")
    print(json.dumps(response))


def search_key(data, key, path=""):
    if type(data) is  dict:
        for k, v in data.items():
            path="{0} -> {1}".format(path, k)
            if k == key or v == key:
                return (k, v, path)
            res = search_key(data[k], key, path)
            if res is not None:
                return res
    if type(data) is list:
        for v in data:
            res = search_key(v, key, path)
            if res is not None:
                return res

def lea_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument("-j", "--input", type=argparse.FileType("r"), default=sys.stdin, help="Path to input file (if absent, stdin is used)")

    args = parser.parse_args()
    instance_doc = args.input.read()
    json_doc = json.loads(instance_doc)
    args.input.close()

    validator = TS103120Validator()
    errors = validator.validate(json_doc)
    if len(errors) > 0:
        for error in errors:
            print(error)
    else:
        print ("TS103120 validation OK")

    # quick and dirty
    _, json_data, _ = search_key(json_doc, 'delivery:JSONData')
    if json_data is None:
        raise Exception('No delivery:JSONData key found')

    inner_validator = TS103976Validator()
    errors = inner_validator.validate(json_data)
    if len(errors) > 0:
        for error in errors:
            print(error)
    else:
        print ("TS103976 validation OK")

    print ("Done")
   