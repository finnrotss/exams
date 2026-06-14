from pathlib import Path

from django.conf import settings


class MetricsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.total_requests = 0
        self.status_2xx = 0
        self.status_4xx = 0
        self.status_5xx = 0
        self.metrics_file = Path(settings.BASE_DIR) / 'metrics.log'

    def __call__(self, request):
        self.total_requests += 1
        response = self.get_response(request)
        status_code = response.status_code

        if 200 <= status_code < 300:
            self.status_2xx += 1
        elif 400 <= status_code < 500:
            self.status_4xx += 1
        elif 500 <= status_code < 600:
            self.status_5xx += 1

        self._write_metrics()
        return response

    def _write_metrics(self) -> None:
        stats = (
            f'Общее количество запросов: {self.total_requests}\n'
            f'2xx: {self.status_2xx}\n'
            f'4xx: {self.status_4xx}\n'
            f'5xx: {self.status_5xx}\n'
        )
        print(stats, end='')
        self.metrics_file.write_text(stats, encoding='utf-8')
