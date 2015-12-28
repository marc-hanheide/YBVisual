
echo '********************************************'
echo '                 YBVISUAL                   '
echo '********************************************'
echo 'Please for the system to start'
echo 'Launching simulation environment'
sleep 5
echo 'Done!'
echo 'Launching ROS components'
sleep 15
echo 'Done!'
echo 'Starting the server'
sleep 5
echo 'Done!'
echo 'Use the following address to connect to the robot: IP:8080'
echo 'Server setup successfully!'
echo ' '
echo ' _________________________________________________________'
echo 'Official Documentation: LINK HERE'
echo 'Tutorials: LINK HERE'
echo 'KUKA Robotics: LINK HERE'
cd lib
python localconsole.py
