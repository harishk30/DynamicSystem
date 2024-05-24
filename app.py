from flask import Flask, request, jsonify, send_file, make_response
import numpy as np
from flask_cors import CORS
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Agg')
from io import BytesIO
from itertools import product

app = Flask(__name__, static_folder='build', static_url_path='')
CORS(app, resources={r"/*": {"origins": "https://sleepy-reef-04227-f51012b87050.herokuapp.com"}})

def lin_sys(A, c, t):
    eigenval, eigenvec = np.linalg.eig(A)
    trajectory = np.zeros((len(c), len(t)), dtype=complex)
    for i in range(len(t)):
        trajectory[:, i] = sum(c[j] * (eigenval[j] ** t[i]) * eigenvec[:, j] for j in range(len(c)))
    return trajectory

@app.route('/simulate', methods=['POST'])
def simulate():
    params = request.json
    time_range = params['timeRange']
    A = np.array(params['A'], dtype=complex)
    t = np.linspace(-time_range // 2, time_range // 2 + 1)

    dim = A.shape[0]
    sign_combinations = list(product([-5, 0, 5], repeat=dim))
    
    all_trajectories_x = []
    all_trajectories_y = []
    fig, ax = plt.subplots()
    cmap = plt.get_cmap('RdYlGn_r')
    eigvals, eigvecs = np.linalg.eig(A)
    for signs in sign_combinations:
        c = np.array(signs, dtype=complex)
        trajectory = lin_sys(A, c, t)
        all_trajectories_x.extend(trajectory[0, :].real)
        all_trajectories_y.extend(trajectory[1, :].real)
        for i in range(len(t)):
            color = cmap((t[i] - t.min()) / (t.max() - t.min()))
            ax.scatter(trajectory[0, i], trajectory[1, i], color=color, s=10)

    ax.set_title('Phase Portrait')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.axhline(0, color='black', linewidth=0.5)
    ax.axvline(0, color='black', linewidth=0.5)
    ax.grid(color='gray', linestyle='--', linewidth=0.5)

    x_min, x_max = min(all_trajectories_x), max(all_trajectories_x)
    y_min, y_max = min(all_trajectories_y), max(all_trajectories_y)
    ax.set_xlim([x_min - 1, x_max + 1])
    ax.set_ylim([y_min - 1, y_max + 1])

    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    response = make_response(send_file(buf, mimetype='image/png'))
    response.headers['Access-Control-Allow-Origin'] = 'https://sleepy-reef-04227-f51012b87050.herokuapp.com'
    return response

if __name__ == '__main__':
    app.run(debug=True)
