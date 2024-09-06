# robotframework-restbridge
Bridge that allows to run single keywords in robot framework via HTTP

## Configure required libraries
Edit `test.robot` to load all required Libraries
`
Library    Browser
Library    RequestsLibrary
...
``

## Start the bridge
$ sh a_start_robot.sh

## Then call it in a seperate window
$ sh b_test.sh