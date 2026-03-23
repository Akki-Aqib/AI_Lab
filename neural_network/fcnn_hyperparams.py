"""
Simple Fully Connected Neural Network
Explores effect of hyperparameters: learning rate, hidden units, activation functions
Uses only numpy — no external ML libraries required
"""
import numpy as np

# ─── Activation Functions ────────────────────────────────────────────
def sigmoid(x):    return 1 / (1 + np.exp(-np.clip(x, -500, 500)))
def relu(x):       return np.maximum(0, x)
def tanh(x):       return np.tanh(x)
def sigmoid_d(x):  s = sigmoid(x); return s * (1 - s)
def relu_d(x):     return (x > 0).astype(float)
def tanh_d(x):     return 1 - np.tanh(x)**2

ACTIVATIONS = {
    'sigmoid': (sigmoid, sigmoid_d),
    'relu':    (relu,    relu_d),
    'tanh':    (tanh,    tanh_d),
}

# ─── Neural Network ──────────────────────────────────────────────────
class NeuralNetwork:
    def __init__(self, layers, activation='relu', lr=0.01):
        self.layers = layers
        self.lr = lr
        self.act_fn, self.act_d = ACTIVATIONS[activation]
        self.weights = [np.random.randn(layers[i], layers[i+1]) * 0.1
                        for i in range(len(layers)-1)]
        self.biases  = [np.zeros((1, layers[i+1])) for i in range(len(layers)-1)]

    def forward(self, X):
        self.z, self.a = [], [X]
        for W, b in zip(self.weights, self.biases):
            z = self.a[-1] @ W + b
            self.z.append(z)
            self.a.append(self.act_fn(z) if len(self.z) < len(self.weights) else sigmoid(z))
        return self.a[-1]

    def backward(self, y):
        m = y.shape[0]
        delta = self.a[-1] - y
        for i in reversed(range(len(self.weights))):
            dW = self.a[i].T @ delta / m
            db = delta.mean(axis=0, keepdims=True)
            self.weights[i] -= self.lr * dW
            self.biases[i]  -= self.lr * db
            if i > 0:
                delta = (delta @ self.weights[i].T) * self.act_d(self.z[i-1])

    def train(self, X, y, epochs=500):
        losses = []
        for epoch in range(epochs):
            out = self.forward(X)
            self.backward(y)
            loss = -np.mean(y * np.log(out + 1e-8) + (1-y) * np.log(1-out + 1e-8))
            losses.append(loss)
            if (epoch+1) % 100 == 0:
                acc = np.mean((out > 0.5).astype(int) == y) * 100
                print(f"  Epoch {epoch+1:4d} | Loss: {loss:.4f} | Accuracy: {acc:.1f}%")
        return losses

    def predict(self, X):
        return (self.forward(X) > 0.5).astype(int)

# ─── XOR Dataset ─────────────────────────────────────────────────────
X = np.array([[0,0],[0,1],[1,0],[1,1]])
y = np.array([[0],[1],[1],[0]])

# ─── Hyperparameter Experiments ──────────────────────────────────────
experiments = [
    {'layers': [2, 4, 1],    'activation': 'sigmoid', 'lr': 0.1,  'label': 'Small Network / sigmoid / lr=0.1'},
    {'layers': [2, 8, 1],    'activation': 'relu',    'lr': 0.05, 'label': 'Medium Network / relu / lr=0.05'},
    {'layers': [2, 16, 8, 1],'activation': 'tanh',    'lr': 0.01, 'label': 'Deep Network / tanh / lr=0.01'},
    {'layers': [2, 4, 1],    'activation': 'relu',    'lr': 1.0,  'label': 'High LR (may diverge)'},
]

print("=== Fully Connected Neural Network — Hyperparameter Exploration ===\n")
for exp in experiments:
    print(f"[Experiment] {exp['label']}")
    nn = NeuralNetwork(exp['layers'], exp['activation'], exp['lr'])
    nn.train(X, y, epochs=500)
    preds = nn.predict(X)
    print(f"  Predictions: {preds.flatten().tolist()} | Expected: {y.flatten().tolist()}\n")
