from DataManager import DataDivision
from AI_Manager import AI_Manager
import matplotlib.pyplot as plt


dataManager = DataDivision('agv.pkl')

data = dataManager._divided_data[-1]
subset1 = data[100:8100] 
subset2 = data[8100:10100]

aiManager = AI_Manager(20)
# aiManager.preprocess_data(subset1, subset2)
# aiManager.train_model()

# tms_data = [56.0,20.0,48.0,52.0,16.0,44.0,12.0,36.0,4.0]
tms_data = [7.0,39.0, 15.0, 47.0, 19.0, 55.0, 51.0, 27.0, 63.0]
# df = dataManager._fullData[92:122]
df = dataManager._fullData[233:254]
avg_points_amount = dataManager._average_points_amount

predicted = aiManager.predict_route(df, tms_data)

plt.scatter(dataManager._divided_data[0]['X-coordinate'],dataManager._divided_data[0]['Y-coordinate'])
plt.scatter(predicted['X-coordinate'],predicted['Y-coordinate'], color = 'red')
plt.show()