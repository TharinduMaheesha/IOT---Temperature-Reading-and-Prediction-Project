Internet of Things can be described as devices which are equipped with sensors, processing power and some software which connects and communicates with other devices to perform some specific tasks based on shared data over the internet. As mentioned by [1] the aim of IoT is unite everything that is around us as one infrastructure which will allow us to control what is going on around us and to keep us informed about it. IoT enables us to convert any device into an intelligent device which at the present are labeled as ‘’Smart Devices”.

The main goal of this project is to develop a basic IoT based temperature monitoring and predicting systems using raspberry pi, node-red, a sensor and an actuator with python for backend development
A temperature sensor will used to capture the current ambient temperature which will be taken as the main input for this monitoring system. Based to the read temperature in a build display gauge an actuator will be used to show the effect of the temperature. This effect will be shown as follows.

• If the read temperature is less than or equal to 20 degrees Celsius the effect will be shown as cool

• If the read temperature is between 20 degrees Celsius and 30 degrees Celsius the effect will be shown as warm

• If the read temperature exceeds 30 degrees Celsius the effect will be shown as hot


The axel of the actuator will be moved to specific angles based on the read temperature to display the effect on the gauge.
The read temperature will also be published on a node-red dashboard using MQTT. In addition to the display of current temperature the dashboard will contain a visualization of past captured data along with a prediction of temperature up to 12 months ahead. The ARIMA model will be used for the prediction of the temperature.
