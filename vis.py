from flask import Flask, render_template, request
import numpy as np

app = Flask(__name__)

def lin_sys(A, y0, t):
    eigenval, eigenvec = np.linalg.eig(A)
    c = np.linalg.solve(eigenvec, y0)
    trajectory = np.zeros((len(y0), len(t)))
    for i in range(len(t)):
        trajectory[:, i] = np.dot(eigenvec, c * np.exp(eigenval * t[i]))
    return trajectory

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/simulate', methods = ['POST'])
def simulate():
    params = request.json
    A = np.array(params['A'], dtype = complex)
    t = np.arrange(params['time'])

    dim = A.shape[0]
    grid_size = 10
    c_ranges = [np.linspace(-2, 2, grid_size) for _ in range(dim)]
    c_grid = np.array(np.meshgrid(*c_ranges)).T.reshape(-1, dim)
    
    trajectories = []
    for c in c_grid:
        eigvals, eigvecs = np.linalg.eig(A)
        x0 = np.dot(eigvecs, c)
        trajectory = lin_sys(A, x0, t)
        trajectories.append(trajectory.tolist())
    
    return {"time": t.tolist(), "trajectories": trajectories}
