"""IMU data playback with raw data plot and pose estimation 3d plot. (LSM9DS1 IMU)"""

"""CSV file column format: 'temp', 'acc_x', 'acc_y', 'acc_z', 'gyro_x', 'gyro_y', 'gyro_z', 'mag_x', 'mag_y', 'mag_z', 'time'"""


import pandas as pd
import seaborn
import matplotlib.pyplot as plt
import sys
import time
import matplotlib.animation as animation
import numpy as np
class PoseEstimationIMU():
    def __init__(self):
        self.csv_file = ''
        self.output = False
        self.imu_data = None
        self.input_data()
        self.csv_to_pandas()
        self.index = 0
        self.acc = np.asarray([[0, 0, 0]])
        self.gyro = np.asarray([[0, 0, 0]])
        self.mag = np.asarray([[0, 0, 0]])
        self.data = pd.DataFrame(columns=['temp', 'acc_x', 'acc_y', 'acc_z',
                                          'gyro_x', 'gyro_y', 'gyro_z', 'mag_x',
                                          'mag_y', 'mag_z', 'time'])
        # 2d projection                               
        self.fig, self.axs = plt.subplots(ncols=2, nrows=2, figsize=(7, 7))
        
        # 3d projection
        # self.fig, self.axs = plt.subplots(
        #     ncols=2, nrows=2, figsize=(7, 7), subplot_kw=dict(projection='3d'))

    def input_data(self):
        try:
            self.csv_file = sys.argv[1]
            if len(sys.argv) > 2:
                if sys.argv[2] == '--save':
                    self.output = True
        except (IndexError, TypeError):
            print("Check csv file path.")

    def csv_to_pandas(self):
        try:
            self.imu_data = pd.read_csv(self.csv_file)
        except FileNotFoundError:
            print("Unable to read provided file.")

    def genarator(self, index):
        try:
            yield self.imu_data.iloc[index]
        except KeyError:
            plt.pause(15)
            sys.exit(1)

    def plot_acc(self):
        seaborn.lineplot(ax=self.axs[0, 0], data=self.acc[1:, 0])
        seaborn.lineplot(ax=self.axs[0, 0], data=self.acc[1:, 1])
        seaborn.lineplot(ax=self.axs[0, 0], data=self.acc[1:, 2])

    def plot_gyro(self):
        seaborn.lineplot(ax=self.axs[1, 0], data=self.gyro[1:, 0])
        seaborn.lineplot(ax=self.axs[1, 0], data=self.gyro[1:, 1])
        seaborn.lineplot(ax=self.axs[1, 0], data=self.gyro[1:, 2])

    def plot_mag(self):
        seaborn.lineplot(ax=self.axs[1, 1], data=self.mag[1:, 0])
        seaborn.lineplot(ax=self.axs[1, 1], data=self.mag[1:, 1])
        seaborn.lineplot(ax=self.axs[1, 1], data=self.mag[1:, 2])

    '''TODO'''

    def plot_end_effector_pose(self):
        # end-effector pose estimation results
        self.axs[0, 1].set_xlim([0, 500])
        self.axs[0, 1].set_ylim([500, 0])
        # self.axs[0, 1].set_zlim([0, 500])

        # initial point (x, y, z) (265, 15, 375) plot (x, y, z) => robot (z, x, y)
        self.axs[0, 1].scatter(265, 375, 15)
        # base location
        self.axs[0, 1].scatter(250 , 250, 470)

    def save_video(slef, anim):
        writer = animation.FFMpegWriter(fps=10)
        anim.save('imu_pose_estimation.mp4', writer=writer)

    def update(self, index):
        data = next(self.genarator(index))

        # clear prev plots
        self.axs[0, 0].clear()
        self.axs[0, 1].clear()
        self.axs[1, 0].clear()
        self.axs[1, 1].clear()

        # update data
        self.acc = np.append(
            self.acc, [[data.acc_x, data.acc_y, data.acc_z]], axis=0)
        self.gyro = np.append(
            self.gyro, [[data.gyro_x, data.gyro_y, data.gyro_z]], axis=0)
        self.mag = np.append(
            self.mag, [[data.mag_x, data.mag_y, data.mag_z]], axis=0)

        # create new plots
        self.plot_acc()
        self.plot_gyro()
        self.plot_mag()
        self.plot_end_effector_pose()

        self.index += 1

    def main(self):
        anim = animation.FuncAnimation(plt.gcf(), self.update, frames=1000,
                                       interval=10, blit=False, repeat=False)
        if self.output == False:
            plt.show()
        elif self.output == True:
            plt.close()
            self.save_video(anim)


if __name__ == '__main__':
    PoseEstimationIMU().main()
