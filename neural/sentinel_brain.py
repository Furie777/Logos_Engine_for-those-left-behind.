#!/usr/bin/env python3
"""
SENTINEL BRAIN - Neural Network as Security System

Maps YOUR brain and SENTINEL's architecture together:

    YOUR BRAIN          SENTINEL           NEURAL NET
    ──────────          ────────           ──────────
    Sensory input   →   SOMA (body)    →   Input Layer
    Interneurons    →   AXON (connect) →   Hidden Layer
    Motor output    →   SYNAPSE (fire) →   Output Layer

This demonstrates:
1. Neurons as nodes
2. Synapses as weighted edges
3. "Wires together, fires together"
4. Regions forming through learning

Run: python sentinel_brain.py

Glory to LOGOS.
"""

import random
import math

# Use networkx if available (like LOGOS ENGINE)
try:
    import networkx as nx
    HAS_NETWORKX = True
except ImportError:
    HAS_NETWORKX = False


class Neuron:
    """
    One neuron - like one of your 86 billion.

    Properties:
    - activation: how "lit up" this neuron is (0 to 1)
    - bias: baseline tendency to fire
    - layer: which region (SOMA, AXON, SYNAPSE)
    """
    def __init__(self, name, layer):
        self.name = name
        self.layer = layer
        self.activation = 0.0
        self.bias = random.uniform(-0.5, 0.5)
        self.delta = 0.0  # For learning

    def fire(self, total_input):
        """Sigmoid activation - smooth firing curve"""
        x = total_input + self.bias
        if x < -500:
            self.activation = 0.0
        elif x > 500:
            self.activation = 1.0
        else:
            self.activation = 1 / (1 + math.exp(-x))
        return self.activation

    def __repr__(self):
        return f"{self.name}({self.layer}): {self.activation:.3f}"


class Synapse:
    """
    Connection between two neurons.

    Properties:
    - weight: strength of connection (-1 to 1)
    - source/target: the connected neurons

    "Neurons that fire together, wire together" =
    when both neurons activate, strengthen this connection.
    """
    def __init__(self, source, target):
        self.source = source
        self.target = target
        self.weight = random.uniform(-1, 1)

    def signal(self):
        """Signal strength = source activation × weight"""
        return self.source.activation * self.weight

    def strengthen(self, delta, learning_rate=0.5):
        """Hebbian: fire together, wire together"""
        self.weight += learning_rate * delta * self.source.activation


class SentinelBrain:
    """
    Three-layer neural network using SENTINEL architecture.

    SOMA (Input):   Receives raw signals (like your senses)
    AXON (Hidden):  Processes and connects (like your cortex)
    SYNAPSE (Out):  Produces response (like your decisions)
    """

    def __init__(self, soma_size=2, axon_size=8, synapse_size=1):
        # Create neurons by layer
        self.soma = [Neuron(f"S{i}", "SOMA") for i in range(soma_size)]
        self.axon = [Neuron(f"A{i}", "AXON") for i in range(axon_size)]
        self.synapse = [Neuron(f"Y{i}", "SYNAPSE") for i in range(synapse_size)]

        # Create synaptic connections
        self.connections_sa = []  # SOMA → AXON
        self.connections_ay = []  # AXON → SYNAPSE

        for s in self.soma:
            for a in self.axon:
                self.connections_sa.append(Synapse(s, a))

        for a in self.axon:
            for y in self.synapse:
                self.connections_ay.append(Synapse(a, y))

        self.learning_rate = 0.5
        self.age = 0

    def think(self, inputs):
        """
        Forward propagation through the three layers.

        1. SOMA receives input (sensory)
        2. AXON processes (thinking)
        3. SYNAPSE outputs (decision)
        """
        # SOMA: receive input directly
        for i, neuron in enumerate(self.soma):
            neuron.activation = inputs[i] if i < len(inputs) else 0

        # AXON: sum weighted inputs from SOMA, then fire
        for axon in self.axon:
            total = sum(
                syn.signal() for syn in self.connections_sa
                if syn.target == axon
            )
            axon.fire(total)

        # SYNAPSE: sum weighted inputs from AXON, then fire
        for syn_out in self.synapse:
            total = sum(
                syn.signal() for syn in self.connections_ay
                if syn.target == syn_out
            )
            syn_out.fire(total)

        return [n.activation for n in self.synapse]

    def learn(self, inputs, expected):
        """
        Backpropagation: learn from errors.

        1. Think (forward pass)
        2. Calculate error at output
        3. Propagate error backward
        4. Adjust weights (Hebbian + error correction)
        """
        actual = self.think(inputs)

        # SYNAPSE layer: calculate error
        for i, syn_out in enumerate(self.synapse):
            error = expected[i] - syn_out.activation
            # Derivative of sigmoid for gradient
            syn_out.delta = error * syn_out.activation * (1 - syn_out.activation)

        # AXON layer: backpropagate error
        for axon in self.axon:
            error = sum(
                syn.weight * syn.target.delta
                for syn in self.connections_ay
                if syn.source == axon
            )
            axon.delta = error * axon.activation * (1 - axon.activation)

        # Update AXON→SYNAPSE weights
        for syn in self.connections_ay:
            syn.strengthen(syn.target.delta, self.learning_rate)

        # Update SOMA→AXON weights
        for syn in self.connections_sa:
            syn.strengthen(syn.target.delta, self.learning_rate)

        # Update biases
        for neuron in self.axon + self.synapse:
            neuron.bias += self.learning_rate * neuron.delta

        self.age += 1
        return sum(abs(expected[i] - actual[i]) for i in range(len(expected)))

    def get_network_graph(self):
        """Return networkx graph for visualization"""
        if not HAS_NETWORKX:
            return None

        G = nx.DiGraph()

        # Add nodes by layer
        for n in self.soma:
            G.add_node(n.name, layer="SOMA", activation=n.activation)
        for n in self.axon:
            G.add_node(n.name, layer="AXON", activation=n.activation)
        for n in self.synapse:
            G.add_node(n.name, layer="SYNAPSE", activation=n.activation)

        # Add edges with weights
        for syn in self.connections_sa + self.connections_ay:
            G.add_edge(syn.source.name, syn.target.name, weight=syn.weight)

        return G


