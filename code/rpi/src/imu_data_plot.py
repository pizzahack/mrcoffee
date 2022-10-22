"""IMU data playback with raw data plot and pose estimation 3d plot. (LSM9DS1 IMU)"""
import pandas as pd
import time
import seaborn
import matplotlib.pyplot as plt
import sys


class PoseEstimationIMU():
    def __init__(self):
        self.csv_file = ''
        self.imu_data = None
        self.input_data()
        self.csv_to_pandas()

    def input_data(self):
        try:
            self.csv_file = sys.argv[1]
        except (IndexError, TypeError):
            print("Check csv file path.")

    def csv_to_pandas(self):
        try:
            self.imu_data = pd.read_csv(self.csv_file)
        except FileNotFoundError:
            print("Unable to read provided file.")

    def genarator(self, i):
        yield self.imu_data.loc[i]

    def main(self):
        for i in range(self.imu_data.shape[0]):
            time.sleep(0.05)
            data = next(self.genarator(i))
            data_str = {'temp': data.temp, 'acc_x': data.acc_x, 'acc_y': data.acc_y, 'acc_z': data.acc_z,
                        'gyro_x': data.gyro_x, 'gyro_y': data.gyro_y, 'gyro_z': data.gyro_z,
                        'mag_x': data.mag_x, 'mag_y': data.mag_y, 'mag_z': data.mag_z,
                        'time': data.time}
            print(data_str)


if __name__ == '__main__':
    PoseEstimationIMU().main()
