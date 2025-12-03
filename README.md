# ODE Methods Website

An interactive educational website for learning different methods to solve Ordinary Differential Equations (ODEs).

## Features

- **Separation of Variables**: Learn how to solve first-order ODEs by separating variables
- **Undetermined Coefficients**: Method for finding particular solutions to linear nonhomogeneous ODEs
- **Integrating Factor**: Technique for solving first-order linear ODEs
- **Characteristic Polynomials**: Method for solving linear homogeneous ODEs with constant coefficients
- **Phase Portraits**: Interactive visualization of ODE systems with matplotlib

Each method page includes:
- Theory and explanation
- Homogeneous and nonhomogeneous solution sections
- Concrete examples with step-by-step solutions
- Interactive ODE solver

## Installation

1. Install Python 3.8 or higher
2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Website

1. Start the Flask server:
```bash
python app.py
```

2. Open your browser and navigate to:
```
http://localhost:5000
```

## Project Structure

```
ODE website/
├── app.py                 # Flask application with routes and API endpoints
├── requirements.txt       # Python dependencies
├── templates/            # HTML templates
│   ├── base.html         # Base template with navigation
│   ├── index.html        # Homepage
│   ├── separation_of_variables.html
│   ├── undetermined_coefficients.html
│   ├── integrating_factor.html
│   ├── characteristic_polynomials.html
│   └── phase_portraits.html
└── static/
    ├── css/
    │   └── style.css     # Styling
    └── js/
        └── main.js       # JavaScript utilities
```

## Usage

### Solving ODEs

On each method page, you can enter an ODE in the interactive section and get a solution. The format depends on the method:

- **Separation of Variables**: `dy/dx = x*y`
- **Integrating Factor**: `dy/dx + 2xy = x`
- **Characteristic Polynomials**: `y'' - 5y' + 6y = 0`
- **Undetermined Coefficients**: `y'' - 3y' + 2y = x^2`

### Phase Portraits

On the Phase Portraits page:
- Select a preset type (Saddle, Nodal Sink, Spiral, Center) to see examples
- Or create your own by entering `dx/dt` and `dy/dt` expressions
- Use Python/numpy syntax (e.g., `y`, `-x - y`, `np.sin(x)`, etc.)

## Technologies

- **Backend**: Flask (Python web framework)
- **Math**: SymPy (symbolic mathematics)
- **Visualization**: Matplotlib (phase portraits)
- **Frontend**: HTML5, CSS3, JavaScript
- **Math Rendering**: MathJax

## Notes

- The ODE solver uses SymPy and may not handle all ODE formats. For best results, use standard mathematical notation.
- Phase portraits are generated server-side using matplotlib and displayed as images.
- The website is designed for educational purposes and demonstrates various ODE solving techniques.

