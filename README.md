



Welcome to DataDrei, a Python and Java-based project that utilizes IntelliJ IDEA 2022.3.3 for data collection and analysis. This README will guide you through setting up the project, configuring your environment, and running the application.

RUN "click this and everything should work.bat" inside src\datameasureDrei and 3(hehe) Windows should open that look like this   
![after clicking the bat](https://gyazo.com/09cb58eb69f48222e16357129149a97d.png)


Setup
1. Install the Python plugin for IntelliJ IDEA:
+ Open IntelliJ IDEA.
+ Go to File > Settings (on Windows/Linux) or IntelliJ IDEA > Preferences (on macOS).
+ Navigate to Plugins in the left pane.
+ Click the Marketplace tab and search for "Python".
+ Install the "Python" plugin and restart IntelliJ IDEA.

2. Create a new project:
+ In IntelliJ IDEA, go to File > New > Project.
+ In the "New Project" window, choose Java + Build system IntelliJ.
+ Click "create".

3. Add Python support to the project:
+ Right-click the src folder in your project, then click New > Directory and name it "datameasureDrei".
+ Move your main.py and data_collector.py files into the "datameasureDrei" directory.
+ Create a config.ini inside the "datameasureDrei" folder and add the following content:
```[settings]
server_url=http://127.0.0.1:7744/datameasure/data1
hello_url=http://127.0.0.1:7744/hello
polling_interval=1
```
+ Make datameasureDrei your root directory or write the following content into your dataDrei.iml file:
```<?xml version="1.0" encoding="UTF-8"?>
<module type="JAVA_MODULE" version="4">
  <component name="NewModuleRootManager" inherit-compiler-output="true">
    <exclude-output />
    <content url="file://$MODULE_DIR$">
      <sourceFolder url="file://$MODULE_DIR$/datameasureDrei" isTestSource="false" />
      <excludeFolder url="file://$MODULE_DIR$/venv" />
    </content>
    <orderEntry type="jdk" jdkName="Python 3.10 (dataDrei)" jdkType="Python SDK" />
    <orderEntry type="sourceFolder" forTests="false" />
  </component>
</module>
```

4. Configure Python SDK:
+ Go to File > Project Structure > SDKs.
+ Click the + button and choose Python SDK.
+ Click OK to save the changes.

Running the Project

1. Install the required Python packages by running the following command in the terminal:
+ pip install -r requirements.txt

2. If you haven't installed Java, download and install it from Oracle's official website.  https://www.oracle.com/java/technologies/downloads/#jdk20-windows
3. Run the program by typing the following command in the terminal:
+ java -jar datameasure.jar
4. After executing the App.java file, run the main.py file. A GUI should open, displaying the results of your data analysis.

Enjoy using DataDrei! If you have any questions or need support, please refer to the project's GitHub repository for additional information and assistance.


