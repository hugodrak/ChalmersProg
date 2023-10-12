# Power system optimization for minimizing generation cost while meeting system constraints.

using SparseArrays
# Remember indexing from 1!
# ======================
# DATA DEFINITIONS
# ======================

# 1.1 Unknown variables
theta_min = -pi
theta_max = pi
v_min = 0.98
v_max = 1.02
W_min = 0
W_max = [0.02, 0.15, 0.08, 0.07, 0.04, 0.17, 0.17, 0.26, 0.05]

# 1.2 Constants for generators
N=9; # Number of generators
C = [175, 100, 150, 150, 300, 350, 400, 300, 200]
Z = 0.003 .* W_max # Maximum reactive power that the generators can handle 0.3%.
parent_node_g = [2, 2, 2, 3, 4, 5, 7, 9, 9]
# 1.3 Constants for the consumer
L = 6
D = [0.10, 0.19, 0.11, 0.09, 0.21, 0.05, 0.04]
parent_node_c = [1, 4, 6, 8, 9, 10, 11]

# 1.4 Constants for the nodes
M = 11; # Number of nodes
# Mapping of generators at each node k
G = [
    [],         # Node 1
    [1, 2, 3],  # Node 2
    [4],        # Node 3
    [5],        # Node 4
    [6],        # Node 5
    [],         # Node 6
    [7],        # Node 7
    [],         # Node 8
    [8, 9],     # Node 9
    [],         # Node 10
    []          # Node 11
]

# Mapping of consumer at each node k
K = [
    [1],        # Node 1
    [],         # Node 2
    [],         # Node 3
    [2],        # Node 4
    [],         # Node 5
    [3],        # Node 6
    [],         # Node 7
    [4],        # Node 8
    [5],        # Node 9
    [6],        # Node 10
    [7]         # Node 11
]

Q_max = [isempty(k) ? 0 : sum(Z[i] for i in k) for k in G] # Maximal reactive power that can be taken up in a node Q_max
b_values = [20.1, -22.3, -16.8, -17.2, -11.7, -19.4, -10.8, -12.3, -9.2, -13.9, -8.7, -11.3, -14.7, -13.5, -26.7]
g_values = [4.12, 5.67, 2.41, 2.78, 1.98, 3.23, 1.59, 1.71, 1.26, 1.11, 1.32, 2.01, 2.41, 2.14, 5.06]
node_pairs = [(1, 2), (1, 11), (2, 3), (2, 11), (3, 4), (3, 9), (4, 5), (5, 6), (5, 8), (6, 7), (7, 8), (7, 9), (8, 9), (9, 10), (10, 11)]

# Initializing the matrices with coefficients for the edges
b_kl = spzeros(M, M)
g_kl = spzeros(M, M)



for (index, (k, l)) in enumerate(node_pairs)
    matrices = [b_kl, g_kl]
    coefficients = [b_values, g_values]
    
    for (mat_idx, mat) in enumerate(matrices)
        coeff = coefficients[mat_idx]
        mat[k, l], mat[l, k] = coeff[index], coeff[index]
    end
end


# ======================
# FUNCTION DEFINITIONS
# ======================
# 1.6 cosntraints between two nodes k,l
# Amount of active power
function p_kl(v_k, v_l, theta_k, theta_l, g_kl, b_kl)
    return v_k^2.0 * g_kl - v_k * v_l * g_kl*cos(theta_k - theta_l) - v_k * v_l * b_kl * sin(theta_k - theta_l)
end

# Amount of reactive power
function q_kl(v_k, v_l, theta_k, theta_l, g_kl, b_kl)
    return -v_k^2.0 * b_kl + v_k * v_l * b_kl*cos(theta_k - theta_l) - v_k * v_l * g_kl * sin(theta_k - theta_l)
end

function p_kl_float(v_k, v_l, theta_k, theta_l, g_kl, b_kl)::Float64
    return v_k^2.0 * g_kl - v_k * v_l * g_kl*cos(theta_k - theta_l) - v_k * v_l * b_kl * sin(theta_k - theta_l)
end

# Amount of reactive power
function q_kl_float(v_k, v_l, theta_k, theta_l, g_kl, b_kl)::Float64
    return -v_k^2.0 * b_kl + v_k * v_l * b_kl*cos(theta_k - theta_l) - v_k * v_l * g_kl * sin(theta_k - theta_l)
end
