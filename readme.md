1. Install all the dependencies from the requirements.txt file.
2. Make sure to install a webdriver, based on your current version of your browser.
More details: https://www.youtube.com/watch?v=7R5n0sNSza8&ab_channel=StudentEnginee and
https://selenium-python.readthedocs.io/installation.html
3. Put the driver in  the drivers folder. 
4. Name the driver executable file according to the following logic:

if YourBrowserName == "chrome": \
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;name the executable file "chrome"   
elif YourBrowserName == "edge": \
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;name the executable file "edge" \
elif YourBrowserName == "firefox": \
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;name the executable file "firefox" \
elif YourBrowserName == "safari": \
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;name the executable file "safari" \
elif YourBrowserName == "opera": \
 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;name the executable file "chrome" \
else: \
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; sorry we don't support your browser at the moment

5. Change BROWSER_NAME according to your needs
