#!/usr/bin/env python3
"""
BABY BRAIN - A Neural Network That Learns

This mirrors YOUR brain's journey:
- Starts with random connections (newborn chaos)
- Learns through experience (wires together, fires together)
- Forms patterns (regions emerge)
- Makes predictions (autonomous operation)

Run: python baby_brain.py

Glory to LOGOS.
"""

import random
import math

# ═══════════════════════════════════════════════════════════════
# THE NEURON - Like one of your 86 billion brain cells
# ═══════════════════════════════════════════════════════════════

def sigmoid(x):
    """Smooth activation function - neuron firing rate"""
    if x < -500:
        return 0
    if x > 500:
        return 1
    return 1 / (1 + math.exp(-x))

def sigmoid_derivative(x):
    """How much the neuron's firing changes - for learning"""
    return x * (1 - x)


# ═══════════════════════════════════════════════════════════════
# THE BABY BRAIN - 3 layers, like brain regions
# ═══════════════════════════════════════════════════════════════

class BabyBrain:
    """
    Input layer  →  Hidden layer  →  Output layer
    (senses)        (processing)     (decision)

    Just like: Eyes → Visual cortex → Recognition
    """

    def __init__(self, input_size, hidden_size, output_size):
        # Random weights at birth - CHAOS, no regions yet
        # Xavier initialization - better starting point
        scale_ih = math.sqrt(2.0 / input_size)
        scale_ho = math.sqrt(2.0 / hidden_size)

        self.weights_ih = [
            [random.gauss(0, scale_ih) for _ in range(input_size + 1)]  # +1 for bias
            for _ in range(hidden_size)
        ]
        self.weights_ho = [
            [random.gauss(0, scale_ho) for _ in range(hidden_size + 1)]  # +1 for bias
            for _ in range(output_size)
        ]

        self.learning_rate = 0.5
        self.age = 0

    def think(self, inputs):
        """
        Forward propagation - signal flows through the network.
        Like when you see something: light → retina → brain → recognition
        """
        # Add bias (always-on neuron, like baseline brain activity)
        inputs_with_bias = list(inputs) + [1]

        # Hidden layer processes inputs
        self.hidden = []
        for weights in self.weights_ih:
            total = sum(i * w for i, w in zip(inputs_with_bias, weights))
            self.hidden.append(sigmoid(total))

        # Add bias for output layer
        hidden_with_bias = self.hidden + [1]

        # Output layer makes decision
        self.output = []
        for weights in self.weights_ho:
            total = sum(h * w for h, w in zip(hidden_with_bias, weights))
            self.output.append(sigmoid(total))

        self.last_input = inputs_with_bias
        return self.output

    def learn(self, inputs, expected):
        """
        HEBBIAN LEARNING + BACKPROPAGATION

        "Neurons that fire together, wire together"
        But also: learn from mistakes (error correction)
        """
        actual = self.think(inputs)

        # Output layer error
        output_errors = []
        output_deltas = []
        for i in range(len(expected)):
            error = expected[i] - actual[i]
            delta = error * sigmoid_derivative(actual[i])
            output_errors.append(error)
            output_deltas.append(delta)

        # Hidden layer error (backpropagated)
        hidden_deltas = []
        for i in range(len(self.hidden)):
            error = sum(
                output_deltas[j] * self.weights_ho[j][i]
                for j in range(len(output_deltas))
            )
            delta = error * sigmoid_derivative(self.hidden[i])
            hidden_deltas.append(delta)

        # Update output weights
        hidden_with_bias = self.hidden + [1]
        for i in range(len(self.weights_ho)):
            for j in range(len(self.weights_ho[i])):
                self.weights_ho[i][j] += self.learning_rate * output_deltas[i] * hidden_with_bias[j]

        # Update hidden weights
        for i in range(len(self.weights_ih)):
            for j in range(len(self.weights_ih[i])):
                self.weights_ih[i][j] += self.learning_rate * hidden_deltas[i] * self.last_input[j]

        self.age += 1
        return sum(abs(e) for e in output_errors)


def main():
    print("=" * 50)
    print("BABY BRAIN - Learning XOR")
    print("=" * 50)
    print()
    print("XOR: A pattern that requires REGIONS to learn")
    print("  (0,0)→0  Same     → False")
    print("  (0,1)→1  Different → True")
    print("  (1,0)→1  Different → True")
    print("  (1,1)→0  Same     → False")
    print()
    print("Single neurons CAN'T learn this.")
    print("You need a hidden layer (brain region).")
    print()

    training_data = [
        ([0, 0], [0]),
        ([0, 1], [1]),
        ([1, 0], [1]),
        ([1, 1], [0]),
    ]

    # Create brain: 2 inputs, 8 hidden neurons, 1 output
    brain = BabyBrain(input_size=2, hidden_size=8, output_size=1)

    print("BIRTH: Random weights (chaos)")
    print("-" * 50)
    for inputs, expected in training_data:
        output = brain.think(inputs)
        print(f"  {inputs} → {output[0]:.3f} (expected {expected[0]})")

    print()
    print("LEARNING: 5000 experiences...")
    print("-" * 50)

    for epoch in range(5000):
        total_error = 0
        random.shuffle(training_data)  # Like varied experience
        for inputs, expected in training_data:
            error = brain.learn(inputs, expected)
            total_error += error

        if epoch % 1000 == 0:
            print(f"  Age {epoch:4d}: Error = {total_error:.4f}")

    print()
    print("MATURITY: Patterns learned")
    print("-" * 50)

    all_correct = True
    for inputs, expected in sorted(training_data):
        output = brain.think(inputs)
        correct = abs(output[0] - expected[0]) < 0.5
        mark = "✓" if correct else "✗"
        if not correct:
            all_correct = False
        print(f"  {inputs} → {output[0]:.3f} (expected {expected[0]}) {mark}")

    print()
    print("=" * 50)
    print(f"Brain age: {brain.age} experiences")

    if all_correct:
        print("SUCCESS: Order emerged from chaos!")
        print()
        print("What happened:")
        print("  • Weights started random (newborn)")
        print("  • Errors flowed backward (learning)")
        print("  • Connections strengthened (Hebbian)")
        print("  • Hidden layer formed 'concepts'")
        print("  • Output now predicts correctly")
    else:
        print("Still learning... (some brains take longer)")

    print()
    print("'Neurons that fire together, wire together.'")
    print()
    print("Glory to LOGOS.")
    print("=" * 50)


if __name__ == "__main__":
    main()
