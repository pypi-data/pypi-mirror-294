import csv
import logging
import os
import time
from multiprocessing import Process, Queue, Event
from queue import Empty
from typing import Union, Dict, Optional, cast

import pandas as pd
import psutil
from nvitop import Device, ResourceMetricCollector

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class PerformanceLogger:
    """Performance logger class using multiprocessing."""

    def __init__(self, log_dir: str, log_node: str, interval: float = 1.0, debug_mode: bool = False):
        os.makedirs(log_dir, exist_ok=True)

        self.filepath = f"{log_dir}/node-{log_node}.csv"
        self.log_dir = log_dir
        self.log_node = log_node
        self.debug_mode = debug_mode
        self.interval = interval
        self.cpu_count = psutil.cpu_count(logical=False)
        self.stop_event = Event()
        self.metrics_queue = Queue()
        self.tag_queue = Queue()  # New queue for tag changes

        # Start custom processes for collecting and writing metrics
        self.collector_process = Process(target=self._run_collector, args=(
            self.stop_event, self.metrics_queue, self.tag_queue, self.interval))
        self.writer_process = Process(target=self._run_writer,
                                      args=(self.stop_event, self.metrics_queue, self.filepath))
        self.collector_process.start()
        self.writer_process.start()

    def stop(self) -> None:
        """Stop the processes."""
        self.stop_event.set()
        self.collector_process.join()
        self.writer_process.join()
        self.metrics_queue.close()
        self.tag_queue.close()

    def change_tag(self, tag: str) -> None:
        """Changes the tag of the logger."""
        self.tag_queue.put(tag)
        logging.info("Tag change request sent: %s", tag)

    def _run_collector(self, stop_event: Event, metrics_queue: Queue, tag_queue: Queue, interval: float) -> None:
        """Process for collecting metrics."""
        collector = ResourceMetricCollector(Device.cuda.all())
        collector.start(tag="metrics-daemon")
        current_tag: Optional[str] = None

        while not stop_event.is_set():
            # Check for tag updates
            try:
                while True:  # Process all pending tag updates
                    current_tag = tag_queue.get_nowait()
            except Empty:
                pass

            metrics = self._collect_metrics(collector, current_tag)
            metrics_queue.put(metrics)
            time.sleep(interval)

        collector.stop()

    def _run_writer(self, stop_event: Event, metrics_queue: Queue, filepath: str) -> None:
        """Process for writing metrics."""
        first_collect = True
        while not stop_event.is_set():
            try:
                metrics = metrics_queue.get(timeout=1)
                self._write_metrics(metrics, filepath, first_collect)
                if first_collect:
                    first_collect = False
            except Empty:
                continue

    def _get_cpu_usage_per_core(self) -> Dict[str, float]:
        """Returns the CPU usage per core."""
        cpu_percent = psutil.cpu_percent(interval=0.1, percpu=True)
        return {f"cpu_core_{i+1} (%)": percent
                for i, percent in enumerate(cpu_percent)}

    def _get_network_bandwidth(self) -> Dict[str, float]:
        """Returns the network bandwidth."""
        interfaces = psutil.net_io_counters(pernic=True)
        it = {}
        for interface, stats in interfaces.items():
            bytes_sent = stats.bytes_sent
            bytes_recv = stats.bytes_recv
            mbps_sent = bytes_sent * 8 / (1024 * 1024)
            mbps_recv = bytes_recv * 8 / (1024 * 1024)
            it[f"network_{interface}/sent (Mbps)"] = mbps_sent
            it[f"network_{interface}/recv (Mbps)"] = mbps_recv
        return it

    def _clean_column_name(self, col: str) -> str:
        """Cleans the column name."""
        rm_prefix = ["metrics-daemon/host/", "metrics-daemon/"]
        for prefix in rm_prefix:
            if col.startswith(prefix):
                col = col[len(prefix):]
        return col

    def _collect_metrics(self, collector: ResourceMetricCollector, current_tag: Optional[str]) -> Dict[str, Union[float, str, None]]:
        """Collects and processes metrics."""
        # Collect the metrics and cast it to the appropriate type
        raw_metrics = collector.collect()
        metrics = cast(Dict[str, Union[float, str, None]], raw_metrics)

        # Collect CPU and network metrics
        cpu_metrics = self._get_cpu_usage_per_core()
        metrics.update(cpu_metrics)

        network_metrics = self._get_network_bandwidth()
        metrics.update(network_metrics)

        metrics['tag'] = current_tag

        return metrics

    def _write_metrics(self, metrics: Dict[str, Union[float, str, None]], filepath: str, first_collect: bool) -> None:
        """Writes metrics to file if the row is not empty."""
        df_metrics = pd.DataFrame.from_records([metrics])
        df_metrics.columns = [self._clean_column_name(col)
                              for col in df_metrics.columns]

        try:
            if first_collect and not os.path.isfile(filepath):
                df_metrics.to_csv(filepath, index=False)
                logging.info("First collection completed at path %s", filepath)
            else:
                if df_metrics.isnull().all().all():
                    logging.info("Skipping empty row")
                    return

                file_exists = os.path.isfile(filepath)
                with open(filepath, 'a', newline='', encoding='utf-8') as f:
                    writer = csv.DictWriter(f, fieldnames=df_metrics.columns)

                    # Write the header only if the file does not exist or the header is missing
                    if not file_exists or f.tell() == 0:
                        writer.writeheader()

                    writer.writerow(df_metrics.iloc[0].to_dict())

                    if self.debug_mode:
                        logging.info("Data written to %s with duration %s",
                                    filepath, df_metrics.iloc[0].get('duration (s)', 'N/A'))
                    f.flush()
        except (IOError, OSError) as e:
            logging.error("File I/O error writing to %s: %s", filepath, str(e))
        except ValueError as e:
            logging.error("Value error during file write: %s", str(e))