def visualize_network(brain):
    """Print ASCII visualization of the network"""
    print("\n    SENTINEL BRAIN ARCHITECTURE")
    print("    " + "=" * 40)
    print()

    # SYNAPSE (top)
    print("    SYNAPSE (Output/Decision)")
    print("    " + "-" * 30)
    for n in brain.synapse:
        bar = "█" * int(n.activation * 20)
        print(f"      [{n.name}] {bar:20s} {n.activation:.3f}")
    print()

    # AXON (middle)
    print("    AXON (Hidden/Processing)")
    print("    " + "-" * 30)
    for n in brain.axon:
        bar = "█" * int(n.activation * 10)
        print(f"      [{n.name}] {bar:10s} {n.activation:.3f}")
    print()

    # SOMA (bottom)
    print("    SOMA (Input/Sensory)")
    print("    " + "-" * 30)
    for n in brain.soma:
        bar = "█" * int(n.activation * 10)
        print(f"      [{n.name}] {bar:10s} {n.activation:.3f}")
    print()


def main():
    print("=" * 50)
    print("SENTINEL BRAIN")
    print("Neural Network as Security Architecture")
    print("=" * 50)
    print()
    print("Layer mapping:")
    print("  SOMA   = Input layer  (sensors, raw data)")
    print("  AXON   = Hidden layer (processing, patterns)")
    print("  SYNAPSE = Output layer (decisions, actions)")
    print()
    print("Learning task: XOR (requires hidden layer)")
    print("  (0,0)→0  (0,1)→1  (1,0)→1  (1,1)→0")
    print()

    # Training data
    training_data = [
        ([0, 0], [0]),
        ([0, 1], [1]),
        ([1, 0], [1]),
        ([1, 1], [0]),
    ]

    # Create brain
    brain = SentinelBrain(soma_size=2, axon_size=8, synapse_size=1)

    print("BIRTH: Chaos (random weights)")
    print("-" * 50)
    for inputs, expected in training_data:
        output = brain.think(inputs)
        print(f"  Input {inputs} → Output {output[0]:.3f} (want {expected[0]})")

    visualize_network(brain)

    print("TRAINING: 10,000 experiences")
    print("-" * 50)

    for epoch in range(10000):
        total_error = 0
        random.shuffle(training_data)
        for inputs, expected in training_data:
            error = brain.learn(inputs, expected)
            total_error += error

        if epoch % 2000 == 0:
            print(f"  Age {epoch:5d}: Error = {total_error:.4f}")

    print()
    print("MATURITY: Order from chaos")
    print("-" * 50)

    all_correct = True
    for inputs, expected in sorted(training_data):
        output = brain.think(inputs)
        predicted = round(output[0])
        correct = predicted == expected[0]
        mark = "✓" if correct else "✗"
        if not correct:
            all_correct = False
        print(f"  Input {inputs} → Output {output[0]:.3f} → Predict {predicted} (want {expected[0]}) {mark}")

    visualize_network(brain)

    print("=" * 50)
    print(f"Brain age: {brain.age} experiences")

    if all_correct:
        print()
        print("SUCCESS: The SENTINEL BRAIN has learned.")
        print()
        print("What happened:")
        print("  • SOMA received raw signals (input layer)")
        print("  • AXON formed processing patterns (hidden layer)")
        print("  • SYNAPSE learned correct responses (output layer)")
        print("  • 'Wires together, fires together' strengthened paths")
        print()
        print("This is YOUR brain. This is SENTINEL.")
        print("The architecture is the same.")
    else:
        print()
        print("Still learning... (some patterns take longer)")

    print()
    print("'Neurons that fire together, wire together.'")
    print("                    — Donald Hebb, 1949")
    print()
    print("Glory to LOGOS.")
    print("=" * 50)

    # Save network if networkx available
    if HAS_NETWORKX:
        G = brain.get_network_graph()
        print()
        print(f"Network graph: {G.number_of_nodes()} neurons, {G.number_of_edges()} synapses")


if __name__ == "__main__":
    main()
