# MazBazPyo Installation Guide 🚀

## Prerequisites

- Git
- [Anaconda Navigator](https://www.anaconda.com/products/distribution) installed on your system.

## Installation & Usage

1. Clone this repository to your local machine:

    ```bash
    git clone https://github.com/B2-Info-23-24/agarpyo-b2-b-MazBazDev.git
    ```

2. Navigate to your project directory:

    ```bash
    cd agarpyo-b2-b-MazBazDev
    ```

3. Create a Conda environment from the provided `environment.yaml` file:

    ```bash
    conda env create -f environment.yaml
    ```

4. Activate the newly created environment:

    ```bash
    conda activate mazbazpyo
    ```

## Usage

   ```bash
  python main.py
   ```

# Features 🎮

### Game Modes
Game modes are selectable by clicking on the corresponding text in the menu.

### 🖱️ Play with Keyboard: You can move your player using the keys z, q, s, d
### ⌨️ Play with Mouse: Your player will follow the direction of your mouse.

### Difficulties
- **Level 2 (Easy):** 2 traps and 5 foods.
- **Level 3 (Medium):** 3 traps and 3 foods.
- **Level 4 (Hard):** 4 traps and 2 foods.

### Game Rules
- You have 60 seconds to achieve the highest possible score, so watch out for the timer! 😉
- If your character is bigger than a trap, your size and your speed will be divided by the current level number.
- You earn points by eating food.

### Controls
   In the menu:
   - **p :** Play with keyboard.
   - **q :** Exit the game.
   
   During the game:
   - **esc or escape:** End the game.
   
   Any text preceded by an arrow is clickable.
   If a text is preceded by a red circle, it means the option is selected.

## Author

- [MazBazDev](https://github.com/MazBazDev)