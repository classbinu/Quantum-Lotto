import streamlit as st
from qiskit import QuantumCircuit, Aer, execute


MAX_LOTTO_NUMBER = 45
LOTTO_NUMBERS_COUNT = 6


def run_quantum_circuit(num_qubits):
    qc = QuantumCircuit(num_qubits, num_qubits)
    qc.h(range(num_qubits))
    qc.measure(range(num_qubits), range(num_qubits))
    backend = Aer.get_backend("qasm_simulator")
    job = execute(qc, backend, shots=1)
    result = job.result()
    counts = result.get_counts()
    outcome = list(counts.keys())[0]
    return int(outcome, 2)


def quantum_random_number_generator(max_number):
    num_qubits = max_number.bit_length()
    while True:
        random_number = run_quantum_circuit(num_qubits)
        if 1 <= random_number <= max_number:
            return random_number


def generate_lotto_numbers():
    lotto_numbers = set()
    while len(lotto_numbers) < LOTTO_NUMBERS_COUNT:
        number = quantum_random_number_generator(MAX_LOTTO_NUMBER)
        lotto_numbers.add(number)
    return sorted(lotto_numbers)


def display_lotto_numbers(numbers):
    ball_style = (
        "display: inline-block; "
        "width: 80px; "
        "height: 80px; "
        "background-color: #4fc3f7; "
        "color: white; "
        "border-radius: 50%; "
        "text-align: center; "
        "line-height: 80px; "
        "font-size: 32px; "
        "margin: 5px;"
    )
    balls_html = "".join(
        f"<span style='{ball_style}'>{num}</span>" for _, num in enumerate(numbers)
    )

    div_style = "text-align: center; margin: 80px 0px;"

    st.markdown(
        f"<div style='{div_style}'>{balls_html}</div>",
        unsafe_allow_html=True,
    )


st.title("Quantum Lotto Number Generator")
st.write("This program generates lotto numbers quantum-mechanically.")


if st.button("Generate Lotto Numbers"):
    lotto_numbers = generate_lotto_numbers()
    display_lotto_numbers(lotto_numbers)

with st.expander("View Code"):
    code = """
    MAX_LOTTO_NUMBER = 45
    LOTTO_NUMBERS_COUNT = 6

    def run_quantum_circuit(num_qubits):
        qc = QuantumCircuit(num_qubits, num_qubits)
        qc.h(range(num_qubits))
        qc.measure(range(num_qubits), range(num_qubits))
        backend = Aer.get_backend("qasm_simulator")
        job = execute(qc, backend, shots=1)
        result = job.result()
        counts = result.get_counts()
        outcome = list(counts.keys())[0]
        return int(outcome, 2)


    def quantum_random_number_generator(max_number):
        num_qubits = max_number.bit_length()
        while True:
            random_number = run_quantum_circuit(num_qubits)
            if 1 <= random_number <= max_number:
                return random_number


    def generate_lotto_numbers():
        lotto_numbers = set()
        while len(lotto_numbers) < LOTTO_NUMBERS_COUNT:
            number = quantum_random_number_generator(MAX_LOTTO_NUMBER)
            lotto_numbers.add(number)
        return sorted(lotto_numbers)
    """
    st.code(code, language="python")
