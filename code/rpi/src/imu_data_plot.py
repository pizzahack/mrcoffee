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
        self.data = pd.DataFrame(columns=['temp', 'acc_x', 'acc_y', 'acc_z',
                                          'gyro_x', 'gyro_y', 'gyro_z', 'mag_x',
                                          'mag_y', 'mag_z', 'time'])
        # 2d projection
        # self.fig, self.axs = plt.subplots(ncols=2, nrows=2, figsize=(7, 7))

        # 3d projection
        self.fig, self.axs = plt.subplots(
            ncols=2, nrows=2, figsize=(7, 7), subplot_kw=dict(projection='3d'))
        self.fig.suptitle(
            'End-effector pose estimation from IMU data. \n (90 degree CW turn) ', fontsize=12)

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
        ax = self.axs[0, 0]
        seaborn.lineplot(ax=self.axs[0, 0], data=self.data[[
                         'acc_x', 'acc_y', 'acc_z']]).set_title("Accelerometer")

    def plot_gyro(self):
        seaborn.lineplot(ax=self.axs[1, 0], data=self.data[[
                         'gyro_x', 'gyro_y', 'gyro_z']]).set_title("Gyroscope")

    def plot_mag(self):
        seaborn.lineplot(ax=self.axs[1, 1], data=self.data[[
                         'mag_x', 'mag_y', 'mag_z']]).set_title("Magnetometer")

    '''TODO'''

    def plot_end_effector_pose(self):
        # end-effector pose estimation results
        self.axs[0, 1].set_title("end-effector")
        self.axs[0, 1].set_xlim([0, 500])
        self.axs[0, 1].set_ylim([500, 0])
        self.axs[0, 1].set_zlim([0, 500])

        # initial point (x, y, z) (265, 15, 375) plot (x, y, z) => robot (z, x, y)
        self.axs[0, 1].scatter(265, 375, 15, color='b')

        # base location
        # self.axs[0, 1].scatter(250, 250, 470)

    def save_video(slef, anim):
        writer = animation.FFMpegWriter(fps=10)
        anim.save('imu_pose_estimation.mp4', writer=writer)

    def update(self, index):
        g = next(self.genarator(index))

        # clear prev plots
        self.axs[0, 0].clear()
        self.axs[0, 1].clear()
        self.axs[1, 0].clear()
        self.axs[1, 1].clear()

        # update data
        new_row = {'temp': g.temp, 'acc_x': g.acc_x, 'acc_y': g.acc_y, 'acc_z': g.acc_z,
                   'gyro_x': g.gyro_x, 'gyro_y': g.gyro_y, 'gyro_z': g.gyro_z,
                   'mag_x': g.mag_x, 'mag_y': g.mag_y, 'mag_z': g.mag_z,
                   'time': g.time}

        self.data = self.data.append(new_row, ignore_index=True)

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
