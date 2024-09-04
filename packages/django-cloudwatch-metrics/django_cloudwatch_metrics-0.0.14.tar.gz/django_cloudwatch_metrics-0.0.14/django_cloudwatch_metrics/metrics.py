import base64
import hashlib
import logging
from datetime import datetime
from typing import Optional

import pytz
from django.db.models import F
from django.db.transaction import atomic
from django.conf import settings

from django_cloudwatch_metrics.hashing import create_cache_key
from django_cloudwatch_metrics.models import MetricAggregation


@atomic
def increment(metric_name: str, value: int, **kwargs):
    """Publishes a metric increment."""
    datetime_period = datetime.now(pytz.utc).replace(second=0, microsecond=0)

    if settings and hasattr(settings, "DJANGO_CLOUDWATCH_ACCURACY_MINUTES"):
        accuracy_in_minutes = settings.DJANGO_CLOUDWATCH_ACCURACY_MINUTES

        # Round datetime_period to the accuracy_in_minutes
        datetime_period = datetime_period.replace(minute=(datetime_period.minute // accuracy_in_minutes) * accuracy_in_minutes)

    if settings and hasattr(settings, "DJANGO_CLOUDWATCH_METRICS") and not settings.DJANGO_CLOUDWATCH_METRICS:
        return

    # Convert all kwargs to strings
    kwargs = {k.encode("ascii", "ignore").decode(): str(v).encode("ascii", "ignore").decode() for k, v in kwargs.items()}

    aggregation_key = create_cache_key(
        metric_name,
        datetime_period,
        kwargs,
    )

    try:
        metric_aggregation, created = MetricAggregation.objects.select_for_update().get_or_create(
            aggregation_key=aggregation_key,
            defaults={
                "datetime_period":  datetime_period,
                "metric_name": metric_name.encode("ascii", "ignore").decode(),
                "dimension_data": kwargs,
                "value": value,
            }
        )
    except Exception as e:
        logging.warning(e)
        metric_aggregation = MetricAggregation.objects.select_for_update().filter(aggregation_key=aggregation_key).first()
        created = False

    if not created and metric_aggregation is not None:
        metric_aggregation.value = F("value") + value
        metric_aggregation.save(update_fields=["value"])
