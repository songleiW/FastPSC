Here’s the English version of the README for your FastPSC project, tailored for a research prototype submission like VLDB. You can adapt the technical parts if the actual command-line arguments or implementation details differ.

---

# 🚀 FastPSC

**FastPSC** is a protocol for **fast and maliciously secure computation of intersection and union over multi-owner sets**. This implementation accompanies the paper:

> **FastPSC: Fast and Maliciously Secure Computation of Intersection and Union on Multi-Owner Sets**
> *(Submitted to VLDB 2025)*

## 📁 Project Structure

```
FastPSC/
├── src/                 # Core protocol implementation
├── examples/            # Sample inputs and run scripts
├── scripts/             # Utility scripts for setup, testing, benchmarking
├── README.md            # This documentation
└── requirements.txt     # Python dependencies (if applicable)
```

## ⚙️ Requirements

* For C++ implementation:

  * `CMake >= 3.10`, `g++` or `clang++`
* For Python implementation:

  * `Python >= 3.8`
* Cryptographic library (e.g., libsodium, OpenSSL)
* Networking support (TCP or gRPC depending on implementation)

## 🔧 Installation & Build

Clone the repository and build the project:

```bash
git clone https://github.com/songleiW/FastPSC.git
cd FastPSC

# For C++ build
mkdir build && cd build
cmake ..
make -j4

# For Python
pip install -r requirements.txt
```

## ▶️ Running the Protocol

You can run the intersection or union protocol among multiple parties (e.g., 3):

### Example: C++ Interface

```bash
# Run Party 1
./build/fastpsc_client --party 1 --mode intersection --input ../examples/data1.txt --host localhost --port 9001 &

# Run Party 2
./build/fastpsc_client --party 2 --mode intersection --input ../examples/data2.txt --host localhost --port 9002 &

# Run Party 3
./build/fastpsc_client --party 3 --mode intersection --input ../examples/data3.txt --host localhost --port 9003
```

To compute the union, just change `--mode intersection` to `--mode union`.

### Example: Python Interface

```bash
# Run all parties (example for 2-party)
python3 src/fastpsc.py --party 1 --mode intersection --input examples/data1.txt --port 9001 &
python3 src/fastpsc.py --party 2 --mode intersection --input examples/data2.txt --port 9002
```

## 🔍 Command-Line Arguments

| Argument            | Description                               |
| ------------------- | ----------------------------------------- |
| `--party`           | Party ID (e.g., 1, 2, 3)                  |
| `--mode`            | `intersection` or `union`                 |
| `--input`           | Input file path (one item per line)       |
| `--host` / `--port` | Communication address for local party     |
| `--config`          | (Optional) JSON config for advanced setup |

## 📄 Input Format

Each party provides a file with one item per line:

**examples/data1.txt**

```
alice@example.com
bob@example.com
carol@example.com
```

All input elements are treated as strings; they are internally hashed and processed securely.

## 📊 Benchmarking

You can benchmark the performance with the provided script:

```bash
bash scripts/benchmark.sh --parties 3 --elem_count 100000 --mode union
```

Sample output:

```
[Benchmark] 3 parties, 100K elements each
Union: 1.2s, 2 rounds, 50MB total communication
Intersection: 0.9s, 1 round, 30MB total communication
```


## ❓ FAQ

* **Q: How many parties are supported?**
  A: Arbitrary number of parties (2 or more), depending on network and system setup.

* **Q: What happens if a party crashes?**
  A: Currently, the protocol requires synchronous and reliable channels. Crash recovery is not supported.

* **Q: Can I plug in a different communication backend?**
  A: Yes. See `src/comm/` for socket/gRPC-based communication modules.

---
