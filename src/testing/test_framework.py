import os
import json
import time
import statistics
from datetime import datetime
from typing import Dict, List

from ..utils.config import load_config
from ..utils.logger import TestLogger
from Ammeters.client import request_current_from_ammeter


class AmmeterTestFramework:
    def __init__(self, config_path: str = "config/config.yaml"):
        self.config = load_config(config_path)
        self._validate_config()

    def run_test(self, ammeter_type: str) -> Dict:
        """
           Run a configurable sampling test for a specific ammeter type.
           Collect measurements, calculate statistics,
           save results, and return a structured result object.
        """

        logger = TestLogger(ammeter_type)

        logger.info(f"Starting test for ammeter type: {ammeter_type}")

        if ammeter_type not in self.config["ammeters"]:
            raise ValueError(f"Unknown ammeter type: {ammeter_type}")

        ammeter_config = self.config["ammeters"][ammeter_type]
        port = ammeter_config["port"]
        command = ammeter_config["command"].encode("utf-8")

        sampling_config = self.config["testing"]["sampling"]

        measurements_count = sampling_config["measurements_count"]
        total_duration_seconds = sampling_config["total_duration_seconds"]
        sampling_frequency_hz = sampling_config["sampling_frequency_hz"]

        if measurements_count <= 0:
            raise ValueError("measurements_count must be greater than 0")

        if total_duration_seconds <= 0:
            raise ValueError("total_duration_seconds must be greater than 0")

        if sampling_frequency_hz <= 0:
            raise ValueError("sampling_frequency_hz must be greater than 0")

        expected_duration = measurements_count / sampling_frequency_hz

        if abs(expected_duration - total_duration_seconds) > 0.5:
            logger.warning(
                f"Sampling configuration mismatch: "
                f"measurements_count / sampling_frequency_hz = {expected_duration}, "
                f"but total_duration_seconds = {total_duration_seconds}"
            )

        interval_seconds = 1 / sampling_frequency_hz

        started_at = datetime.now()
        measurements = []

        # Collect measurements according to the configured sampling frequency
        for sample_index in range(measurements_count):
            try:
                logger.info(f"Collecting sample {sample_index + 1}/{measurements_count}")

                current = request_current_from_ammeter(port, command)
                measurements.append(current)

                logger.info(f"Sample {sample_index + 1}: {current} A")

                if sample_index < measurements_count - 1:
                    time.sleep(interval_seconds)

            # Continue sampling even if a single measurement fails
            except Exception as e:
                logger.error(f"Failed to collect sample {sample_index + 1}: {e}")

        if not measurements:
            raise RuntimeError(f"No valid measurements collected for {ammeter_type}")

        # Calculate statistical metrics for the collected measurements
        stats = self._calculate_statistics(measurements)
        finished_at = datetime.now()

        result = {
            "test_id": self._generate_test_id(ammeter_type),
            "ammeter_type": ammeter_type,
            "port": port,
            "command": ammeter_config["command"],

            "configured_measurements_count": measurements_count,
            "actual_measurements_count": len(measurements),

            "configured_total_duration_seconds": total_duration_seconds,
            "sampling_frequency_hz": sampling_frequency_hz,

            "started_at": started_at.isoformat(),
            "finished_at": finished_at.isoformat(),
            "actual_duration_seconds": (finished_at - started_at).total_seconds(),

            "measurements": measurements,
            "statistics": stats
        }

        self._save_result(result)

        logger.info(f"Finished test for {ammeter_type}")
        logger.info(f"Statistics: {stats}")

        return result

    def _calculate_statistics(self, measurements: List[float]) -> Dict:
        """
        Calculate statistical metrics for collected measurements.
        """

        if len(measurements) == 1:
            standard_deviation = 0.0
        else:
            standard_deviation = statistics.stdev(measurements)

        return {
            "mean": statistics.mean(measurements),
            "median": statistics.median(measurements),
            "standard_deviation": standard_deviation,
            "min": min(measurements),
            "max": max(measurements)
        }

    def _save_result(self, result: Dict) -> None:
        """
        Save test result as JSON file.
        """

        output_dir = self.config.get("result_management", {}).get("output_dir", "results")
        os.makedirs(output_dir, exist_ok=True)

        file_name = f"{result['test_id']}.json"
        file_path = os.path.join(output_dir, file_name)

        with open(file_path, "w") as f:
            json.dump(result, f, indent=4)

    def _generate_test_id(self, ammeter_type: str) -> str:
        """
        Generate unique test id based on ammeter type and timestamp.
        """

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{timestamp}_{ammeter_type}"

    def _validate_config(self) -> None:
        required_sections = ["testing", "ammeters", "result_management"]

        for section in required_sections:
            if section not in self.config:
                raise ValueError(f"Missing required config section: {section}")

        if "sampling" not in self.config["testing"]:
            raise ValueError("Missing required config section: testing.sampling")

        sampling = self.config["testing"]["sampling"]

        required_sampling_keys = [
            "measurements_count",
            "total_duration_seconds",
            "sampling_frequency_hz"
        ]

        for key in required_sampling_keys:
            if key not in sampling:
                raise ValueError(f"Missing required sampling config key: {key}")

        required_ammeters = ["greenlee", "entes", "circutor"]

        for ammeter in required_ammeters:
            if ammeter not in self.config["ammeters"]:
                raise ValueError(f"Missing ammeter config: {ammeter}")

            if "port" not in self.config["ammeters"][ammeter]:
                raise ValueError(f"Missing port for ammeter: {ammeter}")

            if "command" not in self.config["ammeters"][ammeter]:
                raise ValueError(f"Missing command for ammeter: {ammeter}")