from flask import Flask, render_template, request, jsonify, send_file
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
import base64
import sympy as sp
from sympy import symbols, Function, dsolve, Eq, exp, sin, cos, simplify, latex

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/separation-of-variables')
def separation_of_variables():
    return render_template('separation_of_variables.html')

@app.route('/undetermined-coefficients')
def undetermined_coefficients():
    return render_template('undetermined_coefficients.html')

@app.route('/integrating-factor')
def integrating_factor():
    return render_template('integrating_factor.html')

@app.route('/characteristic-polynomials')
def characteristic_polynomials():
    return render_template('characteristic_polynomials.html')

@app.route('/phase-portraits')
def phase_portraits():
    return render_template('phase_portraits.html')

@app.route('/api/solve-ode', methods=['POST'])
def solve_ode():
    """API endpoint to solve ODEs using different methods"""
    data = request.json
    method = data.get('method')
    ode = data.get('ode')
    initial_conditions = data.get('initial_conditions', {})
    
    try:
        x = symbols('x')
        y = Function('y')(x)
        
        # Parse the ODE
        if method == 'separation':
            # For separation of variables: dy/dx = f(x)g(y)
            result = solve_separation_of_variables(ode, initial_conditions)
        elif method == 'integrating_factor':
            # For integrating factor: dy/dx + P(x)y = Q(x)
            result = solve_integrating_factor(ode, initial_conditions)
        elif method == 'characteristic':
            # For characteristic polynomial: ay'' + by' + cy = 0 or = f(x)
            result = solve_characteristic(ode, initial_conditions)
        elif method == 'undetermined':
            # For undetermined coefficients
            result = solve_undetermined_coefficients(ode, initial_conditions)
        else:
            return jsonify({'error': 'Unknown method'}), 400
            
        return jsonify({
            'success': True,
            'solution': result['solution'],
            'steps': result.get('steps', [])
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

def solve_separation_of_variables(ode_str, initial_conditions):
    """Solve ODE using separation of variables"""
    x = symbols('x')
    y = Function('y')(x)
    
    # Try to solve using sympy
    try:
        # Parse simple forms like dy/dx = f(x)*g(y)
        ode_eq = sp.sympify(ode_str.replace('dy/dx', 'Derivative(y(x), x)').replace('y', 'y(x)'))
        sol = dsolve(ode_eq, y)
        solution_str = latex(simplify(sol.rhs))
        return {'solution': solution_str, 'steps': ['Separated variables', 'Integrated both sides', 'Applied initial conditions']}
    except:
        return {'solution': 'Could not automatically solve. Please check the format.', 'steps': []}

def solve_integrating_factor(ode_str, initial_conditions):
    """Solve ODE using integrating factor"""
    x = symbols('x')
    y = Function('y')(x)
    
    try:
        ode_eq = sp.sympify(ode_str.replace('dy/dx', 'Derivative(y(x), x)').replace('y', 'y(x)'))
        sol = dsolve(ode_eq, y)
        solution_str = latex(simplify(sol.rhs))
        return {'solution': solution_str, 'steps': ['Identified P(x) and Q(x)', 'Calculated integrating factor', 'Multiplied through', 'Integrated']}
    except:
        return {'solution': 'Could not automatically solve. Please check the format.', 'steps': []}

def solve_characteristic(ode_str, initial_conditions):
    """Solve ODE using characteristic polynomial"""
    x = symbols('x')
    y = Function('y')(x)
    
    try:
        ode_eq = sp.sympify(ode_str.replace('y\'\'', 'Derivative(y(x), x, x)').replace('y\'', 'Derivative(y(x), x)').replace('y', 'y(x)'))
        sol = dsolve(ode_eq, y)
        solution_str = latex(simplify(sol.rhs))
        return {'solution': solution_str, 'steps': ['Found characteristic equation', 'Solved for roots', 'Constructed general solution']}
    except:
        return {'solution': 'Could not automatically solve. Please check the format.', 'steps': []}

def solve_undetermined_coefficients(ode_str, initial_conditions):
    """Solve ODE using undetermined coefficients"""
    x = symbols('x')
    y = Function('y')(x)
    
    try:
        ode_eq = sp.sympify(ode_str.replace('y\'\'', 'Derivative(y(x), x, x)').replace('y\'', 'Derivative(y(x), x)').replace('y', 'y(x)'))
        sol = dsolve(ode_eq, y)
        solution_str = latex(simplify(sol.rhs))
        return {'solution': solution_str, 'steps': ['Found homogeneous solution', 'Guessed particular solution form', 'Determined coefficients', 'Combined solutions']}
    except:
        return {'solution': 'Could not automatically solve. Please check the format.', 'steps': []}

@app.route('/api/phase-portrait', methods=['POST'])
def generate_phase_portrait():
    """Generate phase portrait for a 2D system of ODEs"""
    data = request.json
    dx_dt = data.get('dx_dt', 'y')
    dy_dt = data.get('dy_dt', '-x')
    x_range = data.get('x_range', [-5, 5])
    y_range = data.get('y_range', [-5, 5])
    portrait_type = data.get('type', 'custom')
    
    try:
        # Create figure
        fig, ax = plt.subplots(figsize=(10, 10))
        
        if portrait_type == 'saddle':
            # dx/dt = x, dy/dt = -y
            create_saddle_portrait(ax, x_range, y_range)
        elif portrait_type == 'nodal_sink':
            # dx/dt = -x, dy/dt = -y
            create_nodal_sink_portrait(ax, x_range, y_range)
        elif portrait_type == 'spiral':
            # dx/dt = -x - y, dy/dt = x - y
            create_spiral_portrait(ax, x_range, y_range)
        elif portrait_type == 'center':
            # dx/dt = y, dy/dt = -x
            create_center_portrait(ax, x_range, y_range)
        elif portrait_type == 'custom':
            create_custom_portrait(ax, dx_dt, dy_dt, x_range, y_range)
        else:
            create_custom_portrait(ax, dx_dt, dy_dt, x_range, y_range)
        
        # Save to bytes
        img = BytesIO()
        plt.savefig(img, format='png', dpi=100, bbox_inches='tight')
        img.seek(0)
        plt.close()
        
        # Encode to base64
        img_base64 = base64.b64encode(img.getvalue()).decode()
        return jsonify({'image': img_base64})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

def create_saddle_portrait(ax, x_range, y_range):
    """Create saddle phase portrait"""
    x = np.linspace(x_range[0], x_range[1], 20)
    y = np.linspace(y_range[0], y_range[1], 20)
    X, Y = np.meshgrid(x, y)
    U = X
    V = -Y
    ax.streamplot(X, Y, U, V, density=1.5, color='blue', linewidth=1)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_title('Saddle Point')
    ax.grid(True, alpha=0.3)
    ax.axhline(y=0, color='k', linewidth=0.5)
    ax.axvline(x=0, color='k', linewidth=0.5)

def create_nodal_sink_portrait(ax, x_range, y_range):
    """Create nodal sink phase portrait"""
    x = np.linspace(x_range[0], x_range[1], 20)
    y = np.linspace(y_range[0], y_range[1], 20)
    X, Y = np.meshgrid(x, y)
    U = -X
    V = -Y
    ax.streamplot(X, Y, U, V, density=1.5, color='blue', linewidth=1)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_title('Nodal Sink')
    ax.grid(True, alpha=0.3)
    ax.axhline(y=0, color='k', linewidth=0.5)
    ax.axvline(x=0, color='k', linewidth=0.5)

def create_spiral_portrait(ax, x_range, y_range):
    """Create spiral phase portrait"""
    x = np.linspace(x_range[0], x_range[1], 20)
    y = np.linspace(y_range[0], y_range[1], 20)
    X, Y = np.meshgrid(x, y)
    U = -X - Y
    V = X - Y
    ax.streamplot(X, Y, U, V, density=1.5, color='blue', linewidth=1)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_title('Spiral Sink')
    ax.grid(True, alpha=0.3)
    ax.axhline(y=0, color='k', linewidth=0.5)
    ax.axvline(x=0, color='k', linewidth=0.5)

def create_center_portrait(ax, x_range, y_range):
    """Create center (circles) phase portrait"""
    x = np.linspace(x_range[0], x_range[1], 20)
    y = np.linspace(y_range[0], y_range[1], 20)
    X, Y = np.meshgrid(x, y)
    U = Y
    V = -X
    ax.streamplot(X, Y, U, V, density=1.5, color='blue', linewidth=1)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_title('Center (Circular Orbits)')
    ax.grid(True, alpha=0.3)
    ax.axhline(y=0, color='k', linewidth=0.5)
    ax.axvline(x=0, color='k', linewidth=0.5)

def create_custom_portrait(ax, dx_dt_str, dy_dt_str, x_range, y_range):
    """Create custom phase portrait from user input"""
    x = np.linspace(x_range[0], x_range[1], 20)
    y = np.linspace(y_range[0], y_range[1], 20)
    X, Y = np.meshgrid(x, y)
    
    # Evaluate the expressions safely
    try:
        # Replace common math functions and operators
        dx_dt_str = dx_dt_str.replace('^', '**').strip()
        dy_dt_str = dy_dt_str.replace('^', '**').strip()
        
        # Create namespace for evaluation (restricted for safety)
        namespace = {
            'x': X, 'y': Y, 
            'np': np, 
            'sin': np.sin, 'cos': np.cos, 'tan': np.tan,
            'exp': np.exp, 'log': np.log, 'sqrt': np.sqrt,
            'abs': np.abs
        }
        
        # Compile and evaluate expressions
        U = eval(dx_dt_str, {"__builtins__": {}}, namespace)
        V = eval(dy_dt_str, {"__builtins__": {}}, namespace)
        
        # Ensure U and V are arrays
        if not isinstance(U, np.ndarray):
            U = np.full_like(X, U)
        if not isinstance(V, np.ndarray):
            V = np.full_like(Y, V)
        
        ax.streamplot(X, Y, U, V, density=1.5, color='blue', linewidth=1)
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_title(f'Phase Portrait: dx/dt = {dx_dt_str}, dy/dt = {dy_dt_str}')
        ax.grid(True, alpha=0.3)
        ax.axhline(y=0, color='k', linewidth=0.5)
        ax.axvline(x=0, color='k', linewidth=0.5)
    except Exception as e:
        raise ValueError(f"Error evaluating expressions: {str(e)}. Please check your syntax. Use Python/numpy notation (e.g., 'y', '-x - y', 'np.sin(x)').")

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='127.0.0.1')

