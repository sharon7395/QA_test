# Ammeter Emulators & QA Testing Framework

This project provides emulators for multiple ammeter types and extends them into a configurable QA testing framework for embedded systems current measurement validation.

The framework demonstrates:
- Socket-based communication
- Multi-threaded emulators
- Statistical analysis
- Logging
- Result persistence
- Configuration-driven testing
- Error handling

---

# Project Structure

```text
Ammeters/
├── base_ammeter.py
├── Greenlee_Ammeter.py
├── Entes_Ammeter.py
├── Circutor_Ammeter.py
├── client.py

config/
├── config.yaml

src/
├── testing/
│   └── test_framework.py
│
├── utils/
│   ├── config.py
│   ├── logger.py
│   └── Utils.py

main.py
run_tests.py
requirements.txt
README.md
```

---

# Ammeter Types

## Greenlee Ammeter

- **Port:** 5001
- **Command:** `MEASURE_GREENLEE -get_measurement`
- **Measurement Method:** Ohm's Law

Formula:

```text
I = V / R
```

The emulator generates:
- Random voltage (1V – 10V)
- Random resistance (0.1Ω – 100Ω)

and calculates the current.

---

## ENTES Ammeter

- **Port:** 5002
- **Command:** `MEASURE_ENTES -get_data`
- **Measurement Method:** Hall Effect

Formula:

```text
I = B * K
```

The emulator generates:
- Random magnetic field
- Random calibration factor

and calculates the current.

---

## CIRCUTOR Ammeter

- **Port:** 5003
- **Command:** `MEASURE_CIRCUTOR -get_measurement`
- **Measurement Method:** Rogowski Coil Integration

Formula:

```text
I = ∫V dt
```

The emulator:
- Generates voltage samples
- Uses a random time step
- Integrates the values to calculate current

---

# Implemented QA Framework

This solution extends the provided ammeter emulator infrastructure into a reusable QA automation framework.

## Main Features

- Starts multiple ammeter emulators using socket servers and threads
- Uses a unified client API to request measurements
- Supports Greenlee, ENTES, and CIRCUTOR ammeters
- Performs configurable sampling using `config/config.yaml`
- Calculates statistical metrics:
  - Mean
  - Median
  - Standard deviation
  - Minimum
  - Maximum
- Stores results as JSON files under `results/`
- Writes execution logs under `results/logs/`
- Compares ammeters by standard deviation to identify the most stable device
- Validates configuration structure before running tests
- Handles communication and sampling errors gracefully

---

# Statistical Analysis

The framework calculates:

- Mean current
- Median current
- Standard deviation
- Minimum value
- Maximum value

The framework also identifies the most stable ammeter based on the lowest standard deviation.

---

# Configuration-Driven Testing

All framework behavior is configured using:

```text
config/config.yaml
```

The configuration controls:
- Number of measurements
- Sampling frequency
- Test duration
- Ports
- Commands
- Output directories

This allows modifying test behavior without changing source code.

---

# How to Run

## 1. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 2. Start the Ammeter Emulators

```bash
python main.py
```

This starts:
- Greenlee emulator
- ENTES emulator
- CIRCUTOR emulator

Each emulator runs in a separate daemon thread.

---

## 3. Run the QA Testing Framework

Open a second terminal and run:

```bash
python run_tests.py
```

The framework will:
- Connect to all ammeters
- Collect measurement samples
- Calculate statistics
- Save test results
- Generate execution logs
- Compare device stability

---

# Result Management

Test results are automatically stored as JSON files under:

```text
results/
```

Execution logs are stored under:

```text
results/logs/
```

Each test run receives a unique timestamp-based test ID.

---

# Design Decisions

- The emulator layer was separated from the testing framework layer.
- Configuration-driven testing was implemented using YAML.
- JSON result persistence was added for traceability and future comparison.
- Logging was added for debugging and execution tracking.
- Socket reuse was enabled to support repeated executions without port conflicts.
- Ports were updated to 5001–5003 because port 5000 was occupied by a macOS system service.
- The framework continues sampling even if a single measurement fails.

---

# Fixes Made

The original project contained several issues that were fixed during implementation:

- Fixed socket binding issues using `SO_REUSEADDR`
- Fixed inconsistent ammeter commands
- Fixed broken communication flow in `main.py`
- Added invalid command handling
- Added timeout handling
- Added response validation
- Implemented missing QA framework logic
- Added structured logging
- Added statistical analysis
- Added configurable sampling
- Added result persistence

---

# Dependencies

The project uses the following external dependency:

- PyYAML

Install dependencies using:

```bash
pip install -r requirements.txt
```

---

# Sample Output

```text
Testing greenlee ammeter...

Results for greenlee:
Mean: 0.649
Median: 0.135
Std Dev: 1.119
Min: 0.084
Max: 3.403

Most stable ammeter: circutor
Lowest standard deviation: 0.014
```

---

# Future Improvements

Possible future extensions:

- Visualization graphs using matplotlib
- Retry mechanism for failed measurements
- Advanced performance analysis
- Automated unit tests using pytest
- Error simulation scenarios
- Historical result comparison dashboard

---

# Technical Notes

- Developed and tested using Python 3.9
- Cross-platform compatible
- Uses minimal external dependencies
- Built primarily using Python standard library