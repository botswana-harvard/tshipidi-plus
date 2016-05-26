import asyncio
import pandas as pd
import json
import pytz
from datetime import date, datetime
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from edc_constants.constants import CLOSED

from call_manager.models import Call

from ..models import TshipidiSubject

tz = pytz.timezone(settings.TIME_ZONE)


class StatisticsView(TemplateView):
    template_name = 'home.html'

    def __init__(self):
        self._response_data = {}
        self.columns = [
            'consented',
            'consented_today',
            'contacted_retry',
            'contacted_today',
            'not_consented',
            'not_contacted',
            'not_interviewed',
            'tshipidi_subjects']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            title=settings.PROJECT_TITLE,
            project_name=settings.PROJECT_TITLE,
        )
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(StatisticsView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if request.is_ajax():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop = asyncio.get_event_loop()
            future_a = asyncio.Future()
            future_b = asyncio.Future()
            tasks = [
                self.tshipidi_subject_data(future_a),
                self.contact_data(future_b),
            ]
            loop.run_until_complete(asyncio.wait(tasks))
            self.response_data.update(future_a.result())
            self.response_data.update(future_b.result())
            loop.close()
            return HttpResponse(json.dumps(self.response_data), content_type='application/json')
        return self.render_to_response(context)

    @asyncio.coroutine
    def contact_data(self, future):
        response_data = {}
        calls = Call.objects.filter(call_attempts__gte=1)
        if calls:
            response_data.update(contacted_retry=calls.exclude(call_status=CLOSED).count())
            calls.filter(**self.modified_option)
            if calls:
                response_data.update(contacted_today=calls.count())
        future.set_result(self.verified_response_data(response_data))

    @asyncio.coroutine
    def tshipidi_subject_data(self, future):
        response_data = {}
        columns = ['id', 'contacted', 'consented', 'modified']
        qs = TshipidiSubject.objects.values_list(*columns).all()
        tshipidi_subjects = pd.DataFrame(list(qs), columns=columns)
        if not tshipidi_subjects.empty:
            response_data.update({
                'tshipidi_subjects': int(tshipidi_subjects['id'].count()),
                'not_contacted': int(tshipidi_subjects.query('contacted == False')['contacted'].count()),
                'not_consented': int(tshipidi_subjects.query('consented == False')['consented'].count()),
                'consented': int(tshipidi_subjects.query('consented == True')['consented'].count()),
            })
            d = date.today()
            local_date = tz.localize(datetime(d.year, d.month, d.day, 0, 0, 0))
            tshipidi_subjects = tshipidi_subjects[(tshipidi_subjects['modified'] >= local_date)]
            response_data.update({
                'contacted_today': int(tshipidi_subjects.query('contacted == True')['contacted'].count()),
                'consented_today': int(tshipidi_subjects.query('consented == True')['consented'].count()),
            })
        future.set_result(self.verified_response_data(response_data))

    @property
    def modified_option(self):
        d = date.today()
        local_date = tz.localize(datetime(d.year, d.month, d.day, 0, 0, 0))
        return {'modified__gte': local_date}

    def verified_response_data(self, response_data):
        diff = set(response_data.keys()).difference(set(self.response_data.keys()))
        if diff:
            raise KeyError('Invalid key or keys in response data dictionary. Got {}'.format(diff))
        return response_data

    @property
    def response_data(self):
        if not self._response_data:
            self._response_data = dict(zip(self.columns, len(self.columns) * [0]))
        return self._response_data
