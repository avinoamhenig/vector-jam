VectorJAM
---------

Juliet Slade and Avinoam Henig

Conference project for Quantum Computing - Jim Marshall

Fall 2016

SETUP INSTRUCTIONS

1. Install pillow
2. Navigate to vector-jam directory in terminal
3. python3 main.py


DOCUMENTATION

- Upon booting up VectorJAM, the grid on the right represents a two-dimensional real vector space.
	- The slide at the very bottom of the left panel adjusts the scale of this grid.
- The blue arrow is a two-dimensional vector in the vector space.
	- You can drag anywhere on the grid to move this vector.
  - The values of the vector are displayed in transposed-row-vector form in the blue label in the left panel.
  - You can normalize this vector at any time by pressing the 'Normalize Vector' button.
- The four boxes below the VectorJAM logo correspond to a 2x2 matrix.
	- You can input new values into the boxes and press update to update the current matrix.
  - Clicking adjoint will give the adjoint of the current matrix.
  - If the matrix is Hermitian or Unitary, labels will show up indicating this.
  	- If the matrix is Unitary, 'Step Back' and 'Step' buttons will appear, clicking these will apply the unitary
    	matrix to the state vector (in Step's case) and the adjoint of the matrix in Step Back's case.
  - You can put imaginary numbers in the matrix, using 'i'. This will enter the program into complex mode.
  - There are seven built-in matrixes
- To see the effect of multiplying the matrix with the blue vector, check the 'Show product vector?' checkbox.
	- This will show a red vector, the product vector, that is equal to MATRIX * BLUE.
  - The values of the vector are displayed in transposed-row-vector form in the red label in the left panel.
- You can see the eigenbasis vectors for the current matrix by checking the 'Show Eigenbasis?' checkbox.
	- The eigenbasis vectors will appear as to arrows – one green and one orange.
	- While not in complex mode, this will also visualize the eigenspaces as two dashed lines.
  - The corresponding eigenvalues, λ1 and λ2, are displayed as green and orange labels in the left panel.
  - If the current matrix is hermitian, the probabilities P1 and P2 of measuring each eigenvalue,
    given the current state of the blue vector, are also displayed as green and orange labels in the left panel.
- You can show the results of projecting the state vector onto the eigenbasis vectors by checking the "Show inner products?" checkbox.
	- This calculates the inner products of the state vector and the spaces.
  - This also normalizes the blue vector behind the scenes before calculatin the inner products.
- Checking the 'Qubit Mode' checkbox will automatically normalize the blue vector as you change its state.
	- This allows you to think of the vector as real-valued qubit in non-complex mode, and a full-on qubit in complex mode.
- If the current matrix is hermitian, you can simulate measuring the blue vector using the current matrix by pressing the 'measure' button.
	- This will probabilistically snap the blue vector to one of the eigenbasis vectors based on the probabilities P1 and P2.
  - The eigenvalue corresponding to the result of the measurement will be highlighted in yellow in left panel.

- Checking "Complex Plane" enters complex mode, which changes the grid on the right so that it now represents a complex plane.
	- The state vector is now represented as two blue lines, a solid one and a dashed one.
  	- Each corresponds to one of the complex numbers of the state vector.
    - The solid line corresponds to the first complex number, and the dashed line to the second.
	  - You can move either of them by clicking close to it and dragging.
	- In a similar fashion to the non-complex mode, the matrix's effect on the blue state vector can be seen by selecting the
	  "Show product vector?" checkbox and the red vector will appear, also represented by two lines.
	- Checking the 'Qubit Mode' checkbox in complex mode will normalize the blue vector and this will be reflected in the manipulations
	  of either of its complex numbers.
		- Dragging the dashed line around changes the solid line and vice versa, so that the vector remains normalized at all times.
	- In complex mode the eigenspaces cannot be visualized.
  - The eigenbasis vectors will also each be represented as two lines, one solid and one dashed.
  - Leaving complex mode will automatically reset each number in the vector to the magnitude of the complex number that was there.
  	- Same thing for the matrix.

ENJOY!
- Juliet, Avinoam, and Math <3
