# README

Developed 5 very primitive solvers for the traffic problem.

### 1. Green wave (~20K points)
Finds a car that can make it to the destination and makes a chain of green lights for that car.

### 2. Round robin (~7.9M points)
On each intersection, turn on each of its lights one by one.

Each light is green for one second.

### 3. Greedy round robin (~8.5M points)
On each intersection, turn on each of its lights one by one.

Each light is green for enough time so that all initially queued cars may pass.

Don't open the streets in which no one wants to go initially.

### 4. Proportional round robin (~8.5M points)
On each intersection, turn on each of its lights one by one.

Each light is green proportional to how busy the street initially is.

Also open the streets in which no one wants to go initially for 1 second.

### 5. Random round robin (~9.0M points)
On each intersection, turn on each of its lights one by one.

Each light is green for a random amount of time between 1 and 5 seconds.

Don't open the streets in which no one wants to go initially.
