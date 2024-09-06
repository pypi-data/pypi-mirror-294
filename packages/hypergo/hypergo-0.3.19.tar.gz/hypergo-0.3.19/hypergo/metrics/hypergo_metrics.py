import math
import inspect
from threading import Lock
from typing import Any, cast, Dict, Mapping, Set, List, Optional, Union
from collections.abc import Callable, Iterable, Sequence
from opentelemetry.sdk.metrics.export import (
    PeriodicExportingMetricReader,
    MetricExporter,
    ConsoleMetricExporter,
    MetricReader,
    AggregationTemporality,
)
from opentelemetry.sdk.metrics import MeterProvider, Meter, ObservableGauge
from opentelemetry.metrics import CallbackOptions, Observation
from hypergo.utility import DynamicImports
from hypergo.metrics.base_metrics import MetricResult

deltaTemporality = {
    ObservableGauge: AggregationTemporality.CUMULATIVE,
}


class HypergoMetric:

    _default_metric_exporter: MetricExporter = ConsoleMetricExporter(preferred_temporality=deltaTemporality)
    _hypergo_metric_lock: Lock = Lock()
    _is_collected: bool = False

    _current_metric_readers: Set[MetricReader] = set(
        [PeriodicExportingMetricReader(_default_metric_exporter, export_interval_millis=math.inf)]
    )

    # _current_metric_readers should have unique exporters (Azure, Graphana, Datadog etc.).
    # In a multithreaded environment, I don't want to see the same exporter registered since there is a check for that
    # using elements inside OpenTelemetry MeterProvider._all_metric_readers
    _current_metric_exporters_class_names: Set[str] = set([_default_metric_exporter.__class__.__name__])

    _current_meter_provider: Union[MeterProvider, None] = None

    @staticmethod
    def set_metric_exporter(metric_exporter: MetricExporter) -> None:
        if metric_exporter.__class__.__name__ not in HypergoMetric._current_metric_exporters_class_names:
            HypergoMetric._current_metric_readers.add(
                PeriodicExportingMetricReader(metric_exporter, export_interval_millis=math.inf)
            )
            HypergoMetric._current_metric_exporters_class_names.add(metric_exporter.__class__.__name__)

    @staticmethod
    def get_meter(name: str) -> Meter:
        # This function is called (on events) way after registration of all
        # exporters done during initialization
        metric_readers: Set[PeriodicExportingMetricReader] = HypergoMetric._current_metric_readers
        with HypergoMetric._hypergo_metric_lock:
            if not HypergoMetric._current_meter_provider or HypergoMetric._is_collected:
                if HypergoMetric._is_collected:
                    # Do one last collection before new MeterProvider is
                    # instantiated
                    HypergoMetric.collect()
                    HypergoMetric._is_collected = False
                    HypergoMetric._current_meter_provider._all_metric_readers.clear()
                HypergoMetric._current_meter_provider = MeterProvider(
                    metric_readers=cast(Sequence[Any], metric_readers)
                )
            return HypergoMetric._current_meter_provider.get_meter(name=name)

    @staticmethod
    def get_metrics_callback(
        package: str, module_name: str, class_name: str
    ) -> List[Callable[[MetricResult], MetricResult]]:
        callbacks: List[Callable[[MetricResult], MetricResult]] = []
        imported_class = DynamicImports.dynamic_imp_class(
            package=package, module_name=module_name, class_name=class_name
        )
        for _, member in inspect.getmembers(imported_class, predicate=inspect.isfunction):
            callbacks.append(member)
        return callbacks

    @staticmethod
    def send(
        meter: Meter,
        metric_name: str,
        metric_result: Union[MetricResult, Sequence[MetricResult]],
        description: Optional[str] = None,
    ) -> None:
        def create_callback(
            value: Union[float, int], attributes: Dict[str, Union[str, None]]
        ) -> Callable[[CallbackOptions], Iterable[Observation]]:
            def func(options: CallbackOptions) -> Iterable[Observation]:
                yield Observation(value, attributes=cast(Mapping[str, str], attributes))

            return func

        _metric_values: Sequence[MetricResult] = ()
        _callbacks: Set[Callable[[CallbackOptions], Iterable[Observation]]] = set()
        metric_unit: Union[str, None] = None
        function_name: str = meter.name

        _metric_values = metric_result if isinstance(metric_result, Sequence) else tuple([metric_result])
        for _metric_result in _metric_values:
            name, unit, value, timestamp = (
                _metric_result.name,
                _metric_result.unit,
                _metric_result.value,
                _metric_result.timestamp,
            )
            if not metric_unit:
                metric_unit = unit
            elif metric_unit != unit:
                raise ValueError(f"All MetricResult(s) for {metric_name} should have the same unit value")
            _callbacks.add(
                create_callback(
                    value=value,
                    attributes={
                        "unit": unit,
                        "name": name,
                        "timestamp": timestamp,
                        "function_name": function_name,
                        "metric_name": metric_name,
                    },
                )
            )

        meter.create_observable_gauge(
            name=metric_name,
            callbacks=cast(Sequence[Callable[[CallbackOptions], Iterable[Observation]]], _callbacks),
            unit=cast(str, metric_unit),
            description=cast(str, description),
        )

    @staticmethod
    def collect() -> None:
        HypergoMetric._current_meter_provider.force_flush(timeout_millis=60000)
        HypergoMetric._is_collected = True
