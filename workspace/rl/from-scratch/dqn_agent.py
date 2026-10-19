import numpy as np
import random
from collections import namedtuple, deque

from model import QNetwork

import torch
import torch.nn.functional as F
import torch.optim as optim

BUFFER_SIZE = int(1e5)  # tamaño de la memoria de experiencias (tamaño D)
BATCH_SIZE = 64         # tamaño del minilote (n_batch)
GAMMA = 0.99            # factor de descuento (gamma)
TAU = 2e-2              # para la actualización suave de los parámetros objetivo (tau)
LR = 5e-4               # tasa de aprendizaje (eta)
UPDATE_EVERY = 4        # cada cuántos pasos se actualiza la red objetivo (C)

class Agent():
    """Interactúa con el entorno y aprende de él."""

    def __init__(self, state_size, action_size, seed):
        """Inicializa un objeto Agent.
        
        Parámetros
        ==========
            state_size (int): dimensión de cada estado
            action_size (int): dimensión de cada acción
            seed (int): semilla aleatoria
        """
        self.state_size = state_size
        self.action_size = action_size
        random.seed(seed)

        # Red Q
        self.qnetwork_local = QNetwork(state_size, action_size, seed)
        self.qnetwork_target = QNetwork(state_size, action_size, seed)
        self.optimizer = optim.Adam(self.qnetwork_local.parameters(), lr=LR)

        # Memoria de experiencias
        self.memory = ReplayBuffer(action_size, BUFFER_SIZE, BATCH_SIZE, seed)
        # Inicializar el contador de pasos (para actualizar cada UPDATE_EVERY pasos)
        self.t_step = 0
    
    def act(self, state, eps=0.):
        """Devuelve la acción para el estado dado según la política actual.
        
        Parámetros
        ==========
            state (array_like): estado actual
            eps (float): epsilon, para la selección de acciones ε-greedy
        """
        state = torch.from_numpy(state).float().unsqueeze(0)
        self.qnetwork_local.eval()
        with torch.no_grad():
            action_values = self.qnetwork_local(state)
        self.qnetwork_local.train()

        # Selección de acciones ε-greedy
        if random.random() > eps:
            return np.argmax(action_values.data.numpy())
        else:
            return random.choice(np.arange(self.action_size))
        
    def step(self, state, action, reward, next_state, done):
        """Almacena una experiencia, aprende de un minilote y, cada UPDATE_EVERY pasos, actualiza la red objetivo.

        Parámetros
        ==========
            state (array_like): estado actual (St)
            action (int): acción tomada (At)
            reward (float): recompensa obtenida (Rt+1)
            next_state (array_like): siguiente estado (St+1)
            done (bool): si St+1 es terminal (no se hace bootstrapping desde él)
        """
        # ------------------- Almacenar la experiencia en la memoria ------------------------ #
        self.memory.add(state, action, reward, next_state, done)

        # ------------------- Entrenar con un minilote de experiencias ---------------------- #
        if len(self.memory) > BATCH_SIZE:
            # Si hay suficientes muestras en la memoria, obtener un subconjunto aleatorio y aprender
            experiences = self.memory.sample()
            self.learn(experiences, GAMMA)

        # ------------------- Actualizar la red objetivo ------------------------------------ #
        self.t_step = (self.t_step + 1) % UPDATE_EVERY
        if self.t_step == 0:
            # Si se han alcanzado C (UPDATE_EVERY) pasos, mezclar los pesos en la red objetivo
            self.soft_update(self.qnetwork_local, self.qnetwork_target, TAU)

    def learn(self, experiences, gamma):
        """Actualiza los parámetros de valor con el lote de tuplas de experiencia dado.

        Parámetros
        ==========
            experiences (Tuple[torch.Tensor]): tupla de tuplas (s, a, r, s', done) 
            gamma (float): factor de descuento
        """
        states, actions, rewards, next_states, dones = experiences

        # Obtener los valores Q máximos predichos (para los siguientes estados) con el modelo objetivo
        # - qnetwork_target : aplicar el paso hacia delante a todo el minilote
        # - detach : no retropropagar
        # - max : obtener la acción que maximiza cada muestra del minilote (dim=1)
        # - [0].unsqueeze(1) : transformar la salida en un vector plano
        Q_target_max = self.qnetwork_target(next_states).detach().max(1)[0].unsqueeze(1)

        # Calcular los valores de referencia y para los estados actuales
        # - dones : detectar si el episodio ha terminado
        y = rewards + (gamma * Q_target_max * (1 - dones))

        # Obtener los valores Q de la acción tomada con el modelo local (Q(Sj, Aj, w))
        # - gather : para cada muestra, seleccionar solo el valor de salida de la acción Aj
        Q_local = self.qnetwork_local(states).gather(1, actions)

        # Optimizar (yj-Q(Sj, Aj, w))^2
        # * Calcular la pérdida
        loss = F.mse_loss(Q_local, y)
        # * Minimizar la pérdida
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

    def soft_update(self, local_model, target_model, tau):
        """Actualización suave de los parámetros del modelo.
        θ_target = τ*θ_local + (1 - τ)*θ_target

        Parámetros
        ==========
            local_model (PyTorch model): modelo del que se copiarán los pesos
            target_model (PyTorch model): modelo al que se copiarán los pesos
            tau (float): parámetro de interpolación 
        """
        for target_param, local_param in zip(target_model.parameters(), local_model.parameters()):
            target_param.data.copy_(tau*local_param.data + (1.0-tau)*target_param.data)


class ReplayBuffer:
    """Memoria de tamaño fijo para almacenar tuplas de experiencia."""

    def __init__(self, action_size, buffer_size, batch_size, seed):
        """Inicializa un objeto ReplayBuffer.

        Parámetros
        ==========
            action_size (int): dimensión de cada acción
            buffer_size (int): tamaño máximo de la memoria
            batch_size (int): tamaño de cada lote de entrenamiento
            seed (int): semilla aleatoria
        """
        self.action_size = action_size
        self.memory = deque(maxlen=buffer_size)  
        self.batch_size = batch_size
        self.experience = namedtuple("Experience", field_names=["state", "action", "reward", "next_state", "done"])
        random.seed(seed)
    
    def add(self, state, action, reward, next_state, done):
        """Añade una nueva experiencia a la memoria."""
        e = self.experience(state, action, reward, next_state, done)
        self.memory.append(e)
    
    def sample(self):
        """Muestrea aleatoriamente un lote de experiencias de la memoria."""
        experiences = random.sample(self.memory, k=self.batch_size)

        states = torch.from_numpy(np.vstack([e.state for e in experiences if e is not None])).float()
        actions = torch.from_numpy(np.vstack([e.action for e in experiences if e is not None])).long()
        rewards = torch.from_numpy(np.vstack([e.reward for e in experiences if e is not None])).float()
        next_states = torch.from_numpy(np.vstack([e.next_state for e in experiences if e is not None])).float()
        dones = torch.from_numpy(np.vstack([e.done for e in experiences if e is not None]).astype(np.uint8)).float()
  
        return (states, actions, rewards, next_states, dones)

    def __len__(self):
        """Devuelve el tamaño actual de la memoria interna."""
        return len(self.memory)
