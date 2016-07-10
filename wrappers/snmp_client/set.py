from pysnmp.carrier.asyncore.dispatch import AsyncoreDispatcher
from pysnmp.carrier.asyncore.dgram import udp
from pyasn1.codec.ber import encoder, decoder
from pysnmp.proto import api
from time import time

__author__ = 'Amir H.'


class Set:
    network_address = None
    community = None
    port = None
    timeout = None
    retry = None
    oid_keys_enc_val = None  # format: ((oid, encoding, value), )

    def __init__(self, data, timeout_func=None, receive_func=None, error_func=None):
        self.__dict__.update(data)

        self.timeout_func = timeout_func
        self.receive_func = receive_func
        self.error_func = error_func

        self.pMod = pMod = api.protoModules[api.protoVersion2c]

        self.reqPDU = reqPDU = pMod.SetRequestPDU()
        pMod.apiPDU.setDefaults(reqPDU)

        pMod.apiPDU.setVarBinds(reqPDU,
                                map(lambda a: (a[0], pMod.OctetString(str(a[2]))) if a[1] == 'str'
                                    else (a[0], pMod.Integer(int(a[2]))), self.oid_keys_enc_val))

        reqMsg = pMod.Message()
        pMod.apiMessage.setDefaults(reqMsg)
        pMod.apiMessage.setCommunity(reqMsg, self.community)
        pMod.apiMessage.setPDU(reqMsg, reqPDU)

        self.startedAt = time()

        transportDispatcher = AsyncoreDispatcher()
        transportDispatcher.registerRecvCbFun(self.cbRecvFun)
        transportDispatcher.registerTimerCbFun(self.cbTimerFun)

        # UDP/IPv4
        transportDispatcher.registerTransport(udp.domainName, udp.UdpSocketTransport().openClientMode())
        transportDispatcher.sendMessage(encoder.encode(reqMsg), udp.domainName, (self.network_address, self.port))
        transportDispatcher.jobStarted(1)

        transportDispatcher.runDispatcher()
        transportDispatcher.closeDispatcher()

    def cbTimerFun(self, timeNow):
        if timeNow - self.startedAt > self.timeout:
            if self.timeout_func:
                self.timeout_func(network_address=self.network_address,
                                  oid_keys=[i[0] for i in self.oid_keys_enc_val])
            else:
                raise TimeoutError("Request timed out")

    def cbRecvFun(self, transportDispatcher, transportDomain, transportAddress, wholeMsg, reqPDU=None):
        reqPDU = self.reqPDU if reqPDU is None else reqPDU
        while wholeMsg:
            rspMsg, wholeMsg = decoder.decode(wholeMsg, asn1Spec=self.pMod.Message())
            rspPDU = self.pMod.apiMessage.getPDU(rspMsg)
            if self.pMod.apiPDU.getRequestID(reqPDU) == self.pMod.apiPDU.getRequestID(rspPDU):
                errorStatus = self.pMod.apiPDU.getErrorStatus(rspPDU)
                if errorStatus:
                    if self.error_func:
                        self.error_func(error_status=errorStatus)
                    else:
                        print(errorStatus.prettyPrint())
                else:
                    if self.receive_func:
                        self.receive_func(network_address=self.network_address,
                                          result_set=((oid, val) for oid, val in self.pMod.apiPDU.getVarBinds(rspPDU)))
                    else:
                        for oid, val in self.pMod.apiPDU.getVarBinds(rspPDU):
                            print('%s = %s' % (oid.prettyPrint(), val.prettyPrint()))
                transportDispatcher.jobFinished(1)
        return wholeMsg
