from pysnmp.carrier.asyncore.dispatch import AsyncoreDispatcher
from pysnmp.carrier.asyncore.dgram import udp
from pyasn1.codec.ber import encoder, decoder
from pysnmp.proto.api import v2c
from time import time

__author__ = 'Amir H.'


class Bulk:
    network_address = None
    community = None
    port = None
    timeout = None
    retry = None
    oid_keys = None
    non_repeaters = None
    max_repetitions = None

    def __init__(self, data, timeout_func=None, receive_func=None, error_func=None):
        self.__dict__.update(data)

        self.timeout_func = timeout_func
        self.receive_func = receive_func
        self.error_func = error_func

        headVars = [v2c.ObjectIdentifier(oid) for oid in
                    map(lambda oid: (int(i) for i in oid.split('.')), self.oid_keys)]

        self.reqPDU = reqPDU = v2c.GetBulkRequestPDU()
        v2c.apiBulkPDU.setDefaults(reqPDU)
        v2c.apiBulkPDU.setNonRepeaters(reqPDU, self.non_repeaters)
        v2c.apiBulkPDU.setMaxRepetitions(reqPDU, self.max_repetitions)
        v2c.apiBulkPDU.setVarBinds(reqPDU, [(x, v2c.null) for x in headVars])

        reqMsg = v2c.Message()
        v2c.apiMessage.setDefaults(reqMsg)
        v2c.apiMessage.setCommunity(reqMsg, self.community)
        v2c.apiMessage.setPDU(reqMsg, reqPDU)

        self.startedAt = time()

        transportDispatcher = AsyncoreDispatcher()
        transportDispatcher.registerRecvCbFun(self.cbRecvFun)
        transportDispatcher.registerTimerCbFun(self.cbTimerFun)

        transportDispatcher.registerTransport(udp.domainName, udp.UdpSocketTransport().openClientMode())
        transportDispatcher.sendMessage(encoder.encode(reqMsg), udp.domainName, (self.network_address, self.port))
        transportDispatcher.jobStarted(1)

        transportDispatcher.runDispatcher()
        transportDispatcher.closeDispatcher()

    def cbTimerFun(self, timeNow):
        if timeNow - self.startedAt > self.timeout:
            if self.timeout_func:
                self.timeout_func(network_address=self.network_address, oid_keys=self.oid_keys)
            else:
                raise TimeoutError("Request timed out")

    def cbRecvFun(self, transportDispatcher, transportDomain, transportAddress, wholeMsg, reqPDU=None, headVars=None):
        # headVars = self.headVars if headVars is None else headVars
        reqPDU = self.reqPDU if reqPDU is None else reqPDU
        while wholeMsg:
            rspMsg, wholeMsg = decoder.decode(wholeMsg, asn1Spec=v2c.Message())
            rspPDU = v2c.apiMessage.getPDU(rspMsg)

            if v2c.apiBulkPDU.getRequestID(reqPDU) == v2c.apiBulkPDU.getRequestID(rspPDU):
                varBindTable = v2c.apiBulkPDU.getVarBindTable(reqPDU, rspPDU)
                errorStatus = v2c.apiBulkPDU.getErrorStatus(rspPDU)
                if errorStatus and errorStatus != 2:
                    errorIndex = v2c.apiBulkPDU.getErrorIndex(rspPDU)
                    if self.error_func:
                        self.error_func(error_status=errorStatus,
                                        error_index=errorIndex and varBindTable[int(errorIndex) - 1] or '?')
                    else:
                        print('%s at %s' % (errorStatus.prettyPrint(),
                                            errorIndex and varBindTable[int(errorIndex) - 1] or '?'))
                    transportDispatcher.jobFinished(1)
                    break

                if self.receive_func:
                    self.receive_func(network_address=transportAddress,
                                      result_set=((name, val) for name, val in (tableRow for tableRow in varBindTable)))
                else:
                    for tableRow in varBindTable:
                        for name, val in tableRow:
                            print('from: %s, %s = %s' % (transportAddress, name.prettyPrint(), val.prettyPrint()))

                for oid, val in varBindTable[-1]:
                    if not isinstance(val, v2c.Null):
                        break
                # else:
                transportDispatcher.jobFinished(1)
        return wholeMsg
