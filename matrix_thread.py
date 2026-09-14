import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
from concurrent.futures import ThreadPoolExecutor
import threading

# Matrix size
size = 100

# Create two 100 x 100 matrices with random values
A = tf.constant(np.random.randint(1, 10, (size, size)), dtype=tf.float32)
B = tf.constant(np.random.randint(1, 10, (size, size)), dtype=tf.float32)

# Matrix to store the final answer
C = np.zeros((size, size))

# Lock is used when updating the operation count
lock = threading.Lock()
completed = 0


# Function for one multiplication
def multiply(row, column, k):
    global completed

    value = tf.multiply(A[row, k], B[k, column]).numpy()

    with lock:
        completed += 1

    return value


# Calculate one value of the result matrix
def calculate_value(row, column, pool):
    total = 0
    jobs = []

    # Perform each multiplication using a thread
    for k in range(size):
        job = pool.submit(multiply, row, column, k)
        jobs.append(job)

    # Add the multiplication results
    for job in jobs:
        total += job.result()

    C[row, column] = total


# Set up the animation
plt.ion()

fig, ax = plt.subplots()
matrix_image = ax.imshow(C, cmap="viridis")

ax.set_title("Matrix Multiplication Using Threads")
plt.colorbar(matrix_image)


# Create a group of worker threads
with ThreadPoolExecutor(max_workers=20) as pool:

    for row in range(size):
        for column in range(size):

            calculate_value(row, column, pool)

            # Update the animation after every 10 elements
            if (row * size + column) % 10 == 0:

                matrix_image.set_data(C)

                ax.set_title(
                    "Matrix Multiplication Using Threads\n"
                    "Completed: "
                    + str(completed)
                    + " / "
                    + str(size * size * size)
                )

                plt.pause(0.01)


# Display the completed matrix
matrix_image.set_data(C)
ax.set_title("Matrix Multiplication Completed!")

plt.ioff()
plt.show()


print("Matrix multiplication completed successfully.")
print("Matrix A size:", A.shape)
print("Matrix B size:", B.shape)
print("Result matrix C size:", C.shape)