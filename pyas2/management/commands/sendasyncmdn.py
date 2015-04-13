from django.core.management.base import BaseCommand, CommandError
from django.utils.translation import ugettext as _
from pyas2 import models
from pyas2 import init
from pyas2 import as2lib
from email.parser import HeaderParser
from django.utils import timezone
from datetime import datetime, timedelta
import requests
import email.utils
import os

class Command(BaseCommand):
    help = _(u'Send all pending asynchronous mdns to your trading partners')

    def handle(self, *args, **options):
        time_threshold = timezone.now() - timedelta(minutes=init.gsettings['async_mdn_wait'])
        init.logger.info(_(u'Sending all pending asynchronous MDNs'))
        in_pending_mdns = models.MDN.objects.filter(status='P',timestamp__gt=time_threshold)
        for pending_mdn in in_pending_mdns:
            hparser = HeaderParser()
            mdn_headers = hparser.parsestr(pending_mdn.headers)    
            try:
                auth = None
                if pending_mdn.omessage.partner and pending_mdn.omessage.partner.http_auth:
                    auth = (pending_mdn.omessage.partner.http_auth_user, pending_mdn.omessage.partner.http_auth_pass)
                with open(pending_mdn.file,'rb') as payload:
                    requests.post(pending_mdn.return_url, auth=auth, headers = dict(mdn_headers.items()), data = payload)
                pending_mdn.status = 'S'
                models.Log.objects.create(message=pending_mdn.omessage, status='S', text=_(u'Successfully sent asynchrous mdn to partner'))	
            except Exception,e:
                models.Log.objects.create(message=pending_mdn.omessage, status='E', text=_(u'Failed to send asynchrous mdn to partner, error is %s' %e))
            finally:
                pending_mdn.save()
        init.logger.info(_(u'Marking messages waiting for MDNs for more than %s minutes'%init.gsettings['async_mdn_wait']))
        out_pending_msgs = models.Message.objects.filter(status='P',direction='OUT',timestamp__lt=time_threshold)
        for pending_msg in out_pending_msgs:
            sts = _(u'Failed to receive asynchronous MDN within the threshold limit')
            pending_msg.status = 'E'
            pending_msg.adv_status = sts
            models.Log.objects.create(message=pending_msg, status='E', text=sts)
            pending_msg.save()
        init.logger.info(_(u'Successfully processed all pending mdns'))
        self.stdout.write(_(u'Successfully processed all pending mdns'))
