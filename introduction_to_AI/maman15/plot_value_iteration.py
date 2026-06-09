import matplotlib.pyplot as plt
import numpy as np

#NAME = "Omer Shraibshtein (205984271)"

def plot_value_iteration(i, mat, filename, title):
    max_abs_reward = abs(np.nanmax(mat))

    print(f"max value: {max_abs_reward}")

    fig = plt.imshow(mat, vmin=-max_abs_reward, vmax=max_abs_reward, cmap='seismic')

    plt.title(title.format(i=i))
    plt.colorbar()
    plt.savefig(filename + '.jpg')

    #plt.show()