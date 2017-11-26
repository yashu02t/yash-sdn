
from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.util import dpid_to_str, str_to_dpid
from pox.lib.util import str_to_bool
import time

from pox.lib.addresses import IPAddr, IPAddr6, EthAddr


from pox.lib.recoco import Timer

# include as part of the betta branch
from pox.openflow.of_json import *

log = core.getLogger()

# We don't want to flood immediately when a switch connects.
# Can be overriden on commandline.
_flood_delay = 0

class Mitigation(object):
    def __init__ (self, connection, transparent):
        self.connection = connection
        self.transparent = transparent

        self.macToPort = {}
        self.blocked_hosts=[]
        # We want to hear PacketIn messages, so we listen to the connection
        connection.addListeners(self)
        connection.addListenerByName("FlowStatsReceived", self._handle_flowstats_received)

        # We just use this to know when to log a helpful message
        self.hold_down_expired = _flood_delay == 0

        Timer(1, self._timer_func, recurring=True)



    def flood(self,event,message = None):
        msg = of.ofp_packet_out()
        if time.time() - self.connection.connect_time>= _flood_delay:
            if self.hold_down_expired is False:
                self.hold_down_expired = True
                #log.info("%s: Flood hold-down expired -- flooding", dpid_to_str(event.dpid))
            if message is not None: log.debug(message)
            msg.actions.append(of.ofp_action_output(port = of.OFPP_FLOOD))
        else:
            pass
        msg.data = event.ofp
        msg.in_port = event.port
        self.connection.send(msg)

    def drop(self,event,duration = None):
        packet = event.parsed
        if duration is not None:
            if not isinstance(duration, tuple):
                duration = (duration,duration)
                msg = of.ofp_flow_mod()
                msg.match = of.ofp_match.from_packet(packet)
                msg.idle_timeout = duration[0]
                msg.hard_timeout = duration[1]
                msg.buffer_id = event.ofp.buffer_id
                self.connection.send(msg)
            elif event.ofp.buffer_id is not None:
                msg = of.ofp_packet_out()
                msg.buffer_id = event.ofp.buffer_id
                msg.in_port = event.port
                self.connection.send(msg)

    def generate_cookie(self, packet):
        ip = packet.find('ipv4')
        if ip is not None:
            src_ip = ip.srcip.toUnsignedN()
            dst_ip = ip.dstip.toUnsignedN()
            value = src_ip + dst_ip
            return value
        return 0

    def _timer_func (self):
        for conn in core.openflow._connections.values():
            conn.send(of.ofp_stats_request(body=of.ofp_flow_stats_request()))
            #log.debug("Sent %i flow stats request(s)", len(core.openflow._connections))

    def _handle_flowstats_received (self,event):
        web_bytes = 0
        web_packet=0
        hosts_list={}
        ip_set = set()
        #stats = flow_stats_to_list(event.stats)
        #log.debug("FlowStatsReceived from %s: %s", dpidToStr(event.connection.dpid), stats)

        for f in event.stats:
            if f.match.dl_type==0x800 and f.match.nw_proto == 6:
                ip_set.add(f.match.nw_src)

        for i in ip_set:
            web_bytes = 0
            web_packet = 0

            for f in event.stats:
                if f.match.nw_dst == '192.168.56.11' and f.match.nw_src == i and f.match.dl_type==0x800\
                        and f.match.nw_proto==6:
                    web_bytes += f.byte_count
                    web_packet += f.packet_count
                    hosts_list[f]= [web_packet,web_bytes]


        for pkt_event in hosts_list:

            if (pkt_event.match.nw_src,pkt_event.match.nw_dst) in self.blocked_hosts:
                return

            elif hosts_list[pkt_event][0] <= 40:
               log.info( "===== Normal flow %s->%s with packets %s and bytes %s on switch %s. ====" \
                      %(pkt_event.match.nw_src,pkt_event.match.nw_dst,hosts_list[pkt_event][0],hosts_list[pkt_event][1],\
                        dpidToStr(event.connection.dpid)))



            elif hosts_list[pkt_event][0] > 40:
                log.warning( "***Potential Malicious flow %s->%s with packets %s and bytes %s on %s. Block*****" \
                      %(pkt_event.match.nw_src,pkt_event.match.nw_dst,hosts_list[pkt_event][0],hosts_list[pkt_event][1],\
                         dpidToStr(event.connection.dpid)))
                self.blocked_hosts.append((pkt_event.match.nw_src, pkt_event.match.nw_dst))
                msg = of.ofp_flow_mod()
                msg.match = pkt_event.match
                msg.actions.append(of.ofp_action_output(port = of.OFPP_NONE))
                msg.command = of.OFPFC_DELETE
                msg.cookie= pkt_event.cookie
                event.connection.send(msg)


    def process_packet(self, event):
        packet = event.parsed
        if packet.src not in self.macToPort:
            self.macToPort[packet.src] = event.port
        if not self.transparent:
            if packet.type == packet.LLDP_TYPE or packet.dst.isBridgeFiltered():
                self.drop(event)
                return
        if packet.dst.is_multicast:
            #self.flood(event,"Port for %s unknown -- flooding" % (packet.dst)) # 3a
            self.flood(event) # 3a
        else:
            if packet.dst not in self.macToPort:
                self.flood(event)
            else:
                port = self.macToPort[packet.dst]
                if port == event.port:
                    log.warning("Same port for packet from %s -> %s on %s.%s.  Drop."
                                % (packet.src, packet.dst, dpid_to_str(event.dpid), port))
                    self.drop(event,10)
                    return
                #log.debug("installing flow for %s.%i -> %s.%i" %(packet.src, event.port, packet.dst, port))
                ipsrc = ''
                ipdst = ''

                if packet.find('ipv4'):
                    ip = packet.find('ipv4')
                    if ip is not None:
                        ipsrc = ip.srcip
                        ipdst =  ip.dstip
                        log.debug("installing flow for %s.%i -> %s.%i on switch %s"\
                                  %(ipsrc, event.port, ipdst, port,dpid_to_str(event.dpid) ))

                msg = of.ofp_flow_mod()
                msg.cookie=self.generate_cookie(packet)
                msg.flags = of.OFPFF_SEND_FLOW_REM
                msg.match = of.ofp_match.from_packet(packet, event.port)
                msg.idle_timeout = 10
                msg.hard_timeout = 30
                msg.actions.append(of.ofp_action_output(port = port))
                msg.data = event.ofp # 6a
                self.connection.send(msg)
                #log.debug("installing flow for %s.%i -> %s.%i on  %s" \
                         # %(ipsrc, event.port, ipdst, port,dpid_to_str(event.dpid) ))


    def _handle_PacketIn (self, event):
        packet = event.parsed
        flag = False
        if packet.find('tcp'):
            ip = packet.find('ipv4')
            ip_src= ip.srcip
            ip_dst= ip.dstip
            if (ip_src,ip_dst) in self.blocked_hosts:
                flag = True

        if not flag:
            self.process_packet(event)

        if flag:
            log.debug("***Access denied for the blocked host %s -> %s on %s****" \
                      %(ip_src, ip_dst,dpid_to_str(event.dpid) ))

            #self.drop(event)
            pass





class l2_learning (object):

    def __init__ (self, transparent, ignore = None):
        core.openflow.addListeners(self)
        self.transparent = transparent
        self.ignore = set(ignore) if ignore else ()

    def _handle_ConnectionUp (self, event):
        if event.dpid in self.ignore:
            log.debug("Ignoring connection %s" % (event.connection))
            return
        log.debug("Connection %s" % (event.connection))

        Mitigation(event.connection, self.transparent)


def launch (transparent=False, hold_down=_flood_delay, ignore = None):
    try:
        global _flood_delay
        _flood_delay = int(str(hold_down), 10)
        assert _flood_delay >= 0
    except:
        raise RuntimeError("Expected hold-down to be a number")
    if ignore:
        ignore = ignore.replace(',', ' ').split()
        ignore = set(str_to_dpid(dpid) for dpid in ignore)
    core.registerNew(l2_learning, str_to_bool(transparent), ignore)