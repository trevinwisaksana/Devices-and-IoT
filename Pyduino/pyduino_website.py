from flask import Flask, render_template,request, redirect, url_for
from pyduino import *
import time

app = Flask(__name__)

# initialize connection to Arduino
# if your arduino was running on a serial port other than '/dev/ttyACM0/'
# declare: a = Arduino(serial_port='/dev/ttyXXXX')
a = Arduino()
time.sleep(3)

# declare the pins we're using
LED_PIN_GREEN = 6
LED_PIN_BLUE = 8
LED_PIN_RED = 10
ANALOG_PIN = 0

# initialize the digital pin as output
# a.set_pin_mode(LED_PIN,'O')

print 'Arduino initialized'

# we are able to make 2 different requests on our webpage
# GET = we just type in the url
# POST = some sort of form submission like a button
@app.route('/', methods = ['POST','GET'])
def hello_world():

    # variables for template page (templates/index.html)
    author = "Harambe"

    # if we make a post request on the webpage aka press button then do stuff
    if request.method == 'POST':

        # if we press the turn on button
        if request.form['submit'] == 'Turn On':
            print 'TURN ON'

            # turn on LED on arduino
            a.is_normal()

        # if we press the Turn Green button
        if request.form['submit'] == 'Emergency Mode':
            print 'Emergency mode'

            # turn on LED that is Green
            a.emergency_mode()

        if request.form['submit'] == 'Normal Mode':
            print 'Normal mode'

            # Turn LED's to work normally
            a.is_normal()

        # if we press the turn off button
        elif request.form['submit'] == 'Turn Off':
            print 'TURN OFF'

            # turn off LED on arduino
            a.digital_write(LED_PIN_GREEN, 0)
            a.digital_write(LED_PIN_RED, 0)
            a.digital_write(LED_PIN_BLUE, 0)

        else:
            pass

    # read in analog value from photoresistor
    time.sleep(1)
    # readval = a.analog_read(ANALOG_PIN)

    # the default page to display will be our template with our template variables
    '''value=100*(readval/1023.)'''
    return render_template('index.html', author=author, value = 0)


# unsecure API urls
@app.route('/turnon', methods=['GET'] )
def turn_on():
    time.sleep(3)
    # sleep to ensure ample time for computer to make serial connection

    a.set_pin_mode(LED_PIN,'O')
    # initialize the digital pin as output

    time.sleep(1)
    # allow time to make connection

    for i in range(0,1000):
        if i%2 == 0:
            a.digital_write(LED_PIN,1) # turn LED on
        else:
            a.digital_write(LED_PIN,0) # turn LED off

        time.sleep(1)
    return redirect( url_for('hello_world') )


@app.route('/turnoff', methods=['GET'] )
def turn_off():
    # turn off LED on arduino
    a.digital_write(LED_PIN,0)
    return redirect( url_for('hello_world') )



if __name__ == "__main__":

    # lets launch our webpage!
    # do 0.0.0.0 so that we can log into this webpage
    # using another computer on the same network later
    app.run(host='0.0.0.0')
