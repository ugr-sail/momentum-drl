import torch
import torch.nn as nn
import torch.nn.functional as F

class QNetwork(nn.Module):
    """Red Q: asigna a cada estado los valores de las acciones."""

    def __init__(self, state_size, action_size, seed, fc1_units=64, fc2_units=64):
        """Inicializa los parámetros y construye el modelo.
        Parámetros
        ==========
            state_size (int): dimensión de cada estado
            action_size (int): dimensión de cada acción
            seed (int): semilla aleatoria
            fc1_units (int): número de nodos de la primera capa oculta
            fc2_units (int): número de nodos de la segunda capa oculta
        """
        super(QNetwork, self).__init__()
        torch.manual_seed(seed)
        self.fc1 = nn.Linear(state_size, fc1_units)
        self.fc2 = nn.Linear(fc1_units, fc2_units)
        self.fc3 = nn.Linear(fc2_units, action_size)

    def forward(self, state):
        """Construye una red que asigna estado -> valores de las acciones."""
        x = F.relu(self.fc1(state))
        x = F.relu(self.fc2(x))
        return self.fc3(x)
